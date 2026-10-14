import time
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
from ..retrieval.tfidf import TFIDFRetriever
from ..retrieval.semantic import SemanticRetriever
from ..retrieval.hybrid import HybridRetriever
from ..database.db import log_search
from .qa_service import extract_direct_answer
from ..data.ai_concepts import get_ai_concepts

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
INDEX_DIR = DATA_DIR / "indexes"

class SearchService:
    _instance: Optional["SearchService"] = None

    def __init__(self):
        self.tfidf: Optional[TFIDFRetriever] = None
        self.semantic: Optional[SemanticRetriever] = None
        self.hybrid: Optional[HybridRetriever] = None
        self.ai_kb = get_ai_concepts()
        self.kb_embeddings: Optional[np.ndarray] = None
        self._load_models()

    def _load_models(self):
        tfidf_path = INDEX_DIR / "tfidf_index.pkl"
        semantic_path = INDEX_DIR / "semantic_index.pkl"

        if tfidf_path.exists():
            print(f"[SearchService] Loading TF-IDF from {tfidf_path}...")
            self.tfidf = TFIDFRetriever.load(tfidf_path)

        if semantic_path.exists():
            print(f"[SearchService] Loading Semantic model from {semantic_path}...")
            self.semantic = SemanticRetriever.load(semantic_path)
            # Pre-compute knowledge base embeddings for instant question answering
            kb_texts = [f"{c['title']} {c['text']}" for c in self.ai_kb]
            self.kb_embeddings = self.semantic.model.encode(
                kb_texts,
                normalize_embeddings=True,
                convert_to_numpy=True
            )

        if self.tfidf and self.semantic:
            self.hybrid = HybridRetriever(self.tfidf, self.semantic, alpha=0.35)

    @classmethod
    def get_instance(cls) -> "SearchService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def search(self, query: str, model_type: str = "semantic", top_k: int = 10) -> Dict[str, Any]:
        t0 = time.perf_counter()
        results: List[Dict[str, Any]] = []

        model_key = model_type.lower()
        if model_key == "tfidf" or model_key == "tf-idf":
            if self.tfidf:
                results = self.tfidf.search(query, top_k=top_k)
        elif model_key == "semantic":
            if self.semantic:
                results = self.semantic.search(query, top_k=top_k)
        elif model_key == "hybrid":
            if self.hybrid:
                results = self.hybrid.search(query, top_k=top_k)
        else:
            if self.semantic:
                results = self.semantic.search(query, top_k=top_k)

        latency_ms = (time.perf_counter() - t0) * 1000.0

        # Direct Answer Finding:
        # First check the verified foundational AI concept knowledge base for questions like
        # 'what is ai?', 'what is deep learning?', 'how does gradient descent work?'
        direct_answer = None
        if self.semantic and self.kb_embeddings is not None:
            q_emb = self.semantic.model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
            kb_scores = np.dot(self.kb_embeddings, q_emb)
            best_kb_idx = int(np.argmax(kb_scores))
            best_kb_score = float(kb_scores[best_kb_idx])
            
            # If the user's question has high alignment with an AI foundational concept (>= 0.45)
            if best_kb_score >= 0.45:
                direct_answer = self.ai_kb[best_kb_idx]["text"]

        # If not matched in foundational KB, extract directly from top retrieved research paper
        if not direct_answer and results and self.tfidf:
            top_doc_id = results[0]["doc_id"]
            top_doc = self.tfidf.corpus_lookup.get(top_doc_id, {})
            direct_answer = extract_direct_answer(
                query=query,
                doc_title=top_doc.get("title", ""),
                doc_text=top_doc.get("text", "")
            )

        # Log search asynchronously or to SQLite
        try:
            log_search(query, model_key, top_k, latency_ms, len(results))
        except Exception as e:
            print(f"Warning: Failed to log search history: {e}")

        return {
            "query": query,
            "model": model_key,
            "top_k": top_k,
            "latency_ms": latency_ms,
            "total_results": len(results),
            "direct_answer": direct_answer,
            "results": results
        }

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        # Check standard corpus first
        if self.tfidf and doc_id in self.tfidf.corpus_lookup:
            doc = self.tfidf.corpus_lookup[doc_id]
            return {
                "doc_id": doc_id,
                "title": doc.get("title", ""),
                "text": doc.get("text", ""),
                "metadata": doc.get("metadata", {})
            }
        # Check knowledge base
        for c in self.ai_kb:
            if c["id"] == doc_id:
                return {
                    "doc_id": c["id"],
                    "title": c["title"],
                    "text": c["text"],
                    "metadata": {"category": c["category"]}
                }
        return None

    def list_documents(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        if not self.tfidf:
            return {"total": 0, "documents": []}
        all_ids = self.tfidf.doc_ids
        total = len(all_ids)
        start = (page - 1) * page_size
        end = start + page_size
        selected_ids = all_ids[start:end]

        docs = []
        for did in selected_ids:
            item = self.tfidf.corpus_lookup.get(did, {})
            docs.append({
                "doc_id": did,
                "title": item.get("title", ""),
                "text": item.get("text", "")[:250] + "...",
                "metadata": item.get("metadata", {})
            })

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "documents": docs
        }
