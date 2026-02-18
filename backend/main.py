from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
import uvicorn
from contextlib import asynccontextmanager

from rag import RAGPipeline
from compare import ComparisonEngine

# Load env vars
load_dotenv()

# App State
rag_pipeline = None
comparison_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_pipeline, comparison_engine
    try:
        rag_pipeline = RAGPipeline()
        comparison_engine = ComparisonEngine(rag_pipeline)
        print("RAG Pipeline + Comparison Engine initialized.")
    except Exception as e:
        print(f"Failed to initialize: {e}")
    yield

app = FastAPI(title="CryptoGuide AI API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class QueryRequest(BaseModel):
    question: str
    protocol: str = "aave"

class CompareRequest(BaseModel):
    question: str
    protocols: List[str] = ["aave", "compound"]

class Source(BaseModel):
    id: int
    document: Optional[str] = None
    page: Optional[int] = None
    text: str
    protocol: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    metadata: Dict[str, Any] = {}

class CompareResponse(BaseModel):
    answer: str
    protocols: List[str]
    sources: List[Source]
    metadata: Dict[str, Any] = {}

# --- Endpoints ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "pipeline_ready": rag_pipeline is not None}

@app.post("/api/query", response_model=QueryResponse)
async def query_protocol(request: QueryRequest):
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="RAG Pipeline not initialized")
    
    try:
        result = rag_pipeline.generate_answer(request.question, request.protocol)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            metadata={"model": "claude-3-haiku-20240307"}
        )
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare", response_model=CompareResponse)
async def compare_protocols(request: CompareRequest):
    if not comparison_engine:
        raise HTTPException(status_code=503, detail="Comparison Engine not initialized")
    
    if len(request.protocols) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 protocols to compare")
    
    try:
        result = comparison_engine.compare_protocols(request.question, request.protocols)
        return CompareResponse(
            answer=result["answer"],
            protocols=result["protocols"],
            sources=result["sources"],
            metadata={"model": "claude-3-haiku-20240307"}
        )
    except Exception as e:
        print(f"Error processing comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
