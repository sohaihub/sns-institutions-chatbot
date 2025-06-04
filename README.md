SNS Institution Q&A Chatbot Project Documentation
SNS Institution Q&A Chatbot Project Documentation	1
Overview	1
Task 1: Model Selection and Setup	2
Model Selection	2
Setup	2
Task 2: Dataset Preprocessing	2
Data Collection	2
Preprocessing	2
Task 3: Model Training	2
Fine-Tuning	3
Task 4: Embedding Generation for RAG	3
Embedding Model	3
Vector Database	3
Task 5: RAG System Implementation	3
RAG Pipeline	3
Prompt Design	3
Task 6: Chatbot Memory Setup	4
Conversation Memory	4
Task 7: Frontend Integration	5
Streamlit App	5
Task 8: Agentic AI Approach	5
Why Agentic AI?	5
Email Automation Agent	5
Task 9: Final Presentation & Documentation	7
Documentation	7
Summary	7

Overview
This project involves the development of an AI-powered Q&A chatbot for SNS Institutions, utilizing a fine-tuned small language model (SLM) from Hugging Face, a Retrieval-Augmented Generation (RAG) system with a vector database, and an agentic AI approach for enhanced efficiency. The chatbot is integrated with a Streamlit-based user interface for rapid deployment and includes an email automation agent to handle queries requiring institutional office interaction. Below is a detailed description of the process, models used, prompts, and the agentic AI implementation.
Task 1: Model Selection and Setup
Model Selection
We selected Mistral-7B from Hugging Face as the small language model (SLM) due to its balance of performance and efficiency for domain-specific tasks. For embedding generation, we used the sentence-transformers/all-MiniLM-L6-v2 model, which is optimized for generating compact and effective embeddings for text similarity tasks.
Setup
Environment: The models were set up using Python with the Hugging Face Transformers library and PyTorch as the backend framework.
Dependencies: Installed required libraries including transformers, torch, sentence-transformers, and faiss-cpu for vector database operations.
Model Loading: The Mistral-7B model was loaded using the AutoModelForCausalLM and AutoTokenizer classes, and the sentence-transformers model was initialized for embedding generation.
Task 2: Dataset Preprocessing
Data Collection
SNS iHub Dataset: Collected a dataset containing domain-specific information about SNS Institutions, including academic programs, institutional policies, for fine-tuning the SLM.
SNS Institutions Dataset: Gathered a broader dataset for the RAG system, including FAQs, institutional guidelines, and public-facing documents.
Preprocessing
Cleaning: Removed inconsistencies, duplicates, and irrelevant content from both datasets. Applied text normalization (e.g., lowercasing, removing special characters).
Format Conversion: Converted documents into JSONL format for training and TXT format for embedding generation. Each document was segmented into chunks of 512 tokens to optimize for embedding and retrieval.

Task 3: Model Training
Fine-Tuning
Framework: Used Hugging Face’s Transformers library to fine-tune the Mistral-7B model on the SNS iHub dataset.
Training Setup: Configured a training pipeline with a learning rate of 2e-5, batch size of 4, and 3 epochs, optimizing for domain-specific knowledge about SNS Institutions.
Task 4: Embedding Generation for RAG
Embedding Model
Used the sentence-transformers/all-MiniLM-L6-v2 model to generate 384-dimensional embeddings for the SNS Institutions dataset.
Process: Each document chunk was processed to create vector embeddings, ensuring semantic representation for similarity search.
Vector Database
Database: Employed FAISS (Facebook AI Similarity Search) as the vector database for efficient storage and retrieval of embeddings.
Implementation: Inserted document chunks and their corresponding embeddings into FAISS, indexing them for cosine similarity-based search.
Query Function: Implemented a similarity search function to retrieve the top-5 relevant documents for a given user query.
Task 5: RAG System Implementation
RAG Pipeline
Retrieval Component: Configured FAISS to retrieve relevant document chunks based on user queries, using cosine similarity to rank results.
Generation Component: Integrated the fine-tuned Mistral-7B model to generate responses. The retrieved documents were used as context to enhance response accuracy.
Prompt Design
The RAG system used the following prompt template to combine user queries with retrieved context:

You are a helpful Q&A chatbot for SNS Institutions. Use the following context to answer the user's question accurately and concisely. If the context is insufficient, rely on your knowledge but indicate uncertainty.

**Context**: {retrieved_documents}

**User Question**: {user_query}

**Answer**:
Example Prompt:

You are a helpful Q&A chatbot for SNS Institutions. Use the following context to answer the user's question accurately and concisely. If the context is insufficient, rely on your knowledge but indicate uncertainty.

**Context**: SNS Institutions offers undergraduate programs in Computer Science, Mechanical Engineering, and Biotechnology. The admission process requires a minimum of 60% in 12th-grade exams.

**User Question**: What are the eligibility criteria for undergraduate programs at SNS Institutions?

**Answer**:


Testing: Validated the RAG pipeline by testing with sample queries, ensuring accurate retrieval and coherent response generation.
Task 6: Chatbot Memory Setup
Conversation Memory
Framework: Used LangChain to implement conversation memory, enabling multi-turn interactions.
Implementation: Stored conversation history in a ConversationBufferMemory object, which maintained the last 5 exchanges to provide context for follow-up questions.
Integration: Linked the memory component to the RAG pipeline, ensuring that previous interactions influenced the context for new queries.
Task 7: Frontend Integration
Streamlit App
Framework Choice: Opted for Streamlit for its simplicity and rapid deployment capabilities, allowing for a user-friendly chatbot interface.
UI Components:
Input Box: A text input field for users to submit queries.
Response Display: A chat-like interface showing the conversation history, with user queries and bot responses.
Styling: Used Streamlit’s built-in styling to create a clean, professional look with SNS Institutions branding (e.g., logo, color scheme).
Hosting: Deployed the Streamlit app on a cloud platform (Streamlit Cloud) for accessibility.
Task 8: Agentic AI Approach
Why Agentic AI?
Instead of a purely generative AI approach, we adopted an agentic AI framework to enhance efficiency and functionality. The agentic approach involves multiple specialized agents working collaboratively:
Chatbot Agent: Handles user queries using the RAG pipeline and conversation memory.
Email Automation Agent: Manages queries requiring interaction with the SNS Institutions office by sending automated emails.
Email Automation Agent
Functionality: If the chatbot identifies a query that requires human intervention (e.g., specific admission details, document requests), it triggers the email automation agent.
Implementation:
Used the smtplib library in Python to send emails via an SMTP server.
Configured the agent to format queries into professional emails and send them to a designated institutional email address.
Prompt for Email Generation:
 text
CollapseWrap
Copy
Subject: User Query from SNS Institution Chatbot

Dear [Office Name],

A user has submitted the following query via the SNS Institution Q&A Chatbot:

**Query**: {user_query}

Please provide the necessary information or assistance. For reference, the conversation history is as follows:

**Conversation History**: {conversation_history}

Regards,
SNS Institution Chatbot


Example Email:
 text
CollapseWrap
Copy
Subject: User Query from SNS Institution Chatbot

Dear Admissions Office,

A user has submitted the following query via the SNS Institution Q&A Chatbot:

**Query**: Can you provide the application deadline for the Computer Science program?

Please provide the necessary information or assistance. For reference, the conversation history is as follows:

**Conversation History**: User: What programs are offered? | Bot: SNS Institutions offers undergraduate programs in Computer Science, Mechanical Engineering, and Biotechnology.

Regards,
SNS Institution Chatbot


Integration: The chatbot agent detects keywords (e.g., “deadline,” “application”) to route queries to the email agent, ensuring seamless interaction.
Task 9: Final Presentation & Documentation
Documentation
This document serves as the comprehensive project documentation, detailing the process, models, prompts, and agentic AI implementation.
GitHub Link: [(https://github.com/sohaihub/sns-institutions-chatbot/)](https://github.com/sohaihub/sns-institutions-chatbot/)
Contents: Includes all code, model checkpoints, datasets, and a README with setup and usage instructions.
Summary
The SNS Institution Q&A Chatbot was built using a fine-tuned Mistral-7B model and a RAG system powered by sentence-transformers and FAISS. The agentic AI approach, with a chatbot agent and an email automation agent, ensures efficient query handling and institutional connectivity. A Streamlit app provides a user-friendly interface, and the project is fully documented with a structured GitHub repository.


