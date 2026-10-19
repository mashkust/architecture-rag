import os
from langchain_ollama import ChatOllama


def get_llm():
    model = os.getenv("RAG_OLLAMA_MODEL", "llama3.1")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    return ChatOllama(model=model, base_url=base_url, temperature=0)
