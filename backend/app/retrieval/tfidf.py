import os
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from ..preprocessing.normalizer import normalize_text, combine_title_and_text

class TFIDFRetriever:
    """
    Lexical retrieval engine based on scikit-learn TfidfVectorizer.
    Fitted once on corpus documents, with sparse matrix cosine similarity.
    """
    def __init__(
        self,
        ngram_range: Tuple[int, int] = (1, 2),
        stop_words: str = "english",
        max_features: Optional[int] = 50000,
        sublinear_tf: bool = True
    ):
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            stop_words=stop_words,
            max_features=max_features,
            sublinear_tf=sublinear_tf,
            lowercase=True
        )
        self.doc_ids: List[str] = []
        self.doc_matrix: Optional[csr_matrix] = None
        self.corpus_lookup: Dict[str, Dict] = {}

    def fit_and_index(self, corpus: Dict[str, Dict]):
        """
        Fits vectorizer and builds sparse document term matrix.
        corpus format: {doc_id: {'title': str, 'text': str, ...}}
        """
        self.doc_ids = list(corpus.keys())
        self.corpus_lookup = corpus
        texts = [
            combine_title_and_text(corpus[doc_id].get("title", ""), corpus[doc_id].get("text", ""))
            for doc_id in self.doc_ids
        ]
        self.doc_matrix = self.vectorizer.fit_transform(texts)
        print(f"[TF-IDF] Fitted vectorizer on {len(self.doc_ids)} docs. Vocabulary size: {len(self.vectorizer.vocabulary_)}")

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Calculates cosine similarity and returns ranked list of top_k results.
        """
        if self.doc_matrix is None or not self.doc_ids:
            return []
        
        query_norm = normalize_text(query)
        if not query_norm:
            return []

        query_vec = self.vectorizer.transform([query_norm])
        # Compute cosine similarity with all doc vectors
        scores = cosine_similarity(query_vec, self.doc_matrix).flatten()
        
        # Get top-k indices
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
                "vectorizer": self.vectorizer,
                "doc_ids": self.doc_ids,
                "doc_matrix": self.doc_matrix,
                "corpus_lookup": self.corpus_lookup
            }, f)
        print(f"[TF-IDF] Saved index to {filepath}")

    @classmethod
    def load(cls, filepath: Path) -> "TFIDFRetriever":
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        instance = cls()
        instance.vectorizer = data["vectorizer"]
        instance.doc_ids = data["doc_ids"]
        instance.doc_matrix = data["doc_matrix"]
        instance.corpus_lookup = data["corpus_lookup"]
        return instance
