import os
import json
import shutil
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from ..schemas.schemas import (
    SearchRequest,
    SearchResponse,
    DatasetInfoResponse,
    ModelsResponse,
    ModelInfo,
    DocumentItem,
    CustomDocumentItem
)
from ..services.search_service import SearchService
from ..database.db import (
    get_recent_searches,
    add_custom_document,
    list_custom_documents,
    get_custom_chunks,
    delete_custom_document
)
from ..services.pdf_service import extract_text_from_pdf, chunk_text

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "results"
UPLOADS_DIR = DATA_DIR / "uploads"
MANIFEST_PATH = DATA_DIR / "processed" / "dataset_manifest.json"

@router.get("/health")
def health_check():
    service = SearchService.get_instance()
    return {
        "status": "healthy",
        "models_loaded": {
            "tfidf": service.tfidf is not None,
            "semantic": service.semantic is not None,
            "hybrid": service.hybrid is not None
        },
        "indexed_documents": len(service.tfidf.doc_ids) if service.tfidf else 0
    }

@router.get("/dataset/info", response_model=DatasetInfoResponse)
def get_dataset_info():
    if not MANIFEST_PATH.exists():
        raise HTTPException(status_code=404, detail="Dataset manifest not found. Run dataset preparation.")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@router.get("/models", response_model=ModelsResponse)
def get_models():
    return {
        "models": [
            {
                "id": "tfidf",
                "name": "TF-IDF Lexical Baseline",
                "type": "Lexical / Sparse Matrix",
                "description": "Standard term frequency-inverse document frequency model using unigrams & bigrams with cosine similarity."
            },
            {
                "id": "semantic",
                "name": "Sentence-Transformers (all-MiniLM-L6-v2)",
                "type": "Dense Semantic Embedding",
                "description": "384-dimensional dense semantic vectors with normalized cosine similarity to capture conceptual meaning."
            },
            {
                "id": "hybrid",
                "name": "Hybrid Retrieval (TF-IDF + Semantic)",
                "type": "Fused Hybrid",
                "description": "Linear combination (alpha=0.4 TF-IDF + 0.6 Semantic) with min-max normalized similarity scores."
            }
        ]
    }

@router.post("/search", response_model=SearchResponse)
def search_documents(request: SearchRequest):
    service = SearchService.get_instance()
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    result = service.search(query, model_type=request.model, top_k=request.top_k)
    return result

@router.get("/documents")
def list_documents(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    service = SearchService.get_instance()
    return service.list_documents(page=page, page_size=page_size)

@router.get("/documents/{document_id}", response_model=DocumentItem)
def get_document_details(document_id: str):
    service = SearchService.get_instance()
    doc = service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found.")
    return doc

@router.get("/evaluation/summary")
def get_evaluation_summary():
    summary_path = RESULTS_DIR / "metrics_summary.csv"
    if not summary_path.exists():
        raise HTTPException(status_code=404, detail="Evaluation has not been run yet.")
    df = pd.read_csv(summary_path)
    return df.to_dict(orient="records")

@router.get("/evaluation/config")
def get_evaluation_config():
    config_path = RESULTS_DIR / "experiment_config.json"
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="Experiment configuration not found.")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/evaluation/errors")
def get_evaluation_errors(limit: int = Query(50, ge=1, le=200)):
    error_path = RESULTS_DIR / "error_analysis.csv"
    if not error_path.exists():
        raise HTTPException(status_code=404, detail="Error analysis not found.")
    df = pd.read_csv(error_path)
    return df.head(limit).to_dict(orient="records")

@router.get("/history")
def get_history():
    return get_recent_searches(limit=20)

# PDF Upload & Custom Corpus Endpoints
@router.post("/custom/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = UPLOADS_DIR / file.filename
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract pages and chunk passages
    try:
        pages = extract_text_from_pdf(temp_path)
        if not pages:
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")
        chunks = chunk_text(pages, chunk_size_words=180, overlap_words=30)
        doc_id = add_custom_document(file.filename, len(pages), chunks)
        return {
            "status": "success",
            "document_id": doc_id,
            "filename": file.filename,
            "page_count": len(pages),
            "chunks_created": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@router.get("/custom/documents")
def get_custom_docs():
    return list_custom_documents()

@router.delete("/custom/documents/{document_id}")
def delete_custom_doc(document_id: str):
    delete_custom_document(document_id)
    return {"status": "deleted", "document_id": document_id}
