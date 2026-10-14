import re
import unicodedata
from typing import Optional

def normalize_text(text: Optional[str]) -> str:
    """
    Normalizes text while preserving domain terminology, hyphens, and scientific notation:
    1. Replaces None with empty string.
    2. NFKD Unicode normalization.
    3. Normalizes whitespace (multiple spaces, tabs, newlines -> single space).
    4. Strips leading/trailing whitespace.
    """
    if text is None:
        return ""
    # Unicode decomposition/normalization
    text = unicodedata.normalize("NFKD", text)
    # Replace non-breaking spaces and line separators
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def combine_title_and_text(title: Optional[str], text: Optional[str]) -> str:
    """
    Combines document title and body text into a coherent passage for indexing.
    """
    norm_title = normalize_text(title)
    norm_text = normalize_text(text)
    if norm_title and norm_text:
        return f"{norm_title} — {norm_text}"
    elif norm_title:
        return norm_title
    elif norm_text:
        return norm_text
    return ""
