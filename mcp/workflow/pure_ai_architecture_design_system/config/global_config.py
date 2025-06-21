# -*- coding: utf-8 -*-
"""
架構設計系統全局配置
"""

class ArchitectureDesignConfig:
    """架構設計系統配置類"""
    
    # 服務端口配置
    ARCHITECTURE_ANALYSIS_PORT = 8304
    WORKFLOW_MCP_PORT = 8305
    ADMIN_UI_PORT = 5003
    
    # AI引擎配置
    AI_MODEL = "claude-3.5-sonnet"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1
    
    # 分析配置
    CONFIDENCE_THRESHOLD = 0.8
    MAX_ANALYSIS_TIME = 30
    RETRY_ATTEMPTS = 3
    
    # 系統配置
    DEBUG_MODE = False
    LOG_LEVEL = "INFO"
    CORS_ENABLED = True
    
    # 路徑配置
    BASE_PATH = "/aicore0620"
    PRODUCT_PATH = f"{BASE_PATH}/product/architecture_design"
    MCP_ADAPTER_PATH = f"{BASE_PATH}/mcp/adapter/architecture_analysis_mcp"
    MCP_WORKFLOW_PATH = f"{BASE_PATH}/mcp/workflow/architecture_design_workflow_mcp"
    ADMINBOARD_PATH = f"{BASE_PATH}/adminboard/architecture_design"
    
    @classmethod
    def get_config(cls):
        """獲取配置字典"""
        return {
            'ports': {
                'analysis': cls.ARCHITECTURE_ANALYSIS_PORT,
                'workflow': cls.WORKFLOW_MCP_PORT,
                'admin_ui': cls.ADMIN_UI_PORT
            },
            'ai': {
                'model': cls.AI_MODEL,
                'max_tokens': cls.MAX_TOKENS,
                'temperature': cls.TEMPERATURE
            },
            'analysis': {
                'confidence_threshold': cls.CONFIDENCE_THRESHOLD,
                'max_time': cls.MAX_ANALYSIS_TIME,
                'retry_attempts': cls.RETRY_ATTEMPTS
            },
            'system': {
                'debug': cls.DEBUG_MODE,
                'log_level': cls.LOG_LEVEL,
                'cors_enabled': cls.CORS_ENABLED
            },
            'paths': {
                'base': cls.BASE_PATH,
                'product': cls.PRODUCT_PATH,
                'mcp_adapter': cls.MCP_ADAPTER_PATH,
                'mcp_workflow': cls.MCP_WORKFLOW_PATH,
                'adminboard': cls.ADMINBOARD_PATH
            }
        }

