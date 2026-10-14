import os
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from ..preprocessing.normalizer import normalize_text, combine_title_and_text

class SemanticRetriever:
    """
    Dense semantic retrieval engine using sentence-transformers/all-MiniLM-L6-v2.
    Embeddings are L2-normalized so dot product equals cosine similarity.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.doc_ids: List[str] = []
        self.doc_embeddings: Optional[np.ndarray] = None
        self.corpus_lookup: Dict[str, Dict] = {}

    def fit_and_index(self, corpus: Dict[str, Dict], batch_size: int = 64):
        """
        Encodes corpus documents in batches and creates dense embedding matrix.
        """
        self.doc_ids = list(corpus.keys())
        self.corpus_lookup = corpus
        texts = [
            combine_title_and_text(corpus[doc_id].get("title", ""), corpus[doc_id].get("text", ""))
            for doc_id in self.doc_ids
        ]
        print(f"[Semantic] Encoding {len(texts)} documents with {self.model_name}...")
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        self.doc_embeddings = embeddings
        print(f"[Semantic] Finished indexing. Embedding shape: {self.doc_embeddings.shape}")

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Encodes query, normalizes embedding, and computes cosine similarity with document embeddings.
        """
        if self.doc_embeddings is None or not self.doc_ids:
            return []

        query_norm = normalize_text(query)
        if not query_norm:
            return []

        query_embedding = self.model.encode(
            [query_norm],
            normalize_embeddings=True,
            convert_to_numpy=True
        )[0]

        # Since both query and document embeddings are L2-normalized,
        # cosine similarity is simply the inner product (dot product).
        scores = np.dot(self.doc_embeddings, query_embedding)

        top_k = min(top_k, len(self.doc_ids))
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            score = float(scores[idx])
            doc_id = self.doc_ids[idx]
            doc_data = self.corpus_lookup.get(doc_id, {})
            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "score": score,
                "title": doc_data.get("title", ""),
                "snippet": doc_data.get("text", "")[:300] + "...",
                "metadata": doc_data.get("metadata", {})
            })
        return results

    def save(self, filepath: Path):
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump({
                "model_name": self.model_name,
                "doc_ids": self.doc_ids,
                "doc_embeddings": self.doc_embeddings,
                "corpus_lookup": self.corpus_lookup
            }, f)
        print(f"[Semantic] Saved index to {filepath}")

    @classmethod
    def load(cls, filepath: Path) -> "SemanticRetriever":
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        instance = cls(model_name=data["model_name"])
        instance.doc_ids = data["doc_ids"]
        instance.doc_embeddings = data["doc_embeddings"]
        instance.corpus_lookup = data["corpus_lookup"]
        return instance
