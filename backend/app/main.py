from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .api.routes import router as api_router
from .database.db import init_db
from .services.search_service import SearchService

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"
FIGURES_DIR = RESULTS_DIR / "figures"

app = FastAPI(
    title="DocuMind AI API",
    description="Question-to-Document Similarity Based Intelligent Search System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    # Initialize SearchService singleton
    SearchService.get_instance()

# Mount figures directory as static files for visualization
if FIGURES_DIR.exists():
    app.mount("/static/figures", StaticFiles(directory=str(FIGURES_DIR)), name="figures")

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "app": "DocuMind AI",
        "tagline": "Ask naturally. Discover relevant documents intelligently.",
        "documentation": "/docs",
        "api_prefix": "/api"
    }
