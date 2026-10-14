import math
import pytest
from backend.app.preprocessing.normalizer import normalize_text, combine_title_and_text
from backend.app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    f1_at_k,
    reciprocal_rank,
    ndcg_at_k
)
from backend.app.retrieval.tfidf import TFIDFRetriever

def test_normalization():
    # Whitespace and unicode normalization
    raw = "  Hello \t\n world!   Café\u0301  "
    norm = normalize_text(raw)
    assert "Hello world!" in norm
    assert normalize_text(None) == ""
    assert normalize_text("") == ""

def test_combine_title_and_text():
    assert combine_title_and_text("Title", "Body text") == "Title — Body text"
    assert combine_title_and_text("Title", "") == "Title"
    assert combine_title_and_text("", "Body text") == "Body text"
    assert combine_title_and_text("", "") == ""

def test_ir_metrics_hand_crafted():
    # Synthetic scenario:
    # Retrieved docs: ['D1', 'D2', 'D3', 'D4', 'D5']
    # Ground truth relevant: {'D2', 'D4', 'D7'} (total 3 relevant)
    retrieved = ["D1", "D2", "D3", "D4", "D5"]
    relevant = {"D2", "D4", "D7"}

    # Precision@5: in top 5, D2 and D4 are relevant -> 2 / 5 = 0.4
    p5 = precision_at_k(retrieved, relevant, k=5)
    assert abs(p5 - 0.4) < 1e-6

    # Recall@5: 2 found out of 3 -> 2 / 3 = 0.66666...
    r5 = recall_at_k(retrieved, relevant, k=5)
    assert abs(r5 - (2.0 / 3.0)) < 1e-6

    # F1@5: harmonic mean
    f1 = f1_at_k(retrieved, relevant, k=5)
    expected_f1 = 2 * (0.4 * (2.0 / 3.0)) / (0.4 + (2.0 / 3.0))
    assert abs(f1 - expected_f1) < 1e-6

    # MRR: first relevant is D2 at rank 2 -> RR = 1 / 2 = 0.5
    rr = reciprocal_rank(retrieved, relevant)
    assert abs(rr - 0.5) < 1e-6

def test_zero_relevance_edge_cases():
    retrieved = ["D1", "D2"]
    empty_rel = set()
    assert precision_at_k(retrieved, empty_rel, k=5) == 0.0
    assert recall_at_k(retrieved, empty_rel, k=5) == 0.0
    assert f1_at_k(retrieved, empty_rel, k=5) == 0.0
    assert reciprocal_rank(retrieved, empty_rel) == 0.0
    assert ndcg_at_k(retrieved, {}, k=5) == 0.0

def test_ndcg_at_k():
    # Ideal order
    qrels = {"D1": 2, "D2": 1, "D3": 0}
    retrieved_ideal = ["D1", "D2", "D3"]
    # If ranked identically to ideal, nDCG should be 1.0
    assert abs(ndcg_at_k(retrieved_ideal, qrels, k=2) - 1.0) < 1e-6

    # Inverted order
    retrieved_suboptimal = ["D2", "D1", "D3"]
    ndcg = ndcg_at_k(retrieved_suboptimal, qrels, k=2)
    assert ndcg < 1.0
    assert ndcg > 0.0

def test_tfidf_retriever_toy():
    corpus = {
        "doc1": {"title": "Asthma Treatment", "text": "Inhaled corticosteroids reduce asthma flare-ups."},
        "doc2": {"title": "Cardiovascular Health", "text": "Statins lower cholesterol and heart disease risk."},
        "doc3": {"title": "Diet and Diabetes", "text": "Low glycemic foods help manage blood sugar levels."}
    }
    retriever = TFIDFRetriever(ngram_range=(1, 1), stop_words="english")
    retriever.fit_and_index(corpus)
    
    # Query with strong asthma overlap
    results = retriever.search("asthma corticosteroids", top_k=2)
    assert len(results) == 2
    assert results[0]["doc_id"] == "doc1"
    assert results[0]["score"] > results[1]["score"]

    # Empty query should return empty list
    assert retriever.search("", top_k=5) == []
    assert retriever.search("   ", top_k=5) == []
