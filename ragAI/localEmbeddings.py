import requests
from langchain.embeddings.base import Embeddings

class LocalEmbeddings(Embeddings):
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embeds a list of documents."""
        return [self._get_embedding(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """Embeds a single query."""
        return self._get_embedding(text)

    def _get_embedding(self, text: str) -> list[float]:
        """Helper method to get embeddings from the local service."""
        payload = {
            "model": self.model,
            "input": text
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise RuntimeError(f"Failed to get embedding: {e}")