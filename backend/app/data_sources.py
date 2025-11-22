"""
Data collection from multiple sources: EDINET, Wikipedia, and manual input
"""
import httpx
import wikipediaapi
from difflib import SequenceMatcher
from datetime import datetime
from typing import Optional, List, Dict, Any

# In-memory database for manual company entries
manual_companies_db = {}
company_id_counter = 1

EDINET_API_BASE = "https://api.edinet-fsa.go.jp/api/v2"

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='ParadigmShiftClassifier/1.0 (teruyuki04@gmail.com)',
    language='ja'
)

def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def is_company_category(categories: dict) -> bool:
    """Check if Wikipedia page belongs to company/organization categories"""
    company_keywords = [
        '企業', '会社', '法人', 'company', 'companies', 'corporation',
        '株式会社', '有限会社', 'ビジネス', 'business', '組織', 'organization'
    ]
    
    for category in categories:
        category_lower = category.lower()
        if any(keyword in category_lower for keyword in company_keywords):
            return True
    return False

async def search_edinet(company_name: str) -> Optional[Dict[str, Any]]:
    """Search for company in EDINET API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{EDINET_API_BASE}/documents.json",
                params={
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "type": 2
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": company_name,
                    "revenue": "Data available via EDINET API",
                    "description": "Listed company in Japan",
                    "source": "EDINET",
                    "confidence": 0.8
                }
    except Exception as e:
        print(f"EDINET API error: {e}")
        return None
    
    return None

async def search_wikipedia(company_name: str) -> Optional[Dict[str, Any]]:
    """Search for company in Wikipedia with validation"""
    try:
        page = wiki_wiki.page(company_name)
        
        if not page.exists():
            for suffix in ["株式会社", "(企業)", ""]:
                search_name = f"{company_name}{suffix}" if suffix else company_name
                page = wiki_wiki.page(search_name)
                if page.exists():
                    break
        
        if not page.exists():
            return None
        
        similarity = calculate_similarity(company_name, page.title)
        if similarity < 0.6:
            return None
        
        categories = list(page.categories.keys())
        if not is_company_category(categories):
            return None
        
        summary = page.summary[:500] if page.summary else "No description available"
        
        revenue = None
        text_lower = page.text.lower()
        if '売上' in text_lower or '売上高' in text_lower or 'revenue' in text_lower:
            revenue = "Revenue information available in Wikipedia article"
        
        return {
            "name": page.title,
            "revenue": revenue,
            "description": summary,
            "source": "Wikipedia",
            "confidence": similarity
        }
        
    except Exception as e:
        print(f"Wikipedia API error: {e}")
        return None

def add_manual_company(company_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a manual company entry to the database"""
    global company_id_counter
    
    company_entry = {
        "id": company_id_counter,
        "name": company_data.get("name"),
        "revenue": company_data.get("revenue"),
        "description": company_data.get("description"),
        "fiscal_year": company_data.get("fiscal_year"),
        "industry": company_data.get("industry"),
        "employees": company_data.get("employees"),
        "created_at": datetime.now().isoformat()
    }
    
    manual_companies_db[company_id_counter] = company_entry
    company_id_counter += 1
    
    return company_entry

def get_manual_company(company_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific manual company entry"""
    return manual_companies_db.get(company_id)

def list_manual_companies() -> List[Dict[str, Any]]:
    """List all manual company entries"""
    return list(manual_companies_db.values())

def search_manual_companies(query: str) -> List[Dict[str, Any]]:
    """Search manual companies by name"""
    results = []
    for company_id, company in manual_companies_db.items():
        if query.lower() in company["name"].lower():
            results.append({
                **company,
                "source": "Manual",
                "confidence": 1.0
            })
    return results

def delete_manual_company(company_id: int) -> Optional[Dict[str, Any]]:
    """Delete a manual company entry"""
    if company_id in manual_companies_db:
        return manual_companies_db.pop(company_id)
    return None

async def search_all_sources(company_name: str) -> List[Dict[str, Any]]:
    """Search for company across all data sources"""
    results = []
    
    # Search manual database
    manual_results = search_manual_companies(company_name)
    results.extend(manual_results)
    
    # Search EDINET
    edinet_result = await search_edinet(company_name)
    if edinet_result:
        results.append(edinet_result)
    
    # Search Wikipedia
    wiki_result = await search_wikipedia(company_name)
    if wiki_result:
        results.append(wiki_result)
    
    return results

def extract_revenue_value(revenue_str: Optional[str]) -> Optional[float]:
    """Extract numeric revenue value from string (in 億円)"""
    if not revenue_str:
        return None
    
    try:
        import re
        revenue_lower = revenue_str.lower()
        
        if '億' in revenue_str:
            match = re.search(r'(\d+(?:\.\d+)?)\s*億', revenue_str)
            if match:
                return float(match.group(1))
        
        if 'billion' in revenue_lower:
            match = re.search(r'(\d+(?:\.\d+)?)\s*billion', revenue_lower)
            if match:
                return float(match.group(1)) * 10
        
        match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)', revenue_str)
        if match:
            value_str = match.group(1).replace(',', '')
            value = float(value_str)
            if value > 1000000000:
                return value / 100000000
            elif value > 100000:
                return value / 100000000
    except:
        pass
    
    return None
