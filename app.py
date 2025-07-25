# app.py

import streamlit as st
from ingestion_agent import ingest_files
from retrieval_agent import RetrievalAgent
from llm_response_agent import LLMResponseAgent
from dotenv import load_dotenv
import tempfile
import os

# Load environment
load_dotenv()

# Initialize agents
retrieval_agent = RetrievalAgent()
llm_agent = LLMResponseAgent()

st.set_page_config(page_title="Multi-Format Agentic RAG Chatbot", layout="wide")
st.title("📄🔍 Multi-Format Agentic RAG Chatbot using Gemini")

# File upload
uploaded_files = st.file_uploader("Upload your documents (PDF, DOCX, PPTX, TXT, CSV)", type=["pdf", "docx", "pptx", "txt", "csv"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing files..."):
        # Save to temp files and get their paths
        file_paths = []
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[-1]) as tmp_file:
                tmp_file.write(file.read())
                file_paths.append(tmp_file.name)

        # Step 1: Ingestion
        ingestion_msg = ingest_files(file_paths, trace_id="001")

        # Step 2: Retrieval Agent builds vector store
        raw_text = ingestion_msg["payload"]["raw_text"]
        retrieval_agent.build_vector_store(raw_text)

        st.success("✅ Files ingested and indexed!")

        # Allow user to ask questions
        query = st.text_input("Ask a question based on the uploaded documents:")

        if query:
            with st.spinner("Thinking..."):
                # Step 3: Retrieve relevant chunks
                retrieval_msg = retrieval_agent.mcp_retrieve(query, trace_id="001")

                # Step 4: Generate answer from LLM
                final_msg = llm_agent.mcp_generate(retrieval_msg)

                # Show response
                st.subheader("💡 Answer:")
                st.markdown(final_msg["payload"]["answer"])

                # Show source chunks
                with st.expander("📚 Source Chunks Used"):
                    for i, chunk in enumerate(final_msg["payload"]["sources"], start=1):
                        st.markdown(f"**Chunk {i}:**\n```\n{chunk}\n```")
