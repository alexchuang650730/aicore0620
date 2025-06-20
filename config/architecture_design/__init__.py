# -*- coding: utf-8 -*-
"""
架構設計系統配置模塊初始化
"""

__version__ = "1.0.0"
__author__ = "Manus AI"
__description__ = "Configuration module for architecture design system"

from .global_config import ArchitectureDesignConfig
from .environment_config import EnvironmentConfig

__all__ = ['ArchitectureDesignConfig', 'EnvironmentConfig']

