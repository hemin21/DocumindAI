import math
from typing import List, Dict, Set

def precision_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    """
    Precision@K = (Number of relevant documents in top K) / K
    """
    if k <= 0:
        return 0.0
    top_k = retrieved_ids[:k]
    rel_in_k = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return rel_in_k / float(k)

def recall_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    """
    Recall@K = (Number of relevant documents in top K) / (Total known relevant documents)
    If a query has 0 relevant documents, recall is defined as 0.0.
    """
    if not relevant_ids or k <= 0:
        return 0.0
    top_k = retrieved_ids[:k]
    rel_in_k = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return rel_in_k / float(len(relevant_ids))

def f1_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
    """
    F1@K = Harmonic mean of Precision@K and Recall@K. Returns 0.0 if both are 0.
    """
    p = precision_at_k(retrieved_ids, relevant_ids, k)
    r = recall_at_k(retrieved_ids, relevant_ids, k)
    if p + r == 0:
        return 0.0
    return 2.0 * (p * r) / (p + r)

def reciprocal_rank(retrieved_ids: List[str], relevant_ids: Set[str]) -> float:
    """
    Reciprocal Rank = 1 / rank of the first relevant document retrieved (1-indexed).
    If no relevant document is retrieved, returns 0.0.
    """
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / float(rank)
    return 0.0

def ndcg_at_k(retrieved_ids: List[str], qrels: Dict[str, int], k: int) -> float:
    """
    Normalized Discounted Cumulative Gain at K (nDCG@K).
    Standard formulation:
      DCG@K = sum_{i=1}^K (2^{rel_i} - 1) / log2(i + 1)
      IDCG@K = ideal DCG obtained by sorting true relevance grades descending.
    """
    if k <= 0 or not qrels:
        return 0.0

    # Calculate DCG@K
    dcg = 0.0
    for i, doc_id in enumerate(retrieved_ids[:k], start=1):
        rel = qrels.get(doc_id, 0)
        if rel > 0:
            dcg += (math.pow(2, rel) - 1.0) / math.log2(i + 1)

    # Calculate Ideal DCG@K (sort true qrel scores in descending order)
    ideal_scores = sorted(qrels.values(), reverse=True)[:k]
    idcg = 0.0
    for i, rel in enumerate(ideal_scores, start=1):
        if rel > 0:
            idcg += (math.pow(2, rel) - 1.0) / math.log2(i + 1)

    if idcg == 0.0:
        return 0.0
    return dcg / idcg
