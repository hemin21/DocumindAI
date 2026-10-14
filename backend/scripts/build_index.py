import time
from pathlib import Path
from backend.app.data.loader import CorpusLoader
from backend.app.retrieval.tfidf import TFIDFRetriever
from backend.app.retrieval.semantic import SemanticRetriever

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
SCIDOCS_DIR = DATA_DIR / "raw" / "scidocs"
INDEX_DIR = DATA_DIR / "indexes"

def build_all_indexes():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    loader = CorpusLoader(SCIDOCS_DIR)
    
    print("Loading SciDocs AI / Computer Science documents...")
    corpus = loader.load_corpus()
    print(f"Loaded {len(corpus):,} AI documents.")

    # 1. Build and save TF-IDF index
    print("\n--- Building TF-IDF Index for AI Literature ---")
    t0 = time.time()
    tfidf = TFIDFRetriever(ngram_range=(1, 2), stop_words="english", max_features=60000)
    tfidf.fit_and_index(corpus)
    tfidf_time = time.time() - t0
    tfidf_path = INDEX_DIR / "tfidf_index.pkl"
    tfidf.save(tfidf_path)
    print(f"TF-IDF Index built in {tfidf_time:.2f} seconds. Saved to {tfidf_path}")

    # 2. Build and save Semantic Index
    print("\n--- Building Semantic Index (all-MiniLM-L6-v2) for AI Literature ---")
    t0 = time.time()
    semantic = SemanticRetriever(model_name="sentence-transformers/all-MiniLM-L6-v2")
    semantic.fit_and_index(corpus, batch_size=128)
    semantic_time = time.time() - t0
    semantic_path = INDEX_DIR / "semantic_index.pkl"
    semantic.save(semantic_path)
    print(f"Semantic Index built in {semantic_time:.2f} seconds. Saved to {semantic_path}")

    print("\n[SUCCESS] Both TF-IDF and Semantic indexes built and saved successfully for SciDocs AI dataset!")

if __name__ == "__main__":
    build_all_indexes()
