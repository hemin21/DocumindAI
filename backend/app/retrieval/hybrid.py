import numpy as np
from typing import List, Dict, Optional
from .tfidf import TFIDFRetriever
from .semantic import SemanticRetriever

def min_max_normalize(scores: np.ndarray) -> np.ndarray:
    """Min-max scales an array of scores into [0, 1]."""
    s_min = scores.min()
    s_max = scores.max()
    if s_max - s_min < 1e-9:
        return np.zeros_like(scores)
    return (scores - s_min) / (s_max - s_min)

class HybridRetriever:
    """
    Hybrid retriever combining Lexical (TF-IDF) and Semantic (Dense) scores.
    Formula:
        score = alpha * norm_tfidf + (1 - alpha) * norm_semantic
    alpha tuned on validation/dev split (default alpha = 0.4).
    """
    def __init__(self, tfidf: TFIDFRetriever, semantic: SemanticRetriever, alpha: float = 0.4):
        self.tfidf = tfidf
        self.semantic = semantic
        self.alpha = alpha

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        if not self.tfidf.doc_ids or self.semantic.doc_embeddings is None:
            return []

        # 1. TF-IDF raw cosine similarity vector across entire corpus
        q_vec = self.tfidf.vectorizer.transform([query])
        from sklearn.metrics.pairwise import cosine_similarity
        raw_tfidf = cosine_similarity(q_vec, self.tfidf.doc_matrix).flatten()

        # 2. Semantic raw cosine similarity vector across entire corpus
        q_emb = self.semantic.model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
        raw_semantic = np.dot(self.semantic.doc_embeddings, q_emb)

        # 3. Normalize scores
        norm_tfidf = min_max_normalize(raw_tfidf)
        norm_semantic = min_max_normalize(raw_semantic)

        # 4. Linear combination
        hybrid_scores = self.alpha * norm_tfidf + (1.0 - self.alpha) * norm_semantic

        top_k = min(top_k, len(self.tfidf.doc_ids))
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            score = float(hybrid_scores[idx])
            doc_id = self.tfidf.doc_ids[idx]
            doc_data = self.tfidf.corpus_lookup.get(doc_id, {})
            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "score": score,
                "tfidf_raw": float(raw_tfidf[idx]),
                "semantic_raw": float(raw_semantic[idx]),
                "title": doc_data.get("title", ""),
                "snippet": doc_data.get("text", "")[:300] + "...",
                "metadata": doc_data.get("metadata", {})
            })
        return results
