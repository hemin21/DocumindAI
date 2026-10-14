import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict

def extract_text_from_pdf(pdf_path: Path) -> List[Dict]:
    """
    Extracts text page-by-page from a PDF using PyMuPDF.
    Returns: [{'page_number': int, 'text': str}, ...]
    """
    doc = fitz.open(str(pdf_path))
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if text:
            pages.append({
                "page_number": page_num + 1,
                "text": text
            })
    doc.close()
    return pages

def chunk_text(pages: List[Dict], chunk_size_words: int = 200, overlap_words: int = 40) -> List[Dict]:
    """
    Splits page text into sliding-window passages with overlap, preserving page references.
    """
    chunks = []
    chunk_idx = 1
    for page in pages:
        words = page["text"].split()
        if not words:
            continue
        start = 0
        while start < len(words):
            end = min(start + chunk_size_words, len(words))
            passage = " ".join(words[start:end])
            chunks.append({
                "chunk_index": chunk_idx,
                "page_number": page["page_number"],
                "text": passage
            })
            chunk_idx += 1
            if end == len(words):
                break
            start += (chunk_size_words - overlap_words)
    return chunks
