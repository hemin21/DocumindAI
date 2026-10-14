# Error Analysis & Project Limitations

## 1. Categorization of Retrieval Failures (NFCorpus Test Split)

Out of the 323 evaluated test queries, 153 queries exhibited failure cases in top-5 rankings. Automated heuristic classification yielded the following distribution:

| Error Category | Case Count | Failure Mechanism | Observed Pattern |
| :--- | :--- | :--- | :--- |
| **High Ambiguity / Abstract Query** | 93 | Subtle clinical relationships not explicitly bridged by single-sentence query phrasing. | Complex queries such as general wellness advice where relevant PubMed abstracts describe deep biochemical pathways. |
| **Lexical Mismatch (Vocabulary Gap)** | 37 | Query uses layperson synonyms; TF-IDF fails because keywords don't match formal PubMed terminology. | "blood pressure diet" vs medical text discussing "angiotensin-converting enzyme inhibitors and sodium retention". |
| **Semantic Blur / Exact Term Underweighting** | 23 | Dense embedding averages token representations across 384 dimensions, diluting rare drug names or chemical compounds. | Explicit acronyms or rare botanical names (e.g., specific flavonoids) where TF-IDF exact matching excelled. |

## 2. Limitations of the Present System
1. **Bi-Encoder Information Bottleneck**: The dense model (`all-MiniLM-L6-v2`) compresses an entire 200+ word abstract into a single 384-dimensional vector. Fine-grained numerical values and conditional clauses are inevitably blurred.
2. **Domain Adaptation Gap**: `all-MiniLM-L6-v2` was trained on general web corpora, not fine-tuned on specialized biomedical ontologies (e.g., MeSH, UMLS).
3. **Linear Score Normalization in Hybrid Fusion**: Min-max normalization operates per-query, which can be sensitive to outlier candidates.

## 3. Grounded Future Research Directions
1. **Cross-Encoder Re-Ranking**: Implement a two-stage retrieval pipeline: Retrieve candidate documents using the fast Hybrid retriever (Top-100), followed by a cross-encoder model (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) scoring query-document pairs jointly to model fine-grained token-level cross-attention.
2. **Domain-Specific Pre-Trained Biomedical Encoders**: Evaluate `PubMedBERT` or `BioLinkBERT` dense encoders trained natively on PubMed literature.
3. **Reciprocal Rank Fusion (RRF)**: Implement rank-based fusion rather than min-max score fusion to make hybrid combination invariant to scale disparities.
