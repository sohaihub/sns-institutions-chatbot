🧠 SNS Institution Q&A Chatbot
An AI-powered Q&A chatbot for SNS Institutions, built using a fine-tuned Mistral-7B model, a RAG (Retrieval-Augmented Generation) system with FAISS, and an agentic AI approach. The chatbot is deployed via a Streamlit app with an integrated email automation agent for handling office-related queries.

📌 Table of Contents
Overview

Task 1: Model Selection and Setup

Task 2: Dataset Preprocessing

Task 3: Model Training

Task 4: Embedding Generation for RAG

Task 5: RAG System Implementation

Task 6: Chatbot Memory Setup

Task 7: Frontend Integration

Task 8: Agentic AI Approach

Task 9: Final Presentation & Documentation

Summary

🧾 Overview
The chatbot uses:

Mistral-7B for domain-specific generation

MiniLM embeddings for similarity search

FAISS for vector database management

LangChain memory for multi-turn conversations

Streamlit for UI

SMTP email agent for institutional queries

📘 Task 1: Model Selection and Setup
✅ Model Selection
SLM: Mistral-7B

Embeddings: sentence-transformers/all-MiniLM-L6-v2

⚙️ Setup
Libraries: transformers, torch, sentence-transformers, faiss-cpu

Model Loading:

AutoModelForCausalLM, AutoTokenizer for Mistral

SentenceTransformer for embeddings

📊 Task 2: Dataset Preprocessing
📥 Data Collection
SNS iHub Dataset: Academic and policy-related data

SNS Institution Dataset: FAQs, guidelines, documents

🧹 Preprocessing
Text cleaning (lowercase, special characters)

Converted to JSONL for training, TXT for embeddings

Chunked into 512 tokens

🧠 Task 3: Model Training
Fine-tuned Mistral-7B using Hugging Face's trainer

Learning Rate: 2e-5 | Batch Size: 4 | Epochs: 3

Optimized for domain-specific responses

📐 Task 4: Embedding Generation for RAG
🔤 Embedding Model
Used MiniLM to generate 384-d embeddings for chunks

🧠 Vector Database
FAISS for storage and similarity search

Top-5 documents retrieved using cosine similarity

🔁 Task 5: RAG System Implementation
🧱 RAG Pipeline
Retriever: FAISS

Generator: Mistral-7B with retrieved context

✏️ Prompt Template
text
Copy
Edit
You are a helpful Q&A chatbot for SNS Institutions. Use the following context to answer the user's question accurately and concisely. If the context is insufficient, rely on your knowledge but indicate uncertainty.

**Context**: {retrieved_documents}
**User Question**: {user_query}
**Answer**:
💬 Task 6: Chatbot Memory Setup
Used LangChain’s ConversationBufferMemory

Retains last 5 exchanges to provide continuity

Integrated into the RAG pipeline for context-aware replies

🖥️ Task 7: Frontend Integration
Developed a Streamlit App

Text input for user queries

Chat-style interface

SNS branding applied (logo, colors)

Hosted on Streamlit Cloud

🤖 Task 8: Agentic AI Approach
🌟 Why Agentic AI?
Separates concerns into specialized agents

Enhances reliability and extendability

📧 Email Automation Agent
Detects institutional queries via keywords

Sends formatted emails to SNS offices using smtplib

Example Email Prompt:
text
Copy
Edit
Subject: User Query from SNS Institution Chatbot

Dear [Office Name],

A user has submitted the following query via the SNS Institution Q&A Chatbot:

**Query**: {user_query}

Please provide the necessary information or assistance. For reference, the conversation history is as follows:

**Conversation History**: {conversation_history}

Regards,  
SNS Institution Chatbot
📑 Task 9: Final Presentation & Documentation
This README serves as comprehensive documentation

Project GitHub: SNS Institution Chatbot

Contents include:

Codebase

Model files

Preprocessed data

Setup guide

✅ Summary
This project demonstrates how to build a domain-specific chatbot using:

A fine-tuned Mistral-7B

A lightweight MiniLM-FAISS powered RAG

An agentic AI approach with email capabilities

A clean and user-friendly Streamlit frontend

The result is a responsive and intelligent assistant for SNS Institutions, capable of accurate answers and real-time email support.
