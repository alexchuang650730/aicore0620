# API密鑰配置說明

## 環境變量設置

在運行服務前，請設置以下環境變量：

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export KILO_API_KEY="your_claude_api_key_here"
```

## 安全說明

- API密鑰已從代碼中移除，改用環境變量
- 請勿將API密鑰直接寫入代碼中
- 建議使用 .env 檔案或系統環境變量管理密鑰

## 使用方式

1. 設置環境變量
2. 運行 `python3 start_service.py`
3. 服務將自動讀取環境變量中的API密鑰

