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
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        
    async def analyze_startup(self, startup_name: str) -> Dict[str, Any]:
        """
        Analyze a startup and determine its paradigm shift layer
        Uses data sources (EDINET, Wikipedia, manual) for revenue-based classification
        """
        # First, collect data from all sources
        collected_data = await data_sources.search_all_sources(startup_name)
        
        # Try data-driven analysis first
        if collected_data:
            result = self._data_driven_analysis(startup_name, collected_data)
            if result:
                result["data_sources"] = collected_data
                return result
        
        # Fall back to AI analysis if available
        if self.client:
            try:
                prompt = self._create_analysis_prompt(startup_name)
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert startup analyst specializing in evaluating companies against the Paradigm Shift 6-Layer Model. You provide detailed, fact-based analysis."},
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
    
    def _create_analysis_prompt(self, startup_name: str) -> str:
        """Create a detailed prompt for AI analysis"""
        layers_description = "\n\n".join([
            f"Layer {layer['id']}: {layer['name']} ({layer['jp_name']})\n"
            f"Definition: {layer['definition']}\n"
            f"Criteria: {json.dumps(layer['criteria'], ensure_ascii=False, indent=2)}"
            for layer in PARADIGM_LAYERS
        ])
        
        prompt = f"""Analyze the startup "{startup_name}" and determine which layer of the Paradigm Shift 6-Layer Model it belongs to.

Framework Layers:
{layers_description}

Instructions:
1. Research your knowledge about {startup_name} (business model, revenue scale, market impact, industry changes)
2. Evaluate against each layer's criteria
3. Determine the most appropriate layer (0-5)
4. Provide detailed reasoning citing specific facts

Response format (JSON):
{{
    "layer_id": <0-5>,
    "reasoning": "<detailed explanation with specific facts about revenue, market impact, structural changes, etc.>",
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
        
        if revenue_value is not None:
            # Layer 5: ARR 300億円〜
            if revenue_value >= 300:
                layer_id = 5
                met_criteria["revenue"] = f"売上規模: {revenue_str}"
            # Layer 4: ARR 100億円〜
            elif revenue_value >= 100:
                layer_id = 4
                met_criteria["revenue"] = f"売上規模: {revenue_str}"
            # Layer 3: ARR 20〜100億円
            elif revenue_value >= 20:
                layer_id = 3
                met_criteria["revenue"] = f"売上規模: {revenue_str}"
            # Layer 2: ARR 5〜20億円
            elif revenue_value >= 5:
                layer_id = 2
                met_criteria["revenue"] = f"売上規模: {revenue_str}"
            # Layer 1: ARR 1〜5億円
            elif revenue_value >= 1:
                layer_id = 1
                met_criteria["revenue"] = f"売上規模: {revenue_str}"
            # Layer 0: ARR < 1億円
            else:
                layer_id = 0
                met_criteria["revenue"] = f"売上規模: {revenue_str}"
        else:
            # No revenue data, use description-based heuristics
            if any(keyword in description.lower() for keyword in ['グローバル', 'worldwide', 'global', '世界']):
                layer_id = 3
                met_criteria["description_analysis"] = "グローバル展開の可能性"
            else:
                layer_id = 1
                met_criteria["description_analysis"] = "限定的な情報に基づく推定"
        
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
