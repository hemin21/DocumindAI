# Methodology Documentation: DocuMind AI

## 1. System Architecture
DocuMind AI implements an information retrieval pipeline:
1. **Corpus Ingestion & Preprocessing**:
   - NFKD Unicode normalization.
   - Whitespace and line-break compression.
   - Title and abstract textual combination with separator tokens (`Title — Body text`).
2. **Lexical Representation (TF-IDF Baseline)**:
   - Built using scikit-learn's `TfidfVectorizer`.
   - Feature space: Unigrams and bigrams (`ngram_range=(1, 2)`), English stop-word filtering, max vocabulary 50,000 features.
   - Sublinear term frequency (`1 + log(tf)`).
   - Scoring: Cosine similarity between query vector and sparse document term matrix.
3. **Dense Semantic Representation (Sentence Transformers)**:
   - Model: `sentence-transformers/all-MiniLM-L6-v2` (6 layers, 384 embedding dimensions).
   - Inverted/batch encoding with L2 vector normalization.
   - Scoring: Normalized dot product (equivalent to cosine similarity).
4. **Hybrid Retrieval Fusion**:
   - Min-Max normalization mapping lexical and dense score vectors onto the `[0, 1]` interval.
   - Score formula:
     $$\text{Score}_{\text{hybrid}} = \alpha \cdot \text{Norm}(\text{Score}_{\text{tfidf}}) + (1 - \alpha) \cdot \text{Norm}(\text{Score}_{\text{semantic}})$$
   - Development split tuning settled at $\alpha = 0.4$.

## 2. Evaluation Metrics Formulation
- **Precision@K**:
  $$\text{Precision@}K = \frac{|\text{Retrieved}_K \cap \text{Relevant}|}{K}$$
- **Recall@K**:
  $$\text{Recall@}K = \frac{|\text{Retrieved}_K \cap \text{Relevant}|}{|\text{Relevant}|}$$
- **F1@K**:
  $$\text{F1@}K = \frac{2 \cdot \text{Precision@}K \cdot \text{Recall@}K}{\text{Precision@}K + \text{Recall@}K}$$
- **Mean Reciprocal Rank (MRR)**:
  $$\text{MRR} = \frac{1}{|Q|} \sum_{q \in Q} \frac{1}{\text{rank}_q}$$
- **Normalized Discounted Cumulative Gain (nDCG@K)**:
  $$\text{DCG@}K = \sum_{i=1}^K \frac{2^{rel_i} - 1}{\log_2(i + 1)}, \quad \text{nDCG@}K = \frac{\text{DCG@}K}{\text{IDCG@}K}$$
