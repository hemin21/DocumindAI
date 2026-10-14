import csv
import json
import pandas as pd
from pathlib import Path
from backend.app.data.loader import CorpusLoader
from backend.app.retrieval.tfidf import TFIDFRetriever
from backend.app.retrieval.semantic import SemanticRetriever

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"
SCIDOCS_DIR = DATA_DIR / "raw" / "scidocs"
INDEX_DIR = DATA_DIR / "indexes"

def run_error_analysis():
    loader = CorpusLoader(SCIDOCS_DIR)
    queries = loader.load_queries()
    test_qrels = loader.load_qrels(split="test")
    
    tfidf = TFIDFRetriever.load(INDEX_DIR / "tfidf_index.pkl")
    semantic = SemanticRetriever.load(INDEX_DIR / "semantic_index.pkl")

    error_cases = []
    
    # Sample first 200 queries for error analysis
    sampled_qids = list(test_qrels.keys())[:200]

    for qid in sampled_qids:
        if qid not in queries:
            continue
        q_text = queries[qid]
        relevant_ids = {doc_id for doc_id, score in test_qrels[qid].items() if score > 0}
        if not relevant_ids:
            continue

        res_tfidf = tfidf.search(q_text, top_k=10)
        res_semantic = semantic.search(q_text, top_k=10)

        tfidf_ids = [r["doc_id"] for r in res_tfidf]
        semantic_ids = [r["doc_id"] for r in res_semantic]

        tfidf_has_rel = any(doc_id in relevant_ids for doc_id in tfidf_ids[:5])
        semantic_has_rel = any(doc_id in relevant_ids for doc_id in semantic_ids[:5])

        # Category 1: Lexical Mismatch (Semantic succeeded, TF-IDF missed)
        if semantic_has_rel and not tfidf_has_rel:
            category = "Lexical Mismatch (Vocabulary Gap in AI Concepts)"
            explanation = "Query used conceptual phrase or synonym (e.g., 'recurrent network') while relevant paper used specialized wording not overlapping exactly in TF-IDF."
            error_cases.append({
                "query_id": qid,
                "query_text": q_text,
                "error_category": category,
                "relevant_doc_count": len(relevant_ids),
                "tfidf_top_5": str(tfidf_ids[:5]),
                "semantic_top_5": str(semantic_ids[:5]),
                "explanation": explanation
            })

        # Category 2: Semantic Generalization / Specific Acronym Underweighting
        elif tfidf_has_rel and not semantic_has_rel:
            category = "Exact Acronym / Architecture Name Underweighting"
            explanation = "Query contained a specific AI algorithm name or mathematical term that TF-IDF matched directly, whereas dense bi-encoder averaged embedding across general semantics."
            error_cases.append({
                "query_id": qid,
                "query_text": q_text,
                "error_category": category,
                "relevant_doc_count": len(relevant_ids),
                "tfidf_top_5": str(tfidf_ids[:5]),
                "semantic_top_5": str(semantic_ids[:5]),
                "explanation": explanation
            })

        # Category 3: Both models missed in Top 5
        elif not tfidf_has_rel and not semantic_has_rel:
            category = "High Semantic Depth / Interdisciplinary Citation Gap"
            explanation = "Both lexical and dense models missed the ground-truth cited paper in Top-5, common when relevance is based on citation lineage rather than immediate textual similarity."
            error_cases.append({
                "query_id": qid,
                "query_text": q_text,
                "error_category": category,
                "relevant_doc_count": len(relevant_ids),
                "tfidf_top_5": str(tfidf_ids[:5]),
                "semantic_top_5": str(semantic_ids[:5]),
                "explanation": explanation
            })

    error_df = pd.DataFrame(error_cases)
    error_csv_path = RESULTS_DIR / "error_analysis.csv"
    error_df.to_csv(error_csv_path, index=False)
    print(f"[OK] Saved {len(error_cases)} AI error analysis cases to: {error_csv_path}")
    print("\nError Category Counts:")
    print(error_df["error_category"].value_counts().to_string())

if __name__ == "__main__":
    run_error_analysis()
