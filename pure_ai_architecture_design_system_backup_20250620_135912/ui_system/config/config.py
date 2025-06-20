# -*- coding: utf-8 -*-
"""
架構設計系統配置文件
Architecture Design System Configuration
"""

# 服務配置
SERVICE_CONFIG = {
    'ui_server': {
        'host': '0.0.0.0',
        'port': 5002,
        'debug': True
    },
    'architecture_mcp': {
        'host': '0.0.0.0', 
        'port': 8303,
        'url': 'http://localhost:8303'
    }
}

# 系統配置
SYSTEM_CONFIG = {
    'service_name': 'pure_ai_architecture_design_system',
    'version': '1.0.0-pure-ai',
    'description': '純AI驅動的企業級架構設計分析系統',
    'ai_driven': True,
    'hardcoding': False
}

# 分析配置
ANALYSIS_CONFIG = {
    'default_confidence_threshold': 0.8,
    'max_analysis_time': 30,  # 秒
    'fallback_enabled': True,
    'supported_file_types': ['.pdf', '.doc', '.docx', '.txt', '.md']
}

# 日誌配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'architecture_design_system.log'
}

