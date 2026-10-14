# Dataset Card: NFCorpus (BEIR Information-Retrieval Benchmark)

## 1. Dataset Summary
- **Dataset Name**: NFCorpus: A Full-Text English Information Retrieval Dataset for Medical Information Seeking
- **Benchmark**: BEIR (Benchmarking Information Retrieval)
- **Source URL**: `https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nfcorpus.zip`
- **Official Repository**: [BEIR Cellar](https://github.com/beir-cellar/beir)
- **Domain**: Evidence-based Medicine, Clinical Nutrition, Healthcare Literature

## 2. Dataset Characteristics & Measured Statistics
- **Total Documents in Corpus**: 3,633 medical research abstracts from PubMed/MEDLINE.
- **Average Document Length**: 233.77 words (Min: 17 words, Max: 1,481 words).
- **Empty Documents**: 0.
- **Total Queries**: 3,237 queries.
- **Average Query Length**: 3.32 words.
- **Relevance Judgments (qrels)**:
  - **Train Split**: 110,575 pairs (2,590 unique queries, 3,588 unique documents).
  - **Dev Split**: 11,385 pairs (324 unique queries, 3,119 unique documents).
  - **Test Split**: 12,334 pairs (323 unique queries, 3,128 unique documents).

## 3. Relevance Label Scale
- `0`: Non-relevant
- `1`: Marginally relevant (mentions related topic or condition)
- `2`: Relevant (directly addresses the query topic or clinical question)
- `3`: Highly relevant

## 4. Query Characteristics & Domain Bias
The queries in NFCorpus are extracted from user search logs on NutritionFacts.org. They vary from natural-language queries (e.g., *"Breast Cancer Cells Feed on Cholesterol"*, *"Treating Asthma With Plants vs. Pills"*) to concise keyword queries (e.g., *"statins and cancer"*). The vocabulary possesses a high density of medical terminology, drug names, and dietary factors.

## 5. Licensing and Attribution
- **License**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
- **Original Citation**:
  ```bibtex
  @inproceedings{bhowmik2016nfcorpus,
    title={NFCorpus: A Full-Text English Information Retrieval Dataset for Medical Information Seeking},
    author={Bhowmik, Rajen and de Vries, Arjen P},
    booktitle={Proceedings of the 39th International ACM SIGIR Conference on Research and Development in Information Retrieval},
    year={2016}
  }
  @inproceedings{thakur2021beir,
    title={BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models},
    author={Thakur, Nandan and Reimers, Nils and R{\"u}ckl{\'e}, Andreas and Srivastava, Abhishek and Gurevych, Iryna},
    booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
    year={2021}
  }
  ```
