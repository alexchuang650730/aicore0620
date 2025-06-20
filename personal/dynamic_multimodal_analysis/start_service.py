#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
啟動腳本 - 設置環境變量並啟動服務
"""

import os
import subprocess
import sys

def setup_environment():
    """設置環境變量"""
    # 設置API密鑰 - 從環境變量讀取，如果沒有則使用空字符串
    os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', '')
    os.environ['KILO_API_KEY'] = os.getenv('KILO_API_KEY', '')
    os.environ['ANTHROPIC_API_KEY'] = os.getenv('KILO_API_KEY', '')
    
    print("✅ 環境變量設置完成")
    if os.environ.get('GEMINI_API_KEY'):
        print(f"📍 GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY', 'Not Set')[:20]}...")
    else:
        print("⚠️ GEMINI_API_KEY 未設置")
    
    if os.environ.get('KILO_API_KEY'):
        print(f"📍 KILO_API_KEY: {os.environ.get('KILO_API_KEY', 'Not Set')[:20]}...")
    else:
        print("⚠️ KILO_API_KEY 未設置")

def start_service():
    """啟動服務"""
    try:
        print("🚀 啟動多模態需求分析服務...")
        subprocess.run([sys.executable, "simple_service.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ 服務已停止")
    except Exception as e:
        print(f"❌ 服務啟動失敗: {e}")

if __name__ == "__main__":
    setup_environment()
    start_service()

