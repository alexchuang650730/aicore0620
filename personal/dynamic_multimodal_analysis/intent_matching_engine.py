#!/usr/bin/env python3
"""
意圖匹配引擎
Intent Matching Engine

智能分析用戶輸入，匹配到正確的工作流和所需的適配器
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class IntentAnalysisResult:
    """意圖分析結果"""
    user_input: str
    primary_intent: str
    confidence: float
    matched_workflow: str
    required_capabilities: List[str]
    suggested_adapters: List[str]
    workflow_sequence: List[str]
    analysis_details: Dict[str, Any]

@dataclass
class IntentPattern:
    """意圖模式"""
    pattern_id: str
    keywords: List[str]
    regex_patterns: List[str]
    target_workflow: str
    required_capabilities: List[str]
    confidence_weight: float
    examples: List[str]

class IntentMatchingEngine:
    """
    意圖匹配引擎
    
    核心功能：
    1. 分析用戶自然語言輸入
    2. 識別開發意圖和需求
    3. 匹配到合適的工作流
    4. 推薦所需的適配器
    """
    
    def __init__(self, capability_registry):
        self.capability_registry = capability_registry
        self.intent_patterns: Dict[str, IntentPattern] = {}
        self.learning_history: List[Dict] = []
        
        # 初始化意圖模式
        self.initialize_intent_patterns()
    
    def initialize_intent_patterns(self):
        """初始化意圖識別模式"""
        
        patterns = [
            # 編碼開發意圖
            IntentPattern(
                pattern_id="coding_development",
                keywords=["開發", "建立", "製作", "寫", "編碼", "程式", "代碼", "實現", "創建"],
                regex_patterns=[
                    r"(開發|建立|製作|創建).*(遊戲|應用|網站|系統|程式)",
                    r"(寫|編寫).*(代碼|程式|腳本)",
                    r"(實現|完成).*(功能|需求|項目)"
                ],
                target_workflow="coding_workflow_mcp",
                required_capabilities=["代碼生成", "AI編程助手"],
                confidence_weight=1.0,
                examples=["開發貪吃蛇遊戲", "建立購物車應用", "製作天氣預報網站"]
            ),
            
            # 遊戲開發意圖
            IntentPattern(
                pattern_id="game_development", 
                keywords=["遊戲", "game", "貪吃蛇", "俄羅斯方塊", "拼圖", "射擊", "RPG"],
                regex_patterns=[
                    r".*(遊戲|game).*",
                    r".*(貪吃蛇|snake).*",
                    r".*(俄羅斯方塊|tetris).*"
                ],
                target_workflow="coding_workflow_mcp",
                required_capabilities=["遊戲開發", "Canvas繪圖", "鍵盤控制", "遊戲邏輯"],
                confidence_weight=1.2,
                examples=["開發貪吃蛇遊戲", "製作俄羅斯方塊", "建立射擊遊戲"]
            ),
            
            # Web 應用開發意圖
            IntentPattern(
                pattern_id="web_development",
                keywords=["網站", "web", "前端", "後端", "React", "Vue", "Angular", "HTML", "CSS"],
                regex_patterns=[
                    r".*(網站|website|web).*",
                    r".*(前端|frontend|後端|backend).*",
                    r".*(React|Vue|Angular).*"
                ],
                target_workflow="coding_workflow_mcp", 
                required_capabilities=["前端開發", "Web框架", "UI組件"],
                confidence_weight=1.0,
                examples=["建立 React 網站", "開發前端應用", "製作響應式網頁"]
            ),
            
            # 需求分析意圖
            IntentPattern(
                pattern_id="requirements_analysis",
                keywords=["需求", "分析", "規劃", "方案", "設計", "計劃"],
                regex_patterns=[
                    r".*(需求|requirement).*",
                    r".*(分析|analysis).*",
                    r".*(規劃|planning).*"
                ],
                target_workflow="requirements_analysis_mcp",
                required_capabilities=["需求分析", "技術方案生成"],
                confidence_weight=0.8,
                examples=["分析系統需求", "制定開發計劃", "設計技術方案"]
            ),
            
            # 架構設計意圖
            IntentPattern(
                pattern_id="architecture_design",
                keywords=["架構", "設計", "系統", "結構", "模式", "框架"],
                regex_patterns=[
                    r".*(架構|architecture).*",
                    r".*(設計|design).*",
                    r".*(系統|system).*"
                ],
                target_workflow="architecture_design_mcp",
                required_capabilities=["架構設計", "系統設計"],
                confidence_weight=0.8,
                examples=["設計系統架構", "規劃技術架構", "制定設計模式"]
            ),
            
            # 測試驗證意圖
            IntentPattern(
                pattern_id="testing_validation",
                keywords=["測試", "驗證", "檢查", "調試", "質量", "bug"],
                regex_patterns=[
                    r".*(測試|test).*",
                    r".*(驗證|validation).*",
                    r".*(調試|debug).*"
                ],
                target_workflow="developer_flow_mcp",
                required_capabilities=["自動化測試", "質量保障"],
                confidence_weight=0.7,
                examples=["進行代碼測試", "驗證功能正確性", "調試程序錯誤"]
            )
        ]
        
        # 註冊模式
        for pattern in patterns:
            self.intent_patterns[pattern.pattern_id] = pattern
            logger.info(f"🎯 註冊意圖模式: {pattern.pattern_id}")
    
    def analyze_intent(self, user_input: str) -> IntentAnalysisResult:
        """分析用戶意圖"""
        logger.info(f"🔍 分析用戶意圖: {user_input}")
        
        # 1. 模式匹配
        pattern_scores = self.calculate_pattern_scores(user_input)
        
        # 2. 選擇最佳匹配
        best_pattern = self.select_best_pattern(pattern_scores)
        
        # 3. 分析所需能力
        required_capabilities = self.analyze_required_capabilities(user_input, best_pattern)
        
        # 4. 推薦適配器
        suggested_adapters = self.recommend_adapters(required_capabilities, user_input)
        
        # 5. 生成工作流序列
        workflow_sequence = self.generate_workflow_sequence(best_pattern, user_input)
        
        # 6. 構建分析結果
        result = IntentAnalysisResult(
            user_input=user_input,
            primary_intent=best_pattern.pattern_id if best_pattern else "unknown",
            confidence=pattern_scores.get(best_pattern.pattern_id, 0.0) if best_pattern else 0.0,
            matched_workflow=best_pattern.target_workflow if best_pattern else "",
            required_capabilities=required_capabilities,
            suggested_adapters=suggested_adapters,
            workflow_sequence=workflow_sequence,
            analysis_details={
                "pattern_scores": pattern_scores,
                "best_pattern": best_pattern.pattern_id if best_pattern else None,
                "analysis_time": datetime.now().isoformat()
            }
        )
        
        # 記錄學習歷史
        self.record_analysis(result)
        
        return result
    
    def calculate_pattern_scores(self, user_input: str) -> Dict[str, float]:
        """計算各個模式的匹配分數"""
        scores = {}
        user_input_lower = user_input.lower()
        
        for pattern_id, pattern in self.intent_patterns.items():
            score = 0.0
            
            # 關鍵詞匹配
            keyword_matches = 0
            for keyword in pattern.keywords:
                if keyword.lower() in user_input_lower:
                    keyword_matches += 1
            
            if pattern.keywords:
                keyword_score = keyword_matches / len(pattern.keywords)
                score += keyword_score * 0.6
            
            # 正則表達式匹配
            regex_matches = 0
            for regex_pattern in pattern.regex_patterns:
                if re.search(regex_pattern, user_input, re.IGNORECASE):
                    regex_matches += 1
            
            if pattern.regex_patterns:
                regex_score = regex_matches / len(pattern.regex_patterns)
                score += regex_score * 0.4
            
            # 應用權重
            score *= pattern.confidence_weight
            
            scores[pattern_id] = score
        
        return scores
    
    def select_best_pattern(self, pattern_scores: Dict[str, float]) -> Optional[IntentPattern]:
        """選擇最佳匹配模式"""
        if not pattern_scores:
            return None
        
        best_pattern_id = max(pattern_scores, key=pattern_scores.get)
        best_score = pattern_scores[best_pattern_id]
        
        # 設置最低信心度閾值
        if best_score < 0.3:
            return None
        
        return self.intent_patterns[best_pattern_id]
    
    def analyze_required_capabilities(self, user_input: str, pattern: Optional[IntentPattern]) -> List[str]:
        """分析所需能力"""
        capabilities = []
        
        if pattern:
            capabilities.extend(pattern.required_capabilities)
        
        # 基於關鍵詞推斷額外能力
        user_input_lower = user_input.lower()
        
        capability_keywords = {
            "貪吃蛇": ["貪吃蛇遊戲邏輯", "Canvas繪圖", "鍵盤控制"],
            "react": ["React組件開發", "JSX語法", "狀態管理"],
            "遊戲": ["遊戲引擎", "碰撞檢測", "動畫效果"],
            "網站": ["HTML生成", "CSS樣式", "響應式設計"],
            "api": ["API設計", "後端開發", "數據庫操作"],
            "ui": ["用戶界面設計", "交互邏輯", "視覺效果"]
        }
        
        for keyword, caps in capability_keywords.items():
            if keyword in user_input_lower:
                capabilities.extend(caps)
        
        return list(set(capabilities))  # 去重
    
    def recommend_adapters(self, required_capabilities: List[str], user_input: str) -> List[str]:
        """推薦適配器"""
        adapters = []
        
        # 查找現有適配器
        for capability in required_capabilities:
            matching_mcps = self.capability_registry.find_mcps_by_capability(capability)
            for mcp in matching_mcps:
                if mcp in self.capability_registry.adapter_mcps:
                    adapters.append(mcp)
        
        # 分析缺失能力
        missing_capabilities = self.capability_registry.analyze_missing_capabilities(required_capabilities)
        
        # 如果有缺失能力，建議創建新適配器
        if missing_capabilities:
            suggestion = self.capability_registry.suggest_adapter_creation(missing_capabilities, user_input)
            if suggestion:
                adapters.append(suggestion["name"])
                logger.info(f"💡 建議創建適配器: {suggestion['name']} (缺失能力: {missing_capabilities})")
        
        return list(set(adapters))  # 去重
    
    def generate_workflow_sequence(self, pattern: Optional[IntentPattern], user_input: str) -> List[str]:
        """生成工作流序列"""
        if not pattern:
            return []
        
        # 基礎序列
        base_sequence = []
        
        # 根據意圖類型決定工作流序列
        if pattern.pattern_id in ["coding_development", "game_development", "web_development"]:
            base_sequence = [
                "requirements_analysis_mcp",  # 需求分析
                "architecture_design_mcp",    # 架構設計
                "coding_workflow_mcp",        # 編碼實現
                "developer_flow_mcp"          # 測試驗證
            ]
            
            # 如果是複雜項目，添加部署和監控
            if any(keyword in user_input.lower() for keyword in ["系統", "平台", "應用"]):
                base_sequence.extend([
                    "release_manager_mcp",      # 部署發布
                    "operations_workflow_mcp"   # 監控運維
                ])
        
        elif pattern.pattern_id == "requirements_analysis":
            base_sequence = ["requirements_analysis_mcp"]
        
        elif pattern.pattern_id == "architecture_design":
            base_sequence = ["architecture_design_mcp"]
        
        elif pattern.pattern_id == "testing_validation":
            base_sequence = ["developer_flow_mcp"]
        
        return base_sequence
    
    def record_analysis(self, result: IntentAnalysisResult):
        """記錄分析結果用於學習"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "user_input": result.user_input,
            "intent": result.primary_intent,
            "confidence": result.confidence,
            "workflow": result.matched_workflow,
            "capabilities": result.required_capabilities,
            "adapters": result.suggested_adapters
        }
        
        self.learning_history.append(record)
        
        # 保持歷史記錄在合理範圍內
        if len(self.learning_history) > 1000:
            self.learning_history = self.learning_history[-500:]
    
    def learn_from_feedback(self, user_input: str, actual_workflow: str, success: bool):
        """從用戶反饋中學習"""
        # 簡化版本：記錄反饋用於未來改進
        feedback_record = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "predicted_workflow": self.analyze_intent(user_input).matched_workflow,
            "actual_workflow": actual_workflow,
            "success": success
        }
        
        logger.info(f"📚 學習反饋: {user_input} → {actual_workflow} ({'成功' if success else '失敗'})")
    
    def get_intent_stats(self) -> Dict[str, Any]:
        """獲取意圖分析統計"""
        if not self.learning_history:
            return {"message": "暫無分析歷史"}
        
        # 統計各種意圖的頻率
        intent_counts = {}
        workflow_counts = {}
        
        for record in self.learning_history:
            intent = record["intent"]
            workflow = record["workflow"]
            
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
            workflow_counts[workflow] = workflow_counts.get(workflow, 0) + 1
        
        return {
            "total_analyses": len(self.learning_history),
            "intent_distribution": intent_counts,
            "workflow_distribution": workflow_counts,
            "avg_confidence": sum(r["confidence"] for r in self.learning_history) / len(self.learning_history),
            "registered_patterns": len(self.intent_patterns)
        }

# 測試和演示代碼
def test_intent_matching():
    """測試意圖匹配引擎"""
    from mcp_capability_registry import MCPCapabilityRegistry
    
    # 創建註冊中心和意圖引擎
    registry = MCPCapabilityRegistry()
    engine = IntentMatchingEngine(registry)
    
    print("🧪 測試意圖匹配引擎")
    
    # 測試用例
    test_cases = [
        "我想開發貪吃蛇遊戲",
        "建立一個 React 購物車應用",
        "製作天氣預報網站",
        "需要分析系統需求",
        "設計微服務架構",
        "進行代碼測試和調試",
        "部署應用到生產環境",
        "開發聊天機器人",
        "建立數據可視化儀表板"
    ]
    
    print("\n🎯 意圖分析測試:")
    for user_input in test_cases:
        result = engine.analyze_intent(user_input)
        
        print(f"\n輸入: '{user_input}'")
        print(f"  意圖: {result.primary_intent} (信心度: {result.confidence:.2f})")
        print(f"  工作流: {result.matched_workflow}")
        print(f"  所需能力: {result.required_capabilities[:3]}...")  # 只顯示前3個
        print(f"  推薦適配器: {result.suggested_adapters}")
        print(f"  工作流序列: {' → '.join(result.workflow_sequence)}")
    
    # 顯示統計信息
    stats = engine.get_intent_stats()
    print(f"\n📊 意圖分析統計:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_intent_matching()

