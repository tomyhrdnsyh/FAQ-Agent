import numpy as np
import pickle
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor

class LocalRetriever:
    def __init__(self, embedding_path: str = "embeddings/embeddings.pkl"):
        self.embedding_path = embedding_path
        self.documents = self._load_embeddings()

    def _load_embeddings(self) -> List[Dict]:
        with open(self.embedding_path, "rb") as f:
            return pickle.load(f)

    def embed_query(self, embed_func, query: str) -> np.ndarray:
        """
        embed_func: function that takes a string and returns np.ndarray
        """
        return embed_func(query)

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    def retrieve(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[float, Dict]]:
        with ThreadPoolExecutor() as executor:
            scored = list(executor.map(lambda doc: {**{k: v for k, v in doc.items() if k not in ['embedding']}, 'score': self.cosine_similarity(query_vector, doc['embedding'])}, self.documents))

        return sorted(scored, key=lambda x: x['score'], reverse=True)[:top_k]
