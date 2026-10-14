import os
import zipfile
import requests
import json
import hashlib
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
NFCORPUS_URL = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nfcorpus.zip"
ZIP_PATH = RAW_DIR / "nfcorpus.zip"
EXTRACT_DIR = RAW_DIR / "nfcorpus"

def download_nfcorpus():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if EXTRACT_DIR.exists() and (EXTRACT_DIR / "corpus.jsonl").exists():
        print(f"[OK] NFCorpus already exists at: {EXTRACT_DIR}")
        return EXTRACT_DIR

    print(f"Downloading NFCorpus from official BEIR repository: {NFCORPUS_URL}")
    response = requests.get(NFCORPUS_URL, stream=True, timeout=60)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))

    with open(ZIP_PATH, "wb") as f, tqdm(
        desc="Downloading nfcorpus.zip",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    # Calculate SHA256
    hasher = hashlib.sha256()
    with open(ZIP_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    sha256 = hasher.hexdigest()
    print(f"[OK] Downloaded {ZIP_PATH} (SHA-256: {sha256})")

    print(f"Extracting {ZIP_PATH} to {RAW_DIR}...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(RAW_DIR)

    print(f"[OK] Extracted successfully to {EXTRACT_DIR}")
    return EXTRACT_DIR

if __name__ == "__main__":
    download_nfcorpus()
