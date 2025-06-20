#!/usr/bin/env python3
"""
真正的AI API客戶端
整合Gemini和Claude的真實API調用
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional

# 設置API密鑰 - 從環境變量讀取
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
KILO_API_KEY = os.getenv("KILO_API_KEY", "")

logger = logging.getLogger(__name__)

class RealAIClient:
    """真正的AI API客戶端"""
    
    def __init__(self):
        self.gemini_api_key = GEMINI_API_KEY
        self.kilo_api_key = KILO_API_KEY
        
    async def call_gemini_flash(self, requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """調用Gemini Flash進行需求分析"""
        try:
            import google.generativeai as genai
            
            # 配置API密鑰
            genai.configure(api_key=self.gemini_api_key)
            
            # 構建專業的分析提示
            prompt = self._build_analysis_prompt(requirement, context, "gemini")
            
            # 調用Gemini API
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            # 解析回應
            analysis_result = self._parse_gemini_response(response.text)
            
            logger.info("Gemini Flash分析成功")
            return {
                "success": True,
                "model_used": "gemini_flash",
                "analysis": analysis_result
            }
            
        except Exception as e:
            logger.error(f"Gemini Flash調用失敗: {e}")
            return {
                "success": False,
                "error": f"Gemini調用異常: {str(e)}"
            }
    
    async def call_claude_sonnet(self, requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """調用Claude Sonnet進行需求分析"""
        try:
            import anthropic
            
            # 使用KILO API密鑰
            client = anthropic.Anthropic(api_key=self.kilo_api_key)
            
            # 構建專業的分析提示
            prompt = self._build_analysis_prompt(requirement, context, "claude")
            
            # 調用Claude API
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 解析回應
            analysis_result = self._parse_claude_response(response.content[0].text)
            
            logger.info("Claude Sonnet分析成功")
            return {
                "success": True,
                "model_used": "claude_sonnet",
                "analysis": analysis_result
            }
            
        except Exception as e:
            logger.error(f"Claude Sonnet調用失敗: {e}")
            # 檢查是否是認證錯誤
            if "401" in str(e) or "authentication_error" in str(e):
                return {
                    "success": False,
                    "error": "Claude API認證失敗：API密鑰無效或已過期",
                    "warning": "⚠️ Claude API密鑰認證失敗，請檢查API密鑰是否正確"
                }
            else:
                return {
                    "success": False,
                    "error": f"Claude調用異常: {str(e)}",
                    "warning": f"⚠️ Claude API調用失敗: {str(e)}"
                }
    
    def _build_analysis_prompt(self, requirement: str, context: Dict[str, Any], model_type: str) -> str:
        """構建專業的分析提示"""
        
        base_prompt = f"""
你是一位資深的業務分析專家，請對以下需求進行深度專業分析：

需求描述：{requirement}

請提供詳細的分析，包括：

1. **複雜度評估**：
   - 技術複雜度（簡單/中等/複雜/高度複雜）
   - 業務複雜度分析
   - 實施難度評估

2. **時間預估**：
   - 詳細的時間框架
   - 關鍵里程碑
   - 風險因素

3. **關鍵洞察**：
   - 核心業務價值
   - 潛在挑戰和機會
   - 行業最佳實踐

4. **專業建議**：
   - 實施策略
   - 技術選型建議
   - 風險緩解措施

5. **量化分析**（如適用）：
   - 人力需求估算
   - 成本效益分析
   - ROI預測
"""

        # 添加上下文信息
        if context:
            if context.get('domain'):
                base_prompt += f"\n\n領域背景：{context['domain']}"
            if context.get('entities'):
                base_prompt += f"\n關鍵實體：{', '.join(context['entities'])}"
            if context.get('document_content'):
                base_prompt += f"\n\n相關文檔內容（前1000字符）：\n{context['document_content'][:1000]}..."

        base_prompt += "\n\n請以JSON格式回應，包含以下字段：complexity, estimated_time, key_insights, recommendations, specific_analysis, confidence"
        
        return base_prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """解析Gemini回應"""
        try:
            import json
            import re
            
            # 嘗試提取JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # 如果沒有JSON，解析文本
            return self._parse_text_response(response_text, "gemini")
            
        except Exception as e:
            logger.warning(f"Gemini回應解析失敗: {e}")
            return self._parse_text_response(response_text, "gemini")
    
    def _parse_claude_response(self, response_text: str) -> Dict[str, Any]:
        """解析Claude回應"""
        try:
            import json
            import re
            
            # 嘗試提取JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                raw_result = json.loads(json_match.group())
                # 標準化格式，確保前端能正確顯示
                return self._normalize_analysis_result(raw_result)
            
            # 如果沒有JSON，解析文本
            return self._parse_text_response(response_text, "claude")
            
        except Exception as e:
            logger.warning(f"Claude回應解析失敗: {e}")
            return self._parse_text_response(response_text, "claude")
    
    def _normalize_analysis_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """標準化分析結果格式，確保前端能正確顯示"""
        normalized = {}
        
        # 處理複雜度 - 轉換為字符串
        complexity = raw_result.get('complexity', '中等')
        if isinstance(complexity, dict):
            # 提取主要複雜度信息
            tech_complexity = complexity.get('technical_complexity', '中等')
            business_complexity = complexity.get('business_complexity', '中等')
            normalized['complexity'] = f"{tech_complexity} (技術) / {business_complexity} (業務)"
        else:
            normalized['complexity'] = str(complexity)
        
        # 處理預估時間 - 轉換為字符串
        estimated_time = raw_result.get('estimated_time', '需要進一步評估')
        if isinstance(estimated_time, dict):
            # 提取總時間
            total_duration = estimated_time.get('total_duration', '需要進一步評估')
            normalized['estimated_time'] = total_duration
        else:
            normalized['estimated_time'] = str(estimated_time)
        
        # 保持其他字段不變
        normalized['key_insights'] = raw_result.get('key_insights', [])
        normalized['recommendations'] = raw_result.get('recommendations', [])
        normalized['questions'] = raw_result.get('questions', [])
        normalized['specific_analysis'] = raw_result.get('specific_analysis', {})
        normalized['confidence'] = raw_result.get('confidence', 0.8)
        
        return normalized
    
    def _parse_text_response(self, text: str, model: str) -> Dict[str, Any]:
        """解析文本回應為結構化數據"""
        import re
        
        # 提取關鍵信息
        complexity_match = re.search(r'複雜度[：:]\s*([^\n]+)', text)
        time_match = re.search(r'時間[：:].*?([0-9]+.*?[週月年])', text)
        
        # 提取洞察（查找列表或段落）
        insights = []
        insight_patterns = [
            r'洞察[：:]\s*([^\n]+)',
            r'關鍵[：:]\s*([^\n]+)',
            r'核心[：:]\s*([^\n]+)'
        ]
        
        for pattern in insight_patterns:
            matches = re.findall(pattern, text)
            insights.extend(matches)
        
        # 提取建議
        recommendations = []
        rec_patterns = [
            r'建議[：:]\s*([^\n]+)',
            r'推薦[：:]\s*([^\n]+)',
            r'應該[：:]\s*([^\n]+)'
        ]
        
        for pattern in rec_patterns:
            matches = re.findall(pattern, text)
            recommendations.extend(matches)
        
        return {
            "complexity": complexity_match.group(1) if complexity_match else "中等",
            "estimated_time": time_match.group(1) if time_match else "需要進一步評估",
            "key_insights": insights[:5] if insights else [f"基於{model}的專業分析"],
            "recommendations": recommendations[:5] if recommendations else ["建議進行詳細需求澄清"],
            "specific_analysis": {
                "model_source": model,
                "analysis_method": "AI深度分析",
                "confidence": "85%"
            },
            "confidence": 85
        }

# 全局實例
real_ai_client = RealAIClient()

# 導出函數供動態分析引擎使用
async def call_gemini_api(requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """調用Gemini API"""
    return await real_ai_client.call_gemini_flash(requirement, context)

async def call_claude_api(requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """調用Claude API"""
    return await real_ai_client.call_claude_sonnet(requirement, context)

