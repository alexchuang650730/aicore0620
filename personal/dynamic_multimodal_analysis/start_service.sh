#!/bin/bash
# 多模態需求分析系統啟動腳本

echo "🚀 啟動多模態需求分析系統..."

# 設置工作目錄
cd /optnew3/multimodal_analysis_system

# 檢查Python環境
echo "📋 檢查Python環境..."
python3 --version

# 安裝依賴
echo "📦 安裝依賴包..."
pip3 install flask flask-cors pillow pymupdf python-docx pandas openpyxl anthropic

# 停止現有服務
echo "🛑 停止現有服務..."
pkill -f multimodal_requirement_analysis_service || true

# 啟動服務
echo "🌟 啟動多模態需求分析服務..."
python3 multimodal_requirement_analysis_service.py &

# 等待服務啟動
sleep 5

# 檢查服務狀態
echo "🔍 檢查服務狀態..."
curl -s http://localhost:8300/health | python3 -m json.tool || echo "服務啟動中..."

echo "✅ 部署完成！"
echo "📍 服務地址: http://localhost:8300"
echo "🏥 健康檢查: http://localhost:8300/health"
echo "📚 API文檔: http://localhost:8300/api/info"

