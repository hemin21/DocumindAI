import re
from typing import List, Dict, Optional

def extract_direct_answer(query: str, doc_title: str, doc_text: str) -> str:
    """
    Extractive answer finding: locates the most direct sentence(s) in the
    retrieved document that answers or addresses the user's question.
    GUARANTEES a clean non-empty answer string so the UI always has an informative answer.
    """
    clean_text = (doc_text or "").strip()
    clean_title = (doc_title or "").strip()

    if not clean_text:
        return f"Key topic related to '{query}': {clean_title}" if clean_title else f"Identified scientific relevance to '{query}'."

    # Clean and split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    sentences = [s.strip() for s in sentences if len(s.strip().split()) >= 4]

    if not sentences:
        return clean_text[:250] + ("..." if len(clean_text) > 250 else "")

    # Query terms (ignore common stop words)
    stop_words = {
        "what", "is", "are", "how", "to", "can", "the", "a", "an", "and",
        "or", "in", "of", "for", "with", "do", "does", "did", "why", "which",
        "about", "on", "at", "by", "from", "be", "this", "that", "tell", "me"
    }
    raw_terms = re.findall(r'\b[a-zA-Z0-9-]{3,}\b', (query or "").lower())
    query_terms = [t for t in raw_terms if t not in stop_words]

    if not query_terms:
        # Fallback to the first informative abstract sentence
        for s in sentences:
            if len(s.split()) >= 8:
                return s
        return sentences[0]

    # Score each sentence based on keyword density and position
    scored_sentences = []
    for idx, sentence in enumerate(sentences):
        s_lower = sentence.lower()
        match_count = sum(1 for term in query_terms if term in s_lower)
        if match_count > 0:
            # Earlier sentences in research abstracts usually contain the problem & core definition
            pos_bonus = max(0, 1.0 - (idx * 0.04))
            score = match_count + pos_bonus
            scored_sentences.append((score, sentence))

    if scored_sentences:
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        return scored_sentences[0][1]

    # If no exact word overlap, return the opening summary sentence of the abstract
    for s in sentences:
        if len(s.split()) >= 8:
            return s
    return sentences[0]
