# llm_response_agent.py

from utils.env_loader import get_google_api_key
import google.generativeai as genai

class LLMResponseAgent:
    def __init__(self, model_name="gemini-1.5-flash"):
        # ✅ Load API key during initialization (recommended)
        genai.configure(api_key=get_google_api_key())
        self.model = genai.GenerativeModel(model_name)

    def format_prompt(self, context_chunks, user_query):
        context_str = "\n\n".join(context_chunks)
        prompt = (
            f"You are an intelligent assistant answering questions based on the following context:\n\n"
            f"{context_str}\n\n"
            f"User's Question: {user_query}\n\n"
            f"Answer in a concise, helpful manner. If information is missing, say so clearly."
        )
        return prompt

    def generate_answer(self, context_chunks, query):
        prompt = self.format_prompt(context_chunks, query)
        response = self.model.generate_content(prompt)
        return response.text

    def mcp_generate(self, mcp_msg):
        context_chunks = mcp_msg["payload"]["retrieved_context"]
        query = mcp_msg["payload"]["query"]
        trace_id = mcp_msg["trace_id"]

        answer = self.generate_answer(context_chunks, query)

        return {
            "sender": "LLMResponseAgent",
            "receiver": "UI",
            "type": "FINAL_ANSWER",
            "trace_id": trace_id,
            "payload": {
                "query": query,
                "answer": answer,
                "sources": context_chunks
            }
        }
