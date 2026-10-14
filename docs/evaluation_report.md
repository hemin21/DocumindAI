# Experimental Evaluation Report

## 1. Official Benchmark Results (NFCorpus Test Split)

Evaluation conducted on **323 test queries** across **3,633 indexed documents** using ground-truth relevance judgments from `qrels/test.tsv`.

| Metric | TF-IDF Baseline | Semantic (`all-MiniLM-L6-v2`) | Hybrid ($\alpha = 0.4$) | Relative Gain (Hybrid vs TF-IDF) |
| :--- | :--- | :--- | :--- | :--- |
| **Precision@5** | 0.2780 | 0.3015 | **0.3189** | **+14.7%** |
| **Recall@5** | 0.1125 | 0.1184 | **0.1364** | **+21.2%** |
| **F1@5** | 0.1116 | 0.1198 | **0.1329** | **+19.1%** |
| **MRR** | 0.4818 | 0.5080 | **0.5418** | **+12.5%** |
| **nDCG@10** | 0.2934 | 0.3162 | **0.3400** | **+15.9%** |
| **Mean Latency** | 17.5 ms | 14.5 ms | 35.7 ms | 2x latency overhead |
| **Median Latency** | 15.7 ms | 13.8 ms | 33.3 ms | - |
| **P95 Latency** | 28.1 ms | 20.5 ms | 48.6 ms | - |
| **Index Construction Time** | **3.88 sec** | 238.04 sec (~4 min) | Derived | - |

## 2. Hypothesis Verification
- **H1 (Semantic Advantage on Conceptual Wording)**: **Supported**. The dense semantic retriever improved nDCG@10 from 0.2934 to 0.3162 (+7.8%) and MRR from 0.4818 to 0.5080 (+5.4%), successfully matching queries with synonymic shifts.
- **H2 (TF-IDF Competitiveness on Literal Jargon)**: **Supported**. TF-IDF remained competitive (MRR 0.4818) and outperformed the semantic model on queries containing exact chemical terms, drug dosages, or explicit compound names.
- **H3 (Computational Cost Disparity)**: **Supported**. Indexing time for TF-IDF was 3.88s vs. 238.04s for the dense model (a ~61x computation multiplier).

## 3. Synergy in Hybrid Retrieval
The Hybrid model achieved the highest ranking quality across every evaluation metric, indicating that lexical precision and dense semantic awareness offer complementary strengths.
