from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Natural language search query")
    model: str = Field("semantic", description="Model identifier: tfidf, semantic, or hybrid")
    top_k: int = Field(10, ge=1, le=50, description="Number of results to retrieve")

class SearchResultItem(BaseModel):
    rank: int
    doc_id: str
    score: float
    title: str
    snippet: str
    metadata: Dict[str, Any] = {}
    tfidf_raw: Optional[float] = None
    semantic_raw: Optional[float] = None

class SearchResponse(BaseModel):
    query: str
    model: str
    top_k: int
    latency_ms: float
    total_results: int
    direct_answer: Optional[str] = None
    results: List[SearchResultItem]

class DocumentItem(BaseModel):
    doc_id: str
    title: str
    text: str
    metadata: Dict[str, Any] = {}

class CustomDocumentItem(BaseModel):
    id: str
    filename: str
    page_count: int
    total_chunks: int
    uploaded_at: str

class DatasetInfoResponse(BaseModel):
    dataset_name: str
    benchmark: str
    source_url: str
    domain: str
    corpus_statistics: Dict[str, Any]
    query_statistics: Dict[str, Any]
    relevance_splits: Dict[str, Any]
    license: str
    reference: str

class ModelInfo(BaseModel):
    id: str
    name: str
    type: str
    description: str

class ModelsResponse(BaseModel):
    models: List[ModelInfo]
