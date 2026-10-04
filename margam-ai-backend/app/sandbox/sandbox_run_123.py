class RAG:
    def __init__(self, documents):
        self.documents = documents          # premade — already loaded
        self.vector_store = None            # gets built after embed() runs

    # --- USER_INJECTED_METHODS_START ---
    def chunk(self, document: str) -> list[str]:
        return [c.strip() + "." for c in document.split(".") if c.strip()]

    def embed(self, text: str) -> list[float]:
        return self.vector_store.embed_query(text)[:256].tolist()

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        return self.vector_store.search(self.embed(query), top_k)
    # --- USER_INJECTED_METHODS_END ---