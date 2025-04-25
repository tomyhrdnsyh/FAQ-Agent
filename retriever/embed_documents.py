import os, pickle, srsly
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
import numpy as np
from loguru import logger

from openai import OpenAI

class EmbeddingGenerator:
    def __init__(
        self,
        model: str = "text-embedding-3-large",
        api_key: str = None,
        save_path: str = "data/faq_embeddings.pkl",
        embedding_fields: List = ['question', 'description']
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.save_path = Path(save_path)
        self.embedding_fields = embedding_fields

    def load_data(self, json_path: str) -> List[Dict]:
        return srsly.read_json(json_path)

    def embed_text(self, text: str) -> np.ndarray:
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            return np.array(response.data[0].embedding, dtype=np.float32)
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise ConnectionError(f"OpenAI Embedding failed: {e}") 

    def embed_and_save(self, input_path: str):
        data = self.load_data(input_path)

        if self.save_path.exists():
            logger.info(f"Cached embeddings found: {self.save_path.name}")
            return  # skip if already embedded

        embedded_data = []
        for item in tqdm(data, desc="Embedding documents"):
            combined_text = ' '.join([v for k, v in item.items() if k in self.embedding_fields])
            embedding = self.embed_text(combined_text)
            embedded_data.append({
                **item,
                "embedding": embedding,
            })

        with open(self.save_path, "wb") as f:
            pickle.dump(embedded_data, f)

        logger.success(f"Embeddings saved to {self.save_path.name}")

    def load_embeddings(self) -> List[Dict]:
        if not self.save_path.exists():
            raise FileNotFoundError("Embedding file not found. Please run embed_and_save() first.")
        with open(self.save_path, "rb") as f:
            return pickle.load(f)


if __name__ == "__main__":
    embedder = EmbeddingGenerator()
    embedder.embed_and_save("data/faq_preprocessed.json")
