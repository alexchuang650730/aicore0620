# 快速部署指南

## 1. 環境準備

### 安裝Python依賴
```bash
pip3 install flask flask-cors pillow pymupdf python-docx pandas openpyxl anthropic
```

### 檢查Python版本
```bash
python3 --version  # 建議 3.8+
```

## 2. 配置API密鑰（可選）

如需啟用AI增強功能，請設置環境變量：

```bash
# OpenAI API
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic API  
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## 3. 啟動服務

```bash
# 進入系統目錄
cd multimodal_analysis_system

# 啟動主服務
python3 multimodal_requirement_analysis_service.py
```

服務將在 http://localhost:8300 啟動

## 4. 驗證部署

### 健康檢查
```bash
curl http://localhost:8300/health
```

### 測試分析功能
```bash
python3 test_multimodal_service.py
```

## 5. 基本使用

### 開始需求分析
```bash
curl -X POST http://localhost:8300/api/start-session \
  -H "Content-Type: application/json" \
  -d '{"requirement": "我需要開發一個網站"}'
```

### 上傳文檔分析
```bash
curl -X POST http://localhost:8300/api/upload-document \
  -F "file=@your-document.pdf"
```

## 6. 故障排除

### 常見問題
1. **端口被占用**：修改服務中的端口號
2. **依賴缺失**：重新安裝pip依賴
3. **文件權限**：確保文件有執行權限

### 日誌查看
服務運行時會在控制台輸出詳細日誌，可用於調試。

## 7. 生產部署建議

1. 使用反向代理（nginx）
2. 配置HTTPS證書
3. 設置進程管理（systemd/supervisor）
4. 配置日誌輪轉
5. 設置監控告警

