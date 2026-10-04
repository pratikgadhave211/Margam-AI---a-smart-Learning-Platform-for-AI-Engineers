class RAG:
    def __init__(self, documents):
        self.documents = documents          # premade — already loaded
        self.vector_store = None            # gets built after embed() runs

    # --- USER_INJECTED_METHODS_START ---
    def chunk(self, document: str) -> list[str]:
        """
        Split a document into chunks.
        Return: list of text chunks.
        """
        # TODO: implement
        pass

    def embed(self, text: str) -> list[float]:
        """
        Convert a text chunk into an embedding vector.
        Return: list of floats.
        """
        # TODO: implement
        pass

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        """
        Retrieve the top_k most relevant chunks for the query.
        Return: list of chunk texts, ranked by relevance.
        """
        # TODO: implement 
        pass
    # --- USER_INJECTED_METHODS_END ---     


    