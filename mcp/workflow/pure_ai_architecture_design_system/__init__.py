# -*- coding: utf-8 -*-
"""
Pure AI Architecture Design System - 完整工作流MCP
"""

__version__ = "1.0.0"
__author__ = "Manus AI"
__description__ = "Complete workflow MCP for pure AI-driven architecture design system"

# 核心組件導入
from .src.architecture_orchestrator import ArchitectureOrchestrator
from .src.architecture_design_mcp import ArchitectureDesignMCP
from .src.architecture_design_ai_engine import ArchitectureDesignAIEngine

# 配置導入
from .config.global_config import ArchitectureDesignConfig
from .config.environment_config import EnvironmentConfig

__all__ = [
    'ArchitectureOrchestrator',
    'ArchitectureDesignMCP', 
    'ArchitectureDesignAIEngine',
    'ArchitectureDesignConfig',
    'EnvironmentConfig'
]

