# ✅ backend/generate_vector_store.py

from langchain.text_splitter import CharacterTextSplitter


from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

# Constants
DB_PATH = "backend/vector_store.pkl"
TEXT_FILE_PATH = "data/cleaned_text.txt"

# Ensure file exists
if not os.path.exists(TEXT_FILE_PATH):
    raise FileNotFoundError(f"File not found: {TEXT_FILE_PATH}")

# Load cleaned text
with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_text(raw_text)


# Generate embeddings using SentenceTransformers
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDINGS_MODEL)
embeddings = model.encode(texts)

# Create FAISS index
import faiss
embeddings_np = np.array(embeddings)
if len(embeddings_np.shape) == 1:
    embeddings_np = embeddings_np.reshape(1, -1)
dimension = embeddings_np.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings_np.astype("float32"))

# Save FAISS index and texts
faiss.write_index(index, DB_PATH)
with open("backend/texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print(f"✅ Vector store and texts saved successfully to {DB_PATH} and backend/texts.pkl")
