import time
import json
import csv
import platform
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from backend.app.data.loader import CorpusLoader
from backend.app.retrieval.tfidf import TFIDFRetriever
from backend.app.retrieval.semantic import SemanticRetriever
from backend.app.retrieval.hybrid import HybridRetriever
from backend.app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    f1_at_k,
    reciprocal_rank,
    ndcg_at_k
)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"
SCIDOCS_DIR = DATA_DIR / "raw" / "scidocs"
INDEX_DIR = DATA_DIR / "indexes"

def run_evaluation():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    loader = CorpusLoader(SCIDOCS_DIR)
    queries = loader.load_queries()
    test_qrels = loader.load_qrels(split="test")
    
    print(f"Total SciDocs test queries with relevance judgments: {len(test_qrels)}")

    print("Loading indexes...")
    tfidf = TFIDFRetriever.load(INDEX_DIR / "tfidf_index.pkl")
    semantic = SemanticRetriever.load(INDEX_DIR / "semantic_index.pkl")
    hybrid = HybridRetriever(tfidf, semantic, alpha=0.35)

    models = {
        "TF-IDF": tfidf,
        "Semantic (all-MiniLM-L6-v2)": semantic,
        "Hybrid (TF-IDF + Semantic)": hybrid
    }

    per_query_records = []
    ranked_results_export = []
    
    # Pre-select evaluated queries (those with at least 1 relevant document in qrels)
    eval_qids = [qid for qid in test_qrels.keys() if qid in queries and any(score > 0 for score in test_qrels[qid].values())]
    print(f"Number of AI queries evaluated: {len(eval_qids)}")

    summary_metrics = {}

    for model_name, retriever in models.items():
        print(f"\n--- Evaluating Model: {model_name} ---")
        p5_list = []
        r5_list = []
        f1_list = []
        rr_list = []
        ndcg10_list = []
        latencies = []

        for qid in tqdm(eval_qids, desc=f"Evaluating {model_name}"):
            q_text = queries[qid]
            q_qrels = test_qrels[qid]
            relevant_ids = {doc_id for doc_id, score in q_qrels.items() if score > 0}

            t0 = time.perf_counter()
            results = retriever.search(q_text, top_k=20)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(latency_ms)

            retrieved_ids = [res["doc_id"] for res in results]

            p5 = precision_at_k(retrieved_ids, relevant_ids, k=5)
            r5 = recall_at_k(retrieved_ids, relevant_ids, k=5)
            f1 = f1_at_k(retrieved_ids, relevant_ids, k=5)
            rr = reciprocal_rank(retrieved_ids, relevant_ids)
            ndcg10 = ndcg_at_k(retrieved_ids, q_qrels, k=10)

            p5_list.append(p5)
            r5_list.append(r5)
            f1_list.append(f1)
            rr_list.append(rr)
            ndcg10_list.append(ndcg10)

            per_query_records.append({
                "model": model_name,
                "query_id": qid,
                "query_text": q_text,
                "precision@5": p5,
                "recall@5": r5,
                "f1@5": f1,
                "reciprocal_rank": rr,
                "ndcg@10": ndcg10,
                "latency_ms": latency_ms,
                "num_relevant": len(relevant_ids)
            })

            if len(ranked_results_export) < 1000:
                ranked_results_export.append({
                    "model": model_name,
                    "query_id": qid,
                    "retrieved": retrieved_ids[:10]
                })

        summary_metrics[model_name] = {
            "Precision@5": float(np.mean(p5_list)),
            "Recall@5": float(np.mean(r5_list)),
            "F1@5": float(np.mean(f1_list)),
            "MRR": float(np.mean(rr_list)),
            "nDCG@10": float(np.mean(ndcg10_list)),
            "Mean Latency (ms)": float(np.mean(latencies)),
            "Median Latency (ms)": float(np.median(latencies)),
            "P95 Latency (ms)": float(np.percentile(latencies, 95)),
            "Evaluated Queries": len(eval_qids),
            "Indexed Documents": len(tfidf.doc_ids)
        }

    # Save summary metrics
    summary_df = pd.DataFrame.from_dict(summary_metrics, orient="index")
    summary_df.index.name = "Model"
    summary_csv_path = RESULTS_DIR / "metrics_summary.csv"
    summary_df.to_csv(summary_csv_path)
    print(f"\n[OK] Metrics summary saved to: {summary_csv_path}")
    print(summary_df.to_string())

    # Save per-query metrics
    per_query_df = pd.DataFrame(per_query_records)
    per_query_csv_path = RESULTS_DIR / "per_query_metrics.csv"
    per_query_df.to_csv(per_query_csv_path, index=False)
    print(f"[OK] Per-query metrics saved to: {per_query_csv_path}")

    # Save ranked results JSONL
    ranked_jsonl_path = RESULTS_DIR / "ranked_results.jsonl"
    with open(ranked_jsonl_path, "w", encoding="utf-8") as f:
        for row in ranked_results_export:
            f.write(json.dumps(row) + "\n")

    # Save Experiment Config
    config_data = {
        "dataset": "SciDocs (BEIR benchmark for Computer Science & AI)",
        "split": "test",
        "num_evaluated_queries": len(eval_qids),
        "total_documents": len(tfidf.doc_ids),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "hardware": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        },
        "models": {
            "TF-IDF": {
                "ngram_range": [1, 2],
                "stop_words": "english",
                "max_features": 60000,
                "sublinear_tf": True
            },
            "Semantic": {
                "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                "embedding_dimension": 384,
                "similarity": "cosine (inner product of normalized embeddings)"
            },
            "Hybrid": {
                "alpha": 0.35,
                "score_fusion": "alpha * norm_tfidf + (1 - alpha) * norm_semantic"
            }
        },
        "summary_results": summary_metrics
    }
    config_path = RESULTS_DIR / "experiment_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
    print(f"[OK] Experiment config saved to: {config_path}")

if __name__ == "__main__":
    run_evaluation()
