from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from .analyzer import StartupAnalyzer

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

analyzer = StartupAnalyzer()

class AnalyzeRequest(BaseModel):
    startup_name: str

class AnalyzeResponse(BaseModel):
    startup_name: str
    layer_id: int
    layer_name: str
    jp_name: str
    definition: str
    reasoning: str
    criteria_met: Dict[str, Any]
    criteria: Dict[str, Any]
    mode: str

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_startup(request: AnalyzeRequest):
    """
    Analyze a startup and determine its paradigm shift layer
    """
    if not request.startup_name or not request.startup_name.strip():
        raise HTTPException(status_code=400, detail="Startup name is required")
    
    try:
        result = analyzer.analyze_startup(request.startup_name.strip())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/layers")
async def get_layers():
    """
    Get all paradigm shift layers
    """
    from .paradigm_framework import PARADIGM_LAYERS
    return {"layers": PARADIGM_LAYERS}
