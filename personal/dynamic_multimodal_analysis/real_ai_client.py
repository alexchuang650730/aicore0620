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
你是一位資深的業務分析專家和管理顧問，擁有豐富的保險業數位轉型經驗。請對以下需求進行深度專業分析：

需求描述：{requirement}

請提供詳細的專業分析，必須包含具體的量化數據和實用建議：

1. **複雜度評估**：
   - 技術複雜度（簡單/中等/複雜/高度複雜）
   - 業務複雜度分析
   - 實施難度評估

2. **時間預估**：
   - 詳細的時間框架（具體月數或年數）
   - 關鍵里程碑時間點
   - 風險因素和緩衝時間

3. **關鍵洞察**（至少5個具體洞察，包含量化數據）：
   - 行業標準和最佳實踐（具體百分比、數據）
   - 成本效益分析（具體金額、ROI）
   - 技術趨勢和應用案例（實際案例數據）
   - 人力資源影響（具體人數、成本）
   - 風險評估和機會分析（量化指標）

4. **專業建議**（至少5個具體建議，包含實施細節）：
   - 短期實施策略（1-2年，具體步驟）
   - 中期發展計劃（3-5年，投資預算）
   - 技術選型建議（具體產品、供應商）
   - 資源配置建議（人力、預算分配）
   - 風險緩解措施（具體方案）

5. **澄清問題**（至少5個關鍵問題）：
   - 業務規模和處理量（年處理件數、金額）
   - 現有系統和技術架構詳情
   - 預算範圍和投資期望
   - 人力資源現狀和配置
   - 合規要求和監管限制

6. **核心功能**（至少3個主要功能，包含技術規格）：
   - 基本功能描述（具體技術要求）
   - 高級功能特性（性能指標）
   - 創新功能建議（差異化優勢）

7. **量化分析**（必須包含具體數據）：
   - 人力需求估算（具體人數、職位）
   - 成本效益分析（投資金額、節約成本）
   - ROI預測（具體百分比、回收期）
   - 處理效率提升（時間節約、準確率）
"""

        # 添加上下文信息
        if context:
            if context.get('domain'):
                base_prompt += f"\n\n領域背景：{context['domain']}"
            if context.get('entities'):
                base_prompt += f"\n關鍵實體：{', '.join(context['entities'])}"
            if context.get('document_content'):
                base_prompt += f"\n\n相關文檔內容（前1000字符）：\n{context['document_content'][:1000]}..."

        base_prompt += """

請以JSON格式回應，包含以下字段：
{
  "complexity": "複雜度描述",
  "estimated_time": "時間預估",
  "key_insights": [
    "具體洞察1（包含量化數據）",
    "具體洞察2（包含量化數據）",
    "具體洞察3（包含量化數據）",
    "具體洞察4（包含量化數據）",
    "具體洞察5（包含量化數據）"
  ],
  "recommendations": [
    "具體建議1（包含實施細節和預算）",
    "具體建議2（包含實施細節和預算）",
    "具體建議3（包含實施細節和預算）",
    "具體建議4（包含實施細節和預算）",
    "具體建議5（包含實施細節和預算）"
  ],
  "questions": [
    "關鍵問題1（業務規模相關）",
    "關鍵問題2（技術架構相關）",
    "關鍵問題3（預算投資相關）",
    "關鍵問題4（人力資源相關）",
    "關鍵問題5（合規監管相關）"
  ],
  "key_features": [
    "核心功能1（包含技術規格）",
    "核心功能2（包含性能指標）",
    "核心功能3（包含創新特性）"
  ],
  "specific_analysis": {
    "quantitative_data": "具體的量化數據分析",
    "cost_benefit": "詳細的成本效益分析",
    "implementation_roadmap": "具體的實施路徑"
  },
  "confidence": 90
}

重要要求：
1. 所有洞察和建議必須包含具體的數據、百分比、金額等量化信息
2. 避免使用模糊的描述，提供可操作的具體建議
3. 基於真實的行業數據和最佳實踐
4. 確保分析的專業性和實用性
5. 不要使用占位符，所有內容都必須是實質性的專業分析"""
        
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
        
        # 確保關鍵字段都是列表格式
        normalized['key_insights'] = self._ensure_list(raw_result.get('key_insights', []), "關鍵洞察")
        normalized['recommendations'] = self._ensure_list(raw_result.get('recommendations', []), "專業建議")
        normalized['questions'] = self._ensure_list(raw_result.get('questions', []), "澄清問題")
        normalized['key_features'] = self._ensure_list(raw_result.get('key_features', []), "核心功能")
        
        # 保持其他字段
        normalized['specific_analysis'] = raw_result.get('specific_analysis', {})
        normalized['confidence'] = raw_result.get('confidence', 0.8)
        
        return normalized
    
    def _ensure_list(self, value, field_name: str) -> list:
        """確保字段是列表格式，並包含實際內容"""
        if isinstance(value, list) and len(value) > 0:
            # 過濾掉空值和占位符
            filtered = [item for item in value if item and not self._is_placeholder(str(item))]
            if filtered:
                return filtered
        elif isinstance(value, dict) and len(value) > 0:
            # 如果是字典，轉換為列表
            return [f"{k}: {v}" for k, v in value.items() if v and not self._is_placeholder(str(v))]
        
        # 如果沒有有效內容，返回默認提示
        return [f"需要進一步分析{field_name}"]
    
    def _is_placeholder(self, text: str) -> bool:
        """檢查是否為占位符"""
        placeholders = [
            "暫無", "待定", "需要確認", "placeholder", "示例", "example",
            "洞察1", "洞察2", "建議1", "建議2", "問題1", "問題2", "功能1", "功能2"
        ]
        return any(placeholder in text for placeholder in placeholders)
    
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

