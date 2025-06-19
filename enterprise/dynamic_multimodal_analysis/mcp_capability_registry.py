#!/usr/bin/env python3
"""
MCP 能力註冊和配置系統
MCP Capability Registration and Configuration System

管理 workflow MCP 和 adapter MCP 的能力註冊
"""

import json
import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class MCPCapability:
    """MCP 能力數據結構"""
    name: str
    description: str
    category: str  # 'workflow', 'adapter', 'tool'
    capabilities: List[str]
    specialties: List[str]
    port: Optional[int] = None
    endpoint: Optional[str] = None
    dependencies: List[str] = None
    auto_generated: bool = False
    created_time: datetime = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_time is None:
            self.created_time = datetime.now()

@dataclass
class WorkflowMCPConfig:
    """工作流 MCP 配置"""
    name: str
    port: int
    capabilities: List[str]
    adapters: List[str]
    description: str
    intent_keywords: List[str]  # 意圖匹配關鍵詞

@dataclass
class AdapterMCPConfig:
    """適配器 MCP 配置"""
    name: str
    capabilities: List[str]
    specialties: List[str]
    description: str
    auto_generated: bool = False
    source_code_path: Optional[str] = None

class MCPCapabilityRegistry:
    """MCP 能力註冊中心"""
    
    def __init__(self, config_path: str = "mcp_capabilities.yaml"):
        self.config_path = config_path
        self.workflow_mcps: Dict[str, WorkflowMCPConfig] = {}
        self.adapter_mcps: Dict[str, AdapterMCPConfig] = {}
        self.capability_index: Dict[str, List[str]] = {}  # 能力 -> MCP 列表
        
        # 載入預設配置
        self.load_default_configurations()
    
    def load_default_configurations(self):
        """載入預設的 MCP 配置"""
        
        # 六大工作流 MCP 配置
        workflow_configs = {
            "requirements_analysis_mcp": WorkflowMCPConfig(
                name="requirements_analysis_mcp",
                port=8090,
                capabilities=["需求分析", "技術方案生成", "業務理解", "AI理解業務需求"],
                adapters=["enhanced_workflow_mcp"],
                description="智能引擎 - AI理解業務需求，生成技術方案",
                intent_keywords=["需求", "分析", "規劃", "方案", "業務"]
            ),
            
            "architecture_design_mcp": WorkflowMCPConfig(
                name="architecture_design_mcp", 
                port=8091,
                capabilities=["架構設計", "系統設計", "最佳實踐推薦", "智能架構建議"],
                adapters=["enhanced_workflow_mcp", "directory_structure_mcp"],
                description="智能引擎 - 智能架構建議，最佳實踐推薦",
                intent_keywords=["架構", "設計", "系統", "結構", "模式"]
            ),
            
            "coding_workflow_mcp": WorkflowMCPConfig(
                name="coding_workflow_mcp",
                port=8092, 
                capabilities=["代碼生成", "AI編程助手", "智能代碼補全", "自動編程"],
                adapters=["kilocode_mcp", "github_mcp", "advanced_smartui"],
                description="KiloCode引擎 - AI編程助手，代碼自動生成，智能代碼補全",
                intent_keywords=["開發", "編碼", "程式", "代碼", "實現", "建立", "製作"]
            ),
            
            "developer_flow_mcp": WorkflowMCPConfig(
                name="developer_flow_mcp",
                port=8093,
                capabilities=["自動化測試", "質量保障", "智能介入協調", "測試生成"],
                adapters=["test_manage_mcp", "development_intervention_mcp"],
                description="模板測試生成引擎 - 自動化測試，質量保障，智能介入協調", 
                intent_keywords=["測試", "驗證", "質量", "檢查", "調試"]
            ),
            
            "release_manager_mcp": WorkflowMCPConfig(
                name="release_manager_mcp",
                port=8094,
                capabilities=["一鍵部署", "環境管理", "版本控制", "發布管理"],
                adapters=["deployment_mcp", "github_mcp"],
                description="Release Manager + 插件系統 - 一鍵部署，環境管理，版本控制",
                intent_keywords=["部署", "發布", "上線", "環境", "版本"]
            ),
            
            "operations_workflow_mcp": WorkflowMCPConfig(
                name="operations_workflow_mcp",
                port=8095,
                capabilities=["性能監控", "問題預警", "運維管理", "系統監控"],
                adapters=["monitoring_mcp", "enterprise_smartui_mcp"],
                description="AdminBoard - 性能監控，問題預警",
                intent_keywords=["監控", "運維", "性能", "預警", "管理"]
            )
        }
        
        # 適配器 MCP 配置
        adapter_configs = {
            "kilocode_mcp": AdapterMCPConfig(
                name="kilocode_mcp",
                capabilities=["JavaScript代碼生成", "React組件開發", "前端框架", "遊戲開發"],
                specialties=["前端開發", "互動應用", "遊戲邏輯", "UI組件", "Web應用"],
                description="KiloCode 代碼生成引擎"
            ),
            
            "advanced_smartui": AdapterMCPConfig(
                name="advanced_smartui", 
                capabilities=["智慧感知UI", "動態佈局", "語音控制", "智能界面"],
                specialties=["用戶界面", "交互設計", "智能感知", "自適應UI"],
                description="Advanced SmartUI 智慧感知界面"
            ),
            
            "github_mcp": AdapterMCPConfig(
                name="github_mcp",
                capabilities=["版本控制", "代碼管理", "協作開發", "Git操作"],
                specialties=["源碼管理", "團隊協作", "版本追蹤", "代碼審查"],
                description="GitHub 集成適配器"
            ),
            
            "enhanced_workflow_mcp": AdapterMCPConfig(
                name="enhanced_workflow_mcp",
                capabilities=["工作流增強", "流程優化", "智能協調"],
                specialties=["流程管理", "工作流優化", "智能調度"],
                description="增強工作流適配器"
            )
        }
        
        # 註冊配置
        for name, config in workflow_configs.items():
            self.register_workflow_mcp(config)
            
        for name, config in adapter_configs.items():
            self.register_adapter_mcp(config)
    
    def register_workflow_mcp(self, config: WorkflowMCPConfig):
        """註冊工作流 MCP"""
        self.workflow_mcps[config.name] = config
        
        # 更新能力索引
        for capability in config.capabilities:
            if capability not in self.capability_index:
                self.capability_index[capability] = []
            self.capability_index[capability].append(config.name)
        
        logger.info(f"📋 註冊工作流 MCP: {config.name} (端口 {config.port})")
    
    def register_adapter_mcp(self, config: AdapterMCPConfig):
        """註冊適配器 MCP"""
        self.adapter_mcps[config.name] = config
        
        # 更新能力索引
        for capability in config.capabilities:
            if capability not in self.capability_index:
                self.capability_index[capability] = []
            self.capability_index[capability].append(config.name)
        
        logger.info(f"🔧 註冊適配器 MCP: {config.name}")
    
    def find_mcps_by_capability(self, capability: str) -> List[str]:
        """根據能力查找 MCP"""
        return self.capability_index.get(capability, [])
    
    def find_workflow_by_intent(self, user_input: str) -> Optional[WorkflowMCPConfig]:
        """根據用戶輸入的意圖查找合適的工作流"""
        user_input_lower = user_input.lower()
        
        # 計算每個工作流的匹配分數
        scores = {}
        for name, config in self.workflow_mcps.items():
            score = 0
            for keyword in config.intent_keywords:
                if keyword in user_input_lower:
                    score += 1
            scores[name] = score
        
        # 返回分數最高的工作流
        if scores and max(scores.values()) > 0:
            best_workflow = max(scores, key=scores.get)
            return self.workflow_mcps[best_workflow]
        
        return None
    
    def get_adapters_for_workflow(self, workflow_name: str) -> List[AdapterMCPConfig]:
        """獲取工作流的適配器配置"""
        if workflow_name not in self.workflow_mcps:
            return []
        
        workflow_config = self.workflow_mcps[workflow_name]
        adapters = []
        
        for adapter_name in workflow_config.adapters:
            if adapter_name in self.adapter_mcps:
                adapters.append(self.adapter_mcps[adapter_name])
        
        return adapters
    
    def analyze_missing_capabilities(self, required_capabilities: List[str]) -> List[str]:
        """分析缺失的能力"""
        missing = []
        
        for capability in required_capabilities:
            if capability not in self.capability_index or not self.capability_index[capability]:
                missing.append(capability)
        
        return missing
    
    def suggest_adapter_creation(self, missing_capabilities: List[str], context: str) -> Dict[str, Any]:
        """建議創建新的適配器"""
        if not missing_capabilities:
            return {}
        
        # 分析上下文，生成適配器建議
        adapter_suggestion = {
            "name": self.generate_adapter_name(missing_capabilities, context),
            "capabilities": missing_capabilities,
            "specialties": self.infer_specialties(missing_capabilities, context),
            "description": f"自動生成的適配器，用於 {context}",
            "auto_generated": True,
            "creation_reason": f"缺失能力: {', '.join(missing_capabilities)}"
        }
        
        return adapter_suggestion
    
    def generate_adapter_name(self, capabilities: List[str], context: str) -> str:
        """生成適配器名稱"""
        # 簡化版本：基於上下文和能力生成名稱
        if "遊戲" in context or "game" in context.lower():
            return "game_development_adapter"
        elif "貪吃蛇" in context:
            return "snake_game_adapter"
        elif "React" in context:
            return "react_development_adapter"
        else:
            # 基於第一個能力生成
            if capabilities:
                base_name = capabilities[0].replace(" ", "_").lower()
                return f"{base_name}_adapter"
            return "custom_adapter"
    
    def infer_specialties(self, capabilities: List[str], context: str) -> List[str]:
        """推斷專業領域"""
        specialties = []
        
        # 基於能力推斷
        for capability in capabilities:
            if "遊戲" in capability:
                specialties.extend(["遊戲開發", "互動邏輯", "遊戲引擎"])
            elif "UI" in capability or "界面" in capability:
                specialties.extend(["用戶界面", "前端開發", "交互設計"])
            elif "代碼" in capability or "編程" in capability:
                specialties.extend(["代碼生成", "自動編程", "軟件開發"])
        
        # 基於上下文推斷
        if "貪吃蛇" in context:
            specialties.extend(["貪吃蛇遊戲", "Canvas繪圖", "鍵盤控制"])
        
        return list(set(specialties))  # 去重
    
    def save_configuration(self):
        """保存配置到文件"""
        config_data = {
            "workflow_mcps": {name: asdict(config) for name, config in self.workflow_mcps.items()},
            "adapter_mcps": {name: asdict(config) for name, config in self.adapter_mcps.items()},
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"💾 配置已保存到 {self.config_path}")
    
    def load_configuration(self):
        """從文件載入配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # 載入工作流 MCP
            for name, data in config_data.get("workflow_mcps", {}).items():
                config = WorkflowMCPConfig(**data)
                self.register_workflow_mcp(config)
            
            # 載入適配器 MCP  
            for name, data in config_data.get("adapter_mcps", {}).items():
                config = AdapterMCPConfig(**data)
                self.register_adapter_mcp(config)
            
            logger.info(f"📂 配置已從 {self.config_path} 載入")
            
        except FileNotFoundError:
            logger.info("配置文件不存在，使用預設配置")
        except Exception as e:
            logger.error(f"載入配置失敗: {e}")
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """獲取註冊中心統計信息"""
        return {
            "workflow_mcps_count": len(self.workflow_mcps),
            "adapter_mcps_count": len(self.adapter_mcps),
            "total_capabilities": len(self.capability_index),
            "auto_generated_adapters": len([a for a in self.adapter_mcps.values() if a.auto_generated]),
            "workflow_mcps": list(self.workflow_mcps.keys()),
            "adapter_mcps": list(self.adapter_mcps.keys())
        }

# 測試和演示代碼
def test_capability_registry():
    """測試能力註冊中心"""
    registry = MCPCapabilityRegistry()
    
    print("🧪 測試 MCP 能力註冊中心")
    
    # 測試意圖匹配
    test_inputs = [
        "我想開發貪吃蛇遊戲",
        "需要分析系統需求", 
        "幫我設計架構",
        "進行代碼測試",
        "部署到生產環境"
    ]
    
    print("\n🎯 意圖匹配測試:")
    for user_input in test_inputs:
        workflow = registry.find_workflow_by_intent(user_input)
        if workflow:
            print(f"  '{user_input}' → {workflow.name} (端口 {workflow.port})")
        else:
            print(f"  '{user_input}' → 未找到匹配的工作流")
    
    # 測試能力查找
    print("\n🔍 能力查找測試:")
    test_capabilities = ["代碼生成", "遊戲開發", "智慧感知UI"]
    for capability in test_capabilities:
        mcps = registry.find_mcps_by_capability(capability)
        print(f"  '{capability}' → {mcps}")
    
    # 測試缺失能力分析
    print("\n❓ 缺失能力分析:")
    required_caps = ["貪吃蛇遊戲邏輯", "Canvas繪圖", "鍵盤控制"]
    missing = registry.analyze_missing_capabilities(required_caps)
    print(f"  需要的能力: {required_caps}")
    print(f"  缺失的能力: {missing}")
    
    # 測試適配器建議
    if missing:
        suggestion = registry.suggest_adapter_creation(missing, "開發貪吃蛇遊戲")
        print(f"\n💡 適配器建議:")
        print(f"  名稱: {suggestion['name']}")
        print(f"  能力: {suggestion['capabilities']}")
        print(f"  專業領域: {suggestion['specialties']}")
    
    # 顯示統計信息
    stats = registry.get_registry_stats()
    print(f"\n📊 註冊中心統計:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_capability_registry()

