import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Any

class CorpusLoader:
    """
    Loads documents, queries, and qrels preserving stable IDs and original structure.
    """
    def __init__(self, dataset_dir: Path):
        self.dataset_dir = Path(dataset_dir)
        self.corpus_file = self.dataset_dir / "corpus.jsonl"
        self.queries_file = self.dataset_dir / "queries.jsonl"
        self.qrels_dir = self.dataset_dir / "qrels"

    def load_corpus(self) -> Dict[str, Dict[str, Any]]:
        """Returns {doc_id: {'title': str, 'text': str, 'metadata': dict}}"""
        corpus = {}
        with open(self.corpus_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                corpus[item["_id"]] = {
                    "title": item.get("title", ""),
                    "text": item.get("text", ""),
                    "metadata": item.get("metadata", {})
                }
        return corpus

    def load_queries(self) -> Dict[str, str]:
        """Returns {query_id: query_text}"""
        queries = {}
        with open(self.queries_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                queries[item["_id"]] = item.get("text", "").strip()
        return queries

    def load_qrels(self, split: str = "test") -> Dict[str, Dict[str, int]]:
        """
        Returns {query_id: {doc_id: relevance_score}}
        """
        qrels_file = self.qrels_dir / f"{split}.tsv"
        qrels = {}
        with open(qrels_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            header = next(reader) # skip header
            for row in reader:
                if len(row) >= 3:
                    qid, doc_id, score = row[0], row[1], int(row[2])
                    if qid not in qrels:
                        qrels[qid] = {}
                    qrels[qid][doc_id] = score
        return qrels
