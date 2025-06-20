#!/bin/bash

# 多模態需求分析系統部署腳本

echo "🚀 開始部署多模態需求分析系統..."

# 檢查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $python_version"

# 安裝依賴
echo "📦 安裝Python依賴..."
pip3 install -r requirements.txt

# 創建必要目錄
mkdir -p logs
mkdir -p uploads
mkdir -p temp

# 設置權限
chmod +x src/multimodal_service.py

# 檢查配置
echo "🔧 檢查配置..."
if [ -z "$HF_TOKEN" ]; then
    echo "⚠️  警告: 未設置HF_TOKEN環境變量"
    echo "請設置: export HF_TOKEN=your_huggingface_token"
fi

# 啟動服務
echo "🌟 啟動服務..."
cd src/
nohup python3 multimodal_service.py > ../logs/service.log 2>&1 &

echo "✅ 部署完成!"
echo "📊 服務地址: http://localhost:8300"
echo "📋 健康檢查: http://localhost:8300/health"
echo "📝 日誌文件: logs/service.log"

