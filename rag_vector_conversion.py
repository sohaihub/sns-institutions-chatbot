import json
import numpy as np
from sentence_transformers import SentenceTransformer
import uuid
from pathlib import Path

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def preprocess_entry(entry):
    # Skip entries with errors
    if entry.get('error'):
        return None
    
    # Combine relevant fields into a single text string
    text_parts = []
    
    # Add title
    if entry.get('title'):
        text_parts.append(entry['title'])
    
    # Add texts
    if entry.get('texts'):
        text_parts.extend(entry['texts'])
    
    # Add buttons
    if entry.get('buttons'):
        text_parts.extend([btn for btn in entry['buttons'] if btn])
    
    # Add link texts
    if entry.get('links'):
        text_parts.extend([link['text'] for link in entry['links'] if link['text']])
    
    # Join all parts into a single string
    combined_text = " ".join([str(part) for part in text_parts if part])
    
    if not combined_text.strip():
        return None
    
    return {
        'url': entry['url'],
        'text': combined_text,
        'metadata': {
            'title': entry.get('title', ''),
            'buttons': entry.get('buttons', []),
            'links': entry.get('links', []),
            'error': entry.get('error', None)
        }
    }

def generate_embeddings(texts, model):
    try:
        embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

def main():
    # Load JSON data
    file_path = r'D:\project\sns_scraped_data.json'
    data = load_json_data(file_path)
    if not data:
        print("No data loaded. Exiting.")
        return
    
    # Initialize the sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Preprocess entries
    processed_entries = []
    texts_to_embed = []
    for entry in data:
        processed = preprocess_entry(entry)
        if processed:
            processed_entries.append(processed)
            texts_to_embed.append(processed['text'])
    
    if not texts_to_embed:
        print("No valid texts to embed. Exiting.")
        return
    
    # Generate embeddings
    embeddings = generate_embeddings(texts_to_embed, model)
    if embeddings is None:
        print("Failed to generate embeddings. Exiting.")
        return
    
    # Combine embeddings with metadata
    vector_data = []
    for i, entry in enumerate(processed_entries):
        vector_data.append({
            'url': entry['url'],
            'vector': embeddings[i].tolist(),  # Convert numpy array to list for JSON
            'text': entry['text'],
            'metadata': entry['metadata']
        })
    
    # Save vectors to a JSON file
    output_path = 'snsct_vector_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vector_data, f, indent=2, ensure_ascii=False)
    
    print(f"Vector data saved to {output_path}")

if __name__ == "__main__":
    main()