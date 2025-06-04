import json
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain.memory import ConversationBufferMemory

class ModelSetup:
    def __init__(self, model_name="microsoft/phi-2"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.embedding_model = None
        self.faiss_index = None
        self.vector_data = None
        self.memory = ConversationBufferMemory()

    def setup_model(self):
        try:
            # Configure for efficient loading
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                padding_side="left"
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16
            )

            print(f"Model {self.model_name} loaded successfully!")
            return True

        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def setup_rag(self, vector_data_path='D:/project/snsct_vector_data.json'):
        try:
            # Load embedding model
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("Embedding model loaded successfully!")

            # Load vector data
            with open(vector_data_path, 'r', encoding='utf-8') as f:
                self.vector_data = json.load(f)
            if not self.vector_data:
                print("No vector data loaded.")
                return False

            # Create FAISS index
            vectors = [item['vector'] for item in self.vector_data]
            if not vectors:
                print("No vectors found.")
                return False
            dimension = len(vectors[0])
            self.faiss_index = faiss.IndexFlatL2(dimension)
            self.faiss_index.add(np.array(vectors, dtype=np.float32))
            print("FAISS index created successfully!")
            return True

        except Exception as e:
            print(f"Error setting up RAG: {e}")
            return False

    def retrieve_documents(self, query, k=5):
        if not self.embedding_model or not self.faiss_index or not self.vector_data:
            print("RAG components not initialized.")
            return []
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.faiss_index.search(query_embedding, k)
        retrieved_docs = [
            {
                'text': self.vector_data[i]['text'],
                'url': self.vector_data[i]['url'],
                'metadata': self.vector_data[i]['metadata'],
                'distance': float(distances[0][j])
            }
            for j, i in enumerate(indices[0])
        ]
        return retrieved_docs

    def generate_response(self, query, retrieved_docs):
        history = self.memory.load_memory_variables({}).get('history', '')
        context_str = "\n".join([doc['text'] for doc in retrieved_docs]) if retrieved_docs else "I don’t have specific info on that."

        prompt = f"""
Hey there! I'm your friendly SNS Institutions assistant. I've got some info to share based on your question. Here's the scoop:

**Previous Chat**: {history}

**Info I Found**: {context_str}

**Your Question**: {query}

**My Answer**: Alright, let's get to it! 
"""
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(self.model.device)
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=100,
            temperature=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("**My Answer**: Alright, let's get to it!")[1].strip()
        self.memory.save_context({"input": query}, {"output": response})
        return response

    def get_model_info(self):
        if self.model:
            return {
                "model_name": self.model_name,
                "vocab_size": self.tokenizer.vocab_size,
                "model_size": sum(p.numel() for p in self.model.parameters()),
                "device": next(self.model.parameters()).device
            }
        return None

RECOMMENDED_MODELS = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.1",
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "deepseek": "deepseek-ai/deepseek-coder-1.3b-instruct",
    "phi": "microsoft/phi-2"
}

def main():
    # Initialize and setup model
    model_setup = ModelSetup(model_name=RECOMMENDED_MODELS["phi"])
    if not model_setup.setup_model():
        print("Failed to setup model. Exiting.")
        return

    # Setup RAG components
    if not model_setup.setup_rag():
        print("Failed to setup RAG. Exiting.")
        return

    print("SNS Institutions Chatbot is ready! Let's chat.")
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("See you later!")
            break

        print(f"\nYou asked: {query}")
        retrieved_docs = model_setup.retrieve_documents(query, k=5)
        print("\nHere's what I found:")
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"Doc {i}:")
            print(f"  Text: {doc['text'][:100]}...")
            print(f"  URL: {doc['url']}")
            print(f"  Title: {doc['metadata']['title']}")
            print(f"  Distance: {doc['distance']:.4f}")

        response = model_setup.generate_response(query, retrieved_docs)
        print(f"\nMy Response: {response}")

if __name__ == "__main__":
    main()