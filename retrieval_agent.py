# retrieval_agent.py

import faiss
import numpy as np
import google.generativeai as genai
from google.generativeai import embed_content
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.env_loader import get_google_api_key  # ✅ Make sure this is available

class RetrievalAgent:
    def __init__(self, model="models/embedding-001"):
        self.model = model
        self.text_chunks = []
        self.embeddings = []
        self.index = None
        self.text_id_map = {}

        # ✅ Configure Google API Key ONCE
        genai.configure(api_key=get_google_api_key())

    def chunk_text(self, raw_text, chunk_size=300, chunk_overlap=50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return splitter.split_text(raw_text)

    def get_embedding(self, text):
        response = embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return np.array(response["embedding"], dtype="float32")

    def build_vector_store(self, raw_text):
        self.text_chunks = self.chunk_text(raw_text)
        self.embeddings = [self.get_embedding(chunk) for chunk in self.text_chunks]
        embedding_dim = len(self.embeddings[0])

        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(self.embeddings))

        self.text_id_map = {i: chunk for i, chunk in enumerate(self.text_chunks)}

    def retrieve(self, query, top_k=3):
        query_embedding = self.get_embedding(query).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        retrieved_chunks = [self.text_id_map[i] for i in indices[0]]
        return retrieved_chunks

    def mcp_retrieve(self, query, trace_id="trace-001"):
        chunks = self.retrieve(query)
        return {
            "sender": "RetrievalAgent",
            "receiver": "LLMResponseAgent",
            "type": "RETRIEVAL_RESULT",
            "trace_id": trace_id,
            "payload": {
                "retrieved_context": chunks,
                "query": query
            }
        }
