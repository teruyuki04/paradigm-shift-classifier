"""
Startup analyzer using AI to evaluate against paradigm shift framework
"""
import os
from typing import Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv
from .paradigm_framework import PARADIGM_LAYERS
from .knowledge_base import get_startup_info, is_out_of_scope
from . import data_sources
import json

load_dotenv()

class StartupAnalyzer:
    def __init__(self):
        # Check for both OPENAI_API_KEY and OpenAI_API_KEY
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OpenAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        
    async def analyze_startup(self, startup_name: str) -> Dict[str, Any]:
        """
        Analyze a startup and determine its paradigm shift layer
        Uses data sources (EDINET, Wikipedia, manual) for revenue-based classification
        """
        # First, collect data from all sources
        collected_data = await data_sources.search_all_sources(startup_name)
        
        # Try data-driven analysis first (only if we have numeric revenue)
        if collected_data:
            result = self._data_driven_analysis(startup_name, collected_data)
            if result:
                result["data_sources"] = collected_data
                return result
        
        # Fall back to AI analysis if available
        if self.client:
            try:
                prompt = self._create_analysis_prompt(startup_name, collected_data)
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert startup analyst specializing in evaluating companies against the Paradigm Shift 6-Layer Model. You provide detailed, fact-based analysis using both quantitative (revenue) and qualitative (impact, behavior change, ecosystem) criteria."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                
                analysis_text = response.choices[0].message.content
                
                result = self._parse_analysis(analysis_text, startup_name)
                result["mode"] = "ai"
                result["data_sources"] = collected_data
                return result
                
            except Exception as e:
                print(f"Error in AI analysis: {e}")
        
        # Final fallback to knowledge base
        return self._fallback_analysis(startup_name, collected_data)
    
    def _create_analysis_prompt(self, startup_name: str, collected_data: List[Dict[str, Any]] = None) -> str:
        """Create a detailed prompt for AI analysis with collected data context"""
        layers_description = "\n\n".join([
            f"Layer {layer['id']}: {layer['name']} ({layer['jp_name']})\n"
            f"Definition: {layer['definition']}\n"
            f"Criteria: {json.dumps(layer['criteria'], ensure_ascii=False, indent=2)}"
            for layer in PARADIGM_LAYERS
        ])
        
        collected_info = ""
        if collected_data:
            collected_info = "\n\nCollected Data:\n"
            for source in collected_data:
                collected_info += f"- Source: {source.get('source', 'Unknown')}\n"
                if source.get('name'):
                    collected_info += f"  Name: {source['name']}\n"
                if source.get('revenue'):
                    collected_info += f"  Revenue: {source['revenue']}\n"
                if source.get('description'):
                    desc = source['description'][:300]
                    collected_info += f"  Description: {desc}...\n"
                collected_info += f"  Confidence: {source.get('confidence', 0)}\n\n"
        
        prompt = f"""Analyze the startup "{startup_name}" and determine which layer of the Paradigm Shift 6-Layer Model it belongs to.

Framework Layers (use these EXACTLY as defined):
{layers_description}

{collected_info}

Instructions:
1. Use the six layers EXACTLY as defined above (layer_id must be 0-5)
2. When revenue information is available and reliable, use it as PRIMARY evidence for classification
3. When revenue is unknown or uncertain, prioritize QUALITATIVE criteria:
   - Behavior change (行動変容): Has the company changed how people behave?
   - Ecosystem impact (エコシステム): Has it created a new industry or ecosystem?
   - Cultural impact (文化変容): Has it changed social norms or culture?
   - System integration (制度統合): Has it influenced regulations or government policy?
   - Category naming (カテゴリー名化): Has the company name become synonymous with the category?
4. For globally recognized companies with clear paradigm-shifting impact (e.g., transforming entire industries, changing cultural norms worldwide), consider higher layers even if revenue data is unavailable
5. Evaluate against each layer's criteria comprehensively
6. Provide detailed reasoning citing specific facts

Response format (JSON):
{{
    "layer_id": <0-5>,
    "reasoning": "<detailed explanation with specific facts about revenue (if available), market impact, structural changes, behavior change, ecosystem, cultural impact, etc.>",
    "criteria_met": {{
        "<criterion1>": "<explanation>",
        "<criterion2>": "<explanation>"
    }}
}}

Be specific and fact-based. If the startup is not well-known or you lack information, classify it as Layer 0 (Pre-Shift) and explain why."""
        
        return prompt
    
    def _parse_analysis(self, analysis_text: str, startup_name: str) -> Dict[str, Any]:
        """Parse AI response and structure the result"""
        try:
            start_idx = analysis_text.find('{')
            end_idx = analysis_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = analysis_text[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                layer_id = parsed.get("layer_id", 0)
                layer_id = max(0, min(5, layer_id))
                
                layer_info = PARADIGM_LAYERS[layer_id]
                
                return {
                    "startup_name": startup_name,
                    "layer_id": layer_id,
                    "layer_name": layer_info["name"],
                    "jp_name": layer_info["jp_name"],
                    "definition": layer_info["definition"],
                    "reasoning": parsed.get("reasoning", ""),
                    "criteria_met": parsed.get("criteria_met", {}),
                    "criteria": layer_info["criteria"]
                }
        except Exception as e:
            print(f"Error parsing analysis: {e}")
        
        return self._fallback_analysis(startup_name)
    
    def _data_driven_analysis(self, startup_name: str, collected_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze startup based on collected data from multiple sources
        Uses revenue thresholds to classify into paradigm shift layers
        """
        if not collected_data:
            return None
        
        # Get the best data source (prioritize Manual > EDINET > Wikipedia)
        best_source = max(collected_data, key=lambda x: x.get("confidence", 0))
        
        revenue_str = best_source.get("revenue")
        description = best_source.get("description", "")
        
        # Extract revenue value
        revenue_value = data_sources.extract_revenue_value(revenue_str)
        
        # Classify based on revenue thresholds (in 億円)
        layer_id = 0
        met_criteria = {}
        
        if revenue_value is None:
            # No numeric revenue data available - cannot classify via data-driven method
            # Return None to fall through to AI analysis
            return None
        
        # Classify based on revenue thresholds (in 億円)
        # Layer 5: 1200億円〜 (Paradigm Shift)
        if revenue_value >= 1200:
            layer_id = 5
            met_criteria["revenue"] = f"売上規模: {revenue_str}"
        # Layer 4: 500〜1200億円 (Systemic Shift)
        elif revenue_value >= 500:
            layer_id = 4
            met_criteria["revenue"] = f"売上規模: {revenue_str}"
        # Layer 3: 150〜500億円 (Structural Shift)
        elif revenue_value >= 150:
            layer_id = 3
            met_criteria["revenue"] = f"売上規模: {revenue_str}"
        # Layer 2: 50〜150億円 (Emerging Shift)
        elif revenue_value >= 50:
            layer_id = 2
            met_criteria["revenue"] = f"売上規模: {revenue_str}"
        # Layer 1: 20〜50億円 (Minimal Shift)
        elif revenue_value >= 20:
            layer_id = 1
            met_criteria["revenue"] = f"売上規模: {revenue_str}"
        # Layer 0: <20億円 (Pre-Shift)
        else:
            layer_id = 0
            met_criteria["revenue"] = f"売上規模: {revenue_str}"
        
        layer_info = PARADIGM_LAYERS[layer_id]
        
        # Build reasoning
        reasoning_parts = []
        reasoning_parts.append(f"{startup_name}について、{len(collected_data)}件のデータソースから情報を収集しました。")
        
        if revenue_str:
            reasoning_parts.append(f"売上規模は{revenue_str}です。")
            if revenue_value:
                reasoning_parts.append(f"この売上規模から、{layer_info['jp_name']}（{layer_info['name']}）に分類されます。")
        
        if description:
            reasoning_parts.append(f"事業概要: {description[:200]}...")
        
        reasoning_parts.append("注意: この分析は収集した限られた情報に基づいています。より詳細な評価には追加調査が必要です。")
        
        return {
            "startup_name": startup_name,
            "layer_id": layer_id,
            "layer_name": layer_info["name"],
            "jp_name": layer_info["jp_name"],
            "level": layer_info["level"],
            "definition": layer_info["definition"],
            "reasoning": " ".join(reasoning_parts),
            "criteria_met": met_criteria,
            "criteria": layer_info["criteria"],
            "mode": "data_driven"
        }
    
    def _fallback_analysis(self, startup_name: str, collected_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fallback analysis using curated knowledge base"""
        if is_out_of_scope(startup_name):
            layer_info = PARADIGM_LAYERS[0]
            return {
                "startup_name": startup_name,
                "layer_id": 0,
                "layer_name": layer_info["name"],
                "jp_name": layer_info["jp_name"],
                "level": layer_info["level"],
                "definition": layer_info["definition"],
                "reasoning": f"対象外: 本フレームワークは1990年以降創業のスタートアップのみを対象としています。{startup_name}は1990年以前に創業された企業のため、このフレームワークでは評価できません。",
                "criteria_met": {},
                "criteria": layer_info["criteria"],
                "mode": "rule_based",
                "data_sources": collected_data or []
            }
        
        startup_info = get_startup_info(startup_name)
        
        if startup_info:
            layer_id = startup_info["layer_id"]
            layer_info = PARADIGM_LAYERS[layer_id]
            
            return {
                "startup_name": startup_name,
                "layer_id": layer_id,
                "layer_name": layer_info["name"],
                "jp_name": layer_info["jp_name"],
                "level": layer_info["level"],
                "definition": layer_info["definition"],
                "reasoning": startup_info["reasoning"],
                "criteria_met": startup_info["criteria_met"],
                "criteria": layer_info["criteria"],
                "mode": "rule_based",
                "data_sources": collected_data or []
            }
        
        layer_info = PARADIGM_LAYERS[0]
        
        return {
            "startup_name": startup_name,
            "layer_id": 0,
            "layer_name": layer_info["name"],
            "jp_name": layer_info["jp_name"],
            "level": layer_info["level"],
            "definition": layer_info["definition"],
            "reasoning": f"{startup_name}の情報が知識ベースにありません。より正確な分析を行うには、OpenAI APIキーを設定してAI分析モードを有効にしてください。",
            "criteria_met": {},
            "criteria": layer_info["criteria"],
            "mode": "rule_based",
            "data_sources": collected_data or []
        }
