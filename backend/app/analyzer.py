"""
Startup analyzer using AI to evaluate against paradigm shift framework
"""
import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from .paradigm_framework import PARADIGM_LAYERS
from .knowledge_base import get_startup_info, is_out_of_scope
import json

load_dotenv()

class StartupAnalyzer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        
    def analyze_startup(self, startup_name: str) -> Dict[str, Any]:
        """
        Analyze a startup and determine its paradigm shift layer
        """
        if not self.client:
            return self._fallback_analysis(startup_name)
        
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
            return result
            
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return self._fallback_analysis(startup_name)
    
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
    
    def _fallback_analysis(self, startup_name: str) -> Dict[str, Any]:
        """Fallback analysis using curated knowledge base"""
        if is_out_of_scope(startup_name):
            layer_info = PARADIGM_LAYERS[0]
            return {
                "startup_name": startup_name,
                "layer_id": 0,
                "layer_name": layer_info["name"],
                "jp_name": layer_info["jp_name"],
                "definition": layer_info["definition"],
                "reasoning": f"対象外: 本フレームワークは1990年以降創業のスタートアップのみを対象としています。{startup_name}は1990年以前に創業された企業のため、このフレームワークでは評価できません。",
                "criteria_met": {},
                "criteria": layer_info["criteria"],
                "mode": "rule_based"
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
                "definition": layer_info["definition"],
                "reasoning": startup_info["reasoning"],
                "criteria_met": startup_info["criteria_met"],
                "criteria": layer_info["criteria"],
                "mode": "rule_based"
            }
        
        layer_info = PARADIGM_LAYERS[0]
        
        return {
            "startup_name": startup_name,
            "layer_id": 0,
            "layer_name": layer_info["name"],
            "jp_name": layer_info["jp_name"],
            "definition": layer_info["definition"],
            "reasoning": f"{startup_name}の情報が知識ベースにありません。より正確な分析を行うには、OpenAI APIキーを設定してAI分析モードを有効にしてください。",
            "criteria_met": {},
            "criteria": layer_info["criteria"],
            "mode": "rule_based"
        }
