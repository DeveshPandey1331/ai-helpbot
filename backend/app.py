# backend/app.py


import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "backend/vector_store.pkl"
TEXTS_PATH = "backend/texts.pkl"
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"

model = SentenceTransformer(EMBEDDINGS_MODEL)
index = faiss.read_index(DB_PATH)
with open(TEXTS_PATH, "rb") as f:
    texts = pickle.load(f)

def get_most_relevant_answer(query):
    query_emb = model.encode([query])
    if len(query_emb.shape) == 1:
        query_emb = query_emb.reshape(1, -1)
    D, I = index.search(np.array(query_emb).astype("float32"), k=1)
    idx = I[0][0]
    return texts[idx]



# API route
@app.post("/ask")
async def ask_question(request: Request):
    body = await request.json()
    query = body.get("question")
    if not query:
        return {"error": "No question provided."}
    answer = get_most_relevant_answer(query)
    return {
        "question": query,
        "answer": answer,
        "sources": []
    }

# Root route (optional)
@app.get("/")
def read_root():
    return {"message": "AI Help Bot Backend is Running!"}
