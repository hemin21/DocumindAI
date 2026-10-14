import sqlite3
import uuid
from pathlib import Path
from typing import List, Dict, Optional, Tuple

DB_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "documind.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Search history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            model TEXT NOT NULL,
            top_k INTEGER NOT NULL,
            latency_ms REAL NOT NULL,
            result_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Custom uploaded documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_documents (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            page_count INTEGER NOT NULL,
            total_chunks INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Custom document chunks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_chunks (
            chunk_id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            FOREIGN KEY (document_id) REFERENCES custom_documents (id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def log_search(query: str, model: str, top_k: int, latency_ms: float, result_count: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO search_history (query, model, top_k, latency_ms, result_count)
        VALUES (?, ?, ?, ?, ?)
    """, (query, model, top_k, latency_ms, result_count))
    conn.commit()
    conn.close()

def get_recent_searches(limit: int = 20) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, query, model, top_k, latency_ms, result_count, created_at
        FROM search_history
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_custom_document(filename: str, page_count: int, chunks: List[Dict]) -> str:
    doc_id = str(uuid.uuid4())[:8]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO custom_documents (id, filename, page_count, total_chunks)
        VALUES (?, ?, ?, ?)
    """, (doc_id, filename, page_count, len(chunks)))

    for chunk in chunks:
        cid = f"{doc_id}-p{chunk['page_number']}-c{chunk['chunk_index']}"
        cursor.execute("""
            INSERT INTO custom_chunks (chunk_id, document_id, page_number, chunk_index, chunk_text)
            VALUES (?, ?, ?, ?, ?)
        """, (cid, doc_id, chunk['page_number'], chunk['chunk_index'], chunk['text']))

    conn.commit()
    conn.close()
    return doc_id

def list_custom_documents() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, page_count, total_chunks, uploaded_at
        FROM custom_documents
        ORDER BY uploaded_at DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_custom_chunks(document_id: Optional[str] = None) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    if document_id:
        cursor.execute("""
            SELECT c.chunk_id, c.document_id, c.page_number, c.chunk_index, c.chunk_text, d.filename
            FROM custom_chunks c
            JOIN custom_documents d ON c.document_id = d.id
            WHERE c.document_id = ?
            ORDER BY c.page_number, c.chunk_index
        """, (document_id,))
    else:
        cursor.execute("""
            SELECT c.chunk_id, c.document_id, c.page_number, c.chunk_index, c.chunk_text, d.filename
            FROM custom_chunks c
            JOIN custom_documents d ON c.document_id = d.id
            ORDER BY c.document_id, c.page_number, c.chunk_index
        """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def delete_custom_document(document_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM custom_chunks WHERE document_id = ?", (document_id,))
    cursor.execute("DELETE FROM custom_documents WHERE id = ?", (document_id,))
    conn.commit()
    conn.close()
    return True
