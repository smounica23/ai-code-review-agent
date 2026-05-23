import chromadb
from config import settings

class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.security_collection = self.client.get_collection("security_guidelines")
        self.python_collection = self.client.get_collection("python_guidelines")
        self.java_collection = self.client.get_collection("java_guidelines")
        self.secure_coding_collection = self.client.get_collection("secure_coding")

    def retrieve(self, query: str, language: str, k: int = 5) -> list[str]:
        chunks = []
        collections = [self.security_collection, self.secure_coding_collection]

        language = language.lower()
        if language == "python":
            collections.append(self.python_collection)
        elif language == "java":
            collections.append(self.java_collection)

        for collection in collections:
            result = collection.query(
                query_texts=[query],
                n_results=k
            )
            documents = result.get("documents", [[]])
            if documents and documents[0]:
                chunks.extend(documents[0])

        return chunks