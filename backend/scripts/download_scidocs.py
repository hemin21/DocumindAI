import os
import zipfile
import requests
import hashlib
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
SCIDOCS_URL = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scidocs.zip"
ZIP_PATH = RAW_DIR / "scidocs.zip"
EXTRACT_DIR = RAW_DIR / "scidocs"

def download_scidocs():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if EXTRACT_DIR.exists() and (EXTRACT_DIR / "corpus.jsonl").exists():
        print(f"[OK] SciDocs already extracted at: {EXTRACT_DIR}")
        return EXTRACT_DIR

    print(f"Downloading SciDocs from official BEIR benchmark: {SCIDOCS_URL}")
    response = requests.get(SCIDOCS_URL, stream=True, timeout=120)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))

    with open(ZIP_PATH, "wb") as f, tqdm(
        desc="Downloading scidocs.zip",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
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
    download_scidocs()
