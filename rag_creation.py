import os
import json
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("rag_preprocess.log"),
        logging.StreamHandler()
    ]
)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
logging.info("Initialized text splitter with chunk_size=1000, chunk_overlap=200")

# Folder where all .json files are stored
json_dir = "scraped_data"
output_file = "rag_documents.json"
documents = []

# Read all .json files
json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]

if not json_files:
    logging.warning(f"No JSON files found in {json_dir}")
else:
    for json_file in json_files:
        file_path = os.path.join(json_dir, json_file)
        logging.info(f"Processing JSON file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate it’s a dictionary with {url: {text, domain}}
            if not isinstance(data, dict):
                logging.warning(f"Skipping file {json_file}: Expected dict at root, got {type(data).__name__}")
                continue

            for url, content in data.items():
                if not isinstance(content, dict):
                    logging.warning(f"Skipping {url} in {json_file}: Content not a dictionary")
                    continue

                text = content.get("text", "").strip()
                domain = content.get("domain", "")

                if not text:
                    logging.warning(f"No text for {url} in {json_file}")
                    continue

                chunks = text_splitter.split_text(text)
                for chunk in chunks:
                    documents.append({
                        "page_content": chunk,
                        "metadata": {
                            "url": url,
                            "domain": domain,
                            "source_file": json_file
                        }
                    })

                logging.info(f"Processed {url} with {len(chunks)} chunks")

        except Exception as e:
            logging.error(f"Failed to process {file_path}: {e}")

# Save the final RAG-ready document
if documents:
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=4)
        logging.info(f"Saved {len(documents)} documents to {output_file}")
    except Exception as e:
        logging.error(f"Error saving {output_file}: {e}")
else:
    logging.warning("No documents to save")
