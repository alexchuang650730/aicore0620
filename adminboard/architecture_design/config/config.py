# -*- coding: utf-8 -*-
"""
架構設計系統配置文件
"""

class ArchitectureDesignConfig:
    """架構設計系統配置"""
    
    # 服務端口配置
    MCP_PORT = 8306  # 主MCP服務端口
    UI_PORT = 5004   # UI服務端口
    
    # MCP服務配置
    MCP_SERVICE_URL = f"http://localhost:{MCP_PORT}"
    
    # 系統配置
    SYSTEM_NAME = "Pure AI Architecture Design System"
    VERSION = "1.0.0"
    
    # AI配置
    AI_TIMEOUT = 30
    CONFIDENCE_THRESHOLD = 0.8
    
    @classmethod
    def get_config(cls):
        """獲取配置字典"""
        return {
            'ports': {
                'mcp': cls.MCP_PORT,
                'ui': cls.UI_PORT
            },
            'urls': {
                'mcp_service': cls.MCP_SERVICE_URL
            },
            'system': {
                'name': cls.SYSTEM_NAME,
                'version': cls.VERSION
            },
            'ai': {
                'timeout': cls.AI_TIMEOUT,
                'confidence_threshold': cls.CONFIDENCE_THRESHOLD
            }
        }

