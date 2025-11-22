from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from .analyzer import StartupAnalyzer
from . import data_sources

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
    level: str
    definition: str
    reasoning: str
    criteria_met: Dict[str, Any]
    criteria: Dict[str, Any]
    mode: str
    data_sources: Optional[List[Dict[str, Any]]] = None

class ManualCompanyInput(BaseModel):
    name: str
    revenue: Optional[str] = None
    description: Optional[str] = None
    fiscal_year: Optional[str] = None
    industry: Optional[str] = None
    employees: Optional[str] = None

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
        result = await analyzer.analyze_startup(request.startup_name.strip())
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

@app.get("/api/search")
async def search_company(query: str):
    """
    Search for company across all data sources
    """
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query is required")
    
    results = await data_sources.search_all_sources(query.strip())
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }

@app.get("/api/edinet/search")
async def edinet_search(name: str):
    """
    Search EDINET specifically
    """
    result = await data_sources.search_edinet(name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Company not found in EDINET")

@app.get("/api/wikipedia/company")
async def wikipedia_search(name: str):
    """
    Search Wikipedia with validation
    """
    result = await data_sources.search_wikipedia(name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Company not found in Wikipedia or failed validation")

@app.post("/api/manual/company")
async def create_manual_company(company: ManualCompanyInput):
    """
    Create a manual company entry
    """
    company_data = data_sources.add_manual_company(company.dict())
    return company_data

@app.get("/api/manual/company/{company_id}")
async def get_manual_company(company_id: int):
    """
    Get a specific manual company entry
    """
    company = data_sources.get_manual_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get("/api/manual/companies")
async def list_manual_companies():
    """
    List all manual company entries
    """
    companies = data_sources.list_manual_companies()
    return {
        "companies": companies,
        "count": len(companies)
    }

@app.delete("/api/manual/company/{company_id}")
async def delete_manual_company(company_id: int):
    """
    Delete a manual company entry
    """
    deleted = data_sources.delete_manual_company(company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted", "company": deleted}
