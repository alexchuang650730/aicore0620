#!/usr/bin/env python3
"""
真正的Claude API調用實現
基於參考代碼實現真實的API調用和深度分析
"""

import os
import json
import asyncio
import aiohttp
import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """模型配置"""
    model_id: str
    api_key: str
    base_url: str
    max_tokens: int
    temperature: float
    timeout: int

class RealClaudeClient:
    """真正的Claude API客戶端"""
    
    def __init__(self):
        # 從環境變量或配置文件獲取API密鑰
        self.api_key = os.getenv('ANTHROPIC_API_KEY', '')
        self.base_url = "https://api.anthropic.com/v1"
        
        # 如果沒有API密鑰，使用OpenRouter作為代理
        if not self.api_key:
            self.api_key = os.getenv('OPENROUTER_API_KEY', '')
            self.base_url = "https://openrouter.ai/api/v1"
        
        self.config = ModelConfig(
            model_id="anthropic/claude-3-sonnet-20240229",
            api_key=self.api_key,
            base_url=self.base_url,
            max_tokens=4000,
            temperature=0.7,
            timeout=60
        )
    
    async def analyze_requirement(self, requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """使用Claude進行需求分析"""
        
        if not self.config.api_key:
            return {"success": False, "error": "缺少API密鑰"}
        
        # 構建專業的分析提示詞
        prompt = self._build_analysis_prompt(requirement, context)
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://powerautomation.ai",
            "X-Title": "Dynamic Analysis Engine"
        }
        
        # 根據API提供商調整請求格式
        if "anthropic.com" in self.config.base_url:
            # 直接使用Anthropic API
            request_data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            endpoint = "/messages"
        else:
            # 使用OpenRouter代理
            request_data = {
                "model": self.config.model_id,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            }
            endpoint = "/chat/completions"
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.base_url}{endpoint}",
                    headers=headers,
                    json=request_data,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                ) as response:
                    
                    processing_time = time.time() - start_time
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # 根據API提供商解析回應
                        if "anthropic.com" in self.config.base_url:
                            content = result["content"][0]["text"]
                        else:
                            content = result["choices"][0]["message"]["content"]
                        
                        # 解析Claude的結構化回應
                        analysis_result = self._parse_claude_response(content)
                        
                        return {
                            "success": True,
                            "analysis": analysis_result,
                            "processing_time": processing_time,
                            "model_used": "claude_sonnet",
                            "raw_response": content
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Claude API錯誤 {response.status}: {error_text}")
                        return {
                            "success": False,
                            "error": f"API錯誤 {response.status}: {error_text}",
                            "processing_time": processing_time
                        }
                        
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Claude API調用異常: {str(e)}")
            return {
                "success": False,
                "error": f"請求異常: {str(e)}",
                "processing_time": processing_time
            }
    
    def _build_analysis_prompt(self, requirement: str, context: Dict[str, Any] = None) -> str:
        """構建專業的分析提示詞"""
        
        base_prompt = f"""
你是一位資深的業務分析專家，擅長深度分析複雜的業務需求。請對以下需求進行全面、專業的分析：

需求內容：
{requirement}

請提供以下結構化的分析結果（以JSON格式回應）：

{{
    "complexity": "複雜度評估（簡單/中等/複雜/高度複雜）",
    "estimated_time": "預估實施時間",
    "key_insights": [
        "關鍵洞察1",
        "關鍵洞察2",
        "關鍵洞察3"
    ],
    "detailed_analysis": {{
        "business_impact": "業務影響分析",
        "technical_requirements": "技術需求分析",
        "resource_requirements": "資源需求分析",
        "risk_assessment": "風險評估",
        "success_factors": "成功關鍵因素"
    }},
    "quantitative_analysis": {{
        "cost_estimate": "成本估算",
        "roi_projection": "投資回報預測",
        "timeline_breakdown": "時間線分解",
        "resource_allocation": "資源配置建議"
    }},
    "recommendations": [
        "具體建議1",
        "具體建議2",
        "具體建議3"
    ],
    "implementation_plan": {{
        "phase_1": "第一階段實施計劃",
        "phase_2": "第二階段實施計劃",
        "phase_3": "第三階段實施計劃"
    }},
    "questions": [
        "需要澄清的問題1",
        "需要澄清的問題2"
    ]
}}

請確保分析深入、專業，並提供具體可行的建議。
"""
        
        # 如果有上下文信息，添加到提示詞中
        if context:
            if context.get("domain"):
                base_prompt += f"\n\n領域背景：{context['domain']}"
            if context.get("entities"):
                base_prompt += f"\n\n關鍵實體：{context['entities']}"
            if context.get("document_content"):
                base_prompt += f"\n\n相關文檔內容摘要：{context['document_content'][:1000]}..."
        
        return base_prompt
    
    def _parse_claude_response(self, content: str) -> Dict[str, Any]:
        """解析Claude的回應"""
        
        try:
            # 嘗試直接解析JSON
            if content.strip().startswith('{'):
                return json.loads(content)
            
            # 如果不是純JSON，嘗試提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # 如果無法解析JSON，手動構建結構化結果
            return self._manual_parse_response(content)
            
        except Exception as e:
            logger.warning(f"解析Claude回應失敗: {e}")
            return self._manual_parse_response(content)
    
    def _manual_parse_response(self, content: str) -> Dict[str, Any]:
        """手動解析回應內容"""
        
        # 基本結構化解析
        lines = content.split('\n')
        
        analysis = {
            "complexity": "中等",
            "estimated_time": "需要進一步評估",
            "key_insights": [],
            "detailed_analysis": {
                "business_impact": "需要深入分析",
                "technical_requirements": "待確定",
                "resource_requirements": "待評估",
                "risk_assessment": "中等風險",
                "success_factors": "待識別"
            },
            "quantitative_analysis": {
                "cost_estimate": "待評估",
                "roi_projection": "待計算",
                "timeline_breakdown": "待制定",
                "resource_allocation": "待規劃"
            },
            "recommendations": [],
            "implementation_plan": {
                "phase_1": "需求分析和規劃",
                "phase_2": "系統設計和開發",
                "phase_3": "測試和部署"
            },
            "questions": [
                "需要更詳細的需求說明嗎？",
                "有特定的預算限制嗎？"
            ]
        }
        
        # 嘗試從內容中提取關鍵信息
        for line in lines:
            line = line.strip()
            if line:
                if any(keyword in line.lower() for keyword in ['複雜', 'complex']):
                    analysis["key_insights"].append(line)
                elif any(keyword in line.lower() for keyword in ['建議', 'recommend']):
                    analysis["recommendations"].append(line)
        
        # 確保列表不為空
        if not analysis["key_insights"]:
            analysis["key_insights"] = ["基於Claude分析的專業洞察"]
        if not analysis["recommendations"]:
            analysis["recommendations"] = ["建議進行更詳細的需求分析"]
        
        return analysis

# 全局Claude客戶端實例
claude_client = RealClaudeClient()

async def call_claude_api(requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """調用Claude API的便捷函數"""
    return await claude_client.analyze_requirement(requirement, context)

