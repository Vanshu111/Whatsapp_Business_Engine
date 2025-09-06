from typing import List, Tuple

class RAGStore:
    def __init__(self): pass
    def upsert(self, items: List[Tuple[str, str]]): pass       # (id, text)
    def search(self, query: str, k=5) -> List[str]: return []  # return top-k texts

def build_prompt(query: str, context_docs: list) -> str:
    context = "\n\n".join(context_docs[:5])
    return f"Context:\n{context}\n\nUser: {query}\n\nAnswer concisely."
