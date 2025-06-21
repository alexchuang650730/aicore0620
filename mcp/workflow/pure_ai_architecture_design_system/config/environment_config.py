# -*- coding: utf-8 -*-
"""
架構設計系統環境配置
"""

import os

class EnvironmentConfig:
    """環境配置類"""
    
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.load_environment_config()
    
    def load_environment_config(self):
        """根據環境加載配置"""
        if self.environment == 'production':
            self.load_production_config()
        elif self.environment == 'staging':
            self.load_staging_config()
        else:
            self.load_development_config()
    
    def load_development_config(self):
        """開發環境配置"""
        self.debug = True
        self.log_level = 'DEBUG'
        self.host = 'localhost'
        self.cors_origins = ['http://localhost:3000', 'http://localhost:5003']
        self.ai_timeout = 30
        self.max_concurrent_requests = 10
    
    def load_staging_config(self):
        """測試環境配置"""
        self.debug = False
        self.log_level = 'INFO'
        self.host = '0.0.0.0'
        self.cors_origins = ['https://staging.example.com']
        self.ai_timeout = 45
        self.max_concurrent_requests = 20
    
    def load_production_config(self):
        """生產環境配置"""
        self.debug = False
        self.log_level = 'WARNING'
        self.host = '0.0.0.0'
        self.cors_origins = ['https://app.example.com']
        self.ai_timeout = 60
        self.max_concurrent_requests = 50
    
    def get_config(self):
        """獲取環境配置"""
        return {
            'environment': self.environment,
            'debug': self.debug,
            'log_level': self.log_level,
            'host': self.host,
            'cors_origins': self.cors_origins,
            'ai_timeout': self.ai_timeout,
            'max_concurrent_requests': self.max_concurrent_requests
        }

