**💬 Agentic RAG Chatbot for Multi-Format Document QA (with Gemini & MCP)**

This project implements an agent-based Retrieval-Augmented Generation (RAG) chatbot that allows users to upload multi-format documents and ask natural language questions over the contents. It uses Google Gemini models, a custom Model Context Protocol (MCP) for message-passing between agents, and a simple Streamlit UI.

**📌 Features**

✅ Accepts and parses documents in PDF, PPTX, DOCX, CSV, TXT/Markdown

✅ Uses Gemini Embeddings + FAISS for vector search

✅ Uses Gemini 1.5 Flash LLM to answer user queries

✅ Modular 3-Agent architecture:

IngestionAgent: Parses and extracts raw text from files

RetrievalAgent: Embeds and retrieves relevant context

LLMResponseAgent: Formats prompt and generates LLM answer

✅ Communication via custom Model Context Protocol (MCP)

✅ Simple Streamlit UI for file upload, query input, and answer display

**📁 Project Structure**

├── app.py                    # Streamlit app

├── ingestion_agent.py        # IngestionAgent: parses uploaded files

├── retrieval_agent.py        # RetrievalAgent: handles embeddings & retrieval

├── llm_response_agent.py     # LLMResponseAgent: interacts with Gemini LLM

├── env_loader.py             # Loads Gemini API key from .env

├── .env                      # Stores your GEMINI_API_KEY (DO NOT COMMIT!)

└── requirements.txt          # Python dependencies

**Install dependencies**

pip install -r requirements.txt

**🛠 Tech Stack**

| Layer     | Tools / Libraries                          |
| --------- | ------------------------------------------ |
| LLM       | `google.generativeai` (Gemini 1.5 Flash)   |
| Embedding | `embed_content` (Gemini `embedding-001`)   |
| Vector DB | `FAISS` (in-memory vector index)           |
| Parsing   | `PyMuPDF`, `python-docx`, `pptx`, `pandas` |
| UI        | `Streamlit`                                |
| Auth      | `dotenv` for API key loading               |

**🌱 Future Improvements**

Add support for multi-turn chat history

Add asynchronous agent orchestration

Use ChromaDB or Pinecone for scalable vector DB

Add file-type tags to source context chunks


