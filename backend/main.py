import os
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from model_service import ModelService
from database import init_db, add_history_entry, get_history, clear_history, get_stats

# Global ML Service instance
model_service: Optional[ModelService] = None
service_startup_error: Optional[str] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_service, service_startup_error
    # Initialize SQLite database
    init_db()

    # Load ML artifacts once at startup
    try:
        model_service = ModelService()
        print(f"ML Model loaded successfully. Supported classes: {model_service.classes}")
    except Exception as e:
        service_startup_error = str(e)
        print(f"CRITICAL ERROR loading ML artifacts at startup: {service_startup_error}")

    yield
    print("Shutting down backend...")

app = FastAPI(
    title="MoodLens AI Emotion Classification API",
    version="1.2.0",
    description="Production REST API for text-based emotion prediction using TF-IDF and Logistic Regression",
    lifespan=lifespan
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class PredictRequest(BaseModel):
    text: str = Field(..., description="Text passage to analyze for emotional valence")

class PredictResponse(BaseModel):
    predicted_emotion: str
    confidence: float
    probabilities: Dict[str, float]
    cleaned_text: Optional[str] = None
    tokens_count: Optional[int] = None
    history_id: Optional[int] = None

class HistoryItem(BaseModel):
    id: int
    text: str
    predicted_emotion: str
    confidence: float
    probabilities: Dict[str, float]
    created_at: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    classes: List[str]
    artifacts_dir: str
    error: Optional[str] = None

class StatsResponse(BaseModel):
    total_records: int
    avg_confidence: float
    dominant_emotion: str
    dominant_count: int

# API Endpoints
@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Reports whether the service and ML model artifacts are loaded successfully."""
    if service_startup_error or not model_service or not model_service.is_loaded:
        return HealthResponse(
            status="error",
            model_loaded=False,
            classes=[],
            artifacts_dir=str(model_service.artifacts_dir if model_service else "unknown"),
            error=service_startup_error or (model_service.error_message if model_service else "Model not initialized")
        )

    return HealthResponse(
        status="healthy",
        model_loaded=True,
        classes=model_service.classes,
        artifacts_dir=str(model_service.artifacts_dir),
        error=None
    )

@app.post("/api/predict", response_model=PredictResponse, status_code=status.HTTP_200_OK)
def predict_emotion(payload: PredictRequest):
    """
    Accepts input text, applies trained preprocessing, transforms with TF-IDF,
    and returns predicted emotion and probability distribution across all 6 classes.
    Persists query record to SQLite history.
    """
    if not model_service or not model_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Emotion prediction service unavailable: {service_startup_error or 'Artifacts not loaded'}"
        )

    raw_text = payload.text.strip() if payload.text else ""
    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Input text cannot be empty. Please provide a valid sentence or thought to analyze."
        )

    try:
        result = model_service.predict(raw_text)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference computation error: {str(e)}"
        )

    # Persist in SQLite history
    try:
        history_record = add_history_entry(
            text=raw_text,
            predicted_emotion=result["predicted_emotion"],
            confidence=result["confidence"],
            probabilities=result["probabilities"]
        )
        history_id = history_record["id"]
    except Exception as e:
        # Do not fail inference if history write encounters an issue, but log it
        print(f"Warning: failed to record history: {e}")
        history_id = None

    return PredictResponse(
        predicted_emotion=result["predicted_emotion"],
        confidence=result["confidence"],
        probabilities=result["probabilities"],
        cleaned_text=result["cleaned_text"],
        tokens_count=result["tokens_count"],
        history_id=history_id
    )

@app.get("/api/history", response_model=List[HistoryItem])
def get_analysis_history(limit: int = 100, offset: int = 0):
    """Returns stored emotion analysis history in reverse chronological order."""
    try:
        return get_history(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve history: {str(e)}"
        )

@app.delete("/api/history")
def delete_analysis_history():
    """Clears all stored analysis history from SQLite."""
    try:
        deleted_count = clear_history()
        return {"status": "success", "message": f"Cleared {deleted_count} history records", "deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear history: {str(e)}"
        )

@app.get("/api/stats", response_model=StatsResponse)
def get_analysis_stats():
    """Returns aggregated summary metrics across all historical predictions."""
    try:
        stats = get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve stats: {str(e)}"
        )
