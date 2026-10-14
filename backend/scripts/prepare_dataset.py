import json
import csv
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
SCIDOCS_DIR = DATA_DIR / "raw" / "scidocs"
MANIFEST_PATH = DATA_DIR / "processed" / "dataset_manifest.json"

def analyze_and_prepare_manifest():
    DATA_DIR.joinpath("processed").mkdir(parents=True, exist_ok=True)

    # 1. Inspect Corpus
    corpus_file = SCIDOCS_DIR / "corpus.jsonl"
    doc_count = 0
    empty_docs = 0
    doc_lens = []
    sample_doc_ids = []

    with open(corpus_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            doc_count += 1
            text = (data.get("title", "") + " " + data.get("text", "")).strip()
            if not text:
                empty_docs += 1
            words = text.split()
            doc_lens.append(len(words))
            if len(sample_doc_ids) < 5:
                sample_doc_ids.append((data["_id"], data.get("title", "")))

    # 2. Inspect Queries
    queries_file = SCIDOCS_DIR / "queries.jsonl"
    query_count = 0
    query_lens = []
    sample_queries = []

    with open(queries_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            query_count += 1
            q_text = data.get("text", "").strip()
            words = q_text.split()
            query_lens.append(len(words))
            if len(sample_queries) < 8:
                sample_queries.append([data["_id"], q_text])

    # 3. Inspect Test Qrels
    test_tsv = SCIDOCS_DIR / "qrels" / "test.tsv"
    q_ids = set()
    c_ids = set()
    grades = Counter()
    rel_count = 0

    with open(test_tsv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) >= 3:
                qid, cid, score = row[0], row[1], int(row[2])
                q_ids.add(qid)
                c_ids.add(cid)
                grades[score] += 1
                rel_count += 1

    manifest = {
        "dataset_name": "SciDocs (Scientific Documents & AI / Computer Science)",
        "benchmark": "BEIR (Benchmarking Information Retrieval)",
        "source_url": "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scidocs.zip",
        "domain": "Artificial Intelligence, Machine Learning, Deep Learning, NLP & Computer Science",
        "corpus_statistics": {
            "total_documents": doc_count,
            "empty_documents": empty_docs,
            "avg_document_word_length": round(sum(doc_lens) / max(len(doc_lens), 1), 2),
            "max_document_word_length": max(doc_lens) if doc_lens else 0,
            "min_document_word_length": min(doc_lens) if doc_lens else 0,
            "sample_document_ids": sample_doc_ids
        },
        "query_statistics": {
            "total_queries": query_count,
            "avg_query_word_length": round(sum(query_lens) / max(len(query_lens), 1), 2),
            "max_query_word_length": max(query_lens) if query_lens else 0,
            "min_query_word_length": min(query_lens) if query_lens else 0,
            "sample_queries": sample_queries
        },
        "relevance_splits": {
            "test": {
                "num_judgments": rel_count,
                "unique_queries": len(q_ids),
                "unique_documents": len(c_ids),
                "grade_distribution": dict(grades)
            }
        },
        "relevance_grades_legend": {
            "0": "Non-relevant",
            "1": "Relevant (Citing paper / Cocited / Topic match)"
        },
        "license": "CC BY-SA 4.0 / Research Use Only",
        "reference": "Cohan et al. (2020), SPECTER: Document-level Representation Learning using Citation-informed Transformers. Also BEIR: Thakur et al. (2021) NeurIPS."
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[OK] Manifest generated successfully at: {MANIFEST_PATH}")
    print(f"Total AI & CS Documents: {doc_count:,}")
    print(f"Total AI & CS Queries: {query_count:,}")
    print(f"Test Qrels Judgments: {rel_count:,}")
    return manifest

if __name__ == "__main__":
    analyze_and_prepare_manifest()
