# 測試組件管理UI系統

## 📋 系統概述

測試組件管理UI系統是為AICore0620架構重構項目專門開發的管理界面，用於驗證和管理測試組件歸屬重構的結果。

## 🏗️ 架構重構背景

基於用戶提出的架構設計問題：
> "性能優化performance_analysis_mcp分析測試策略testing_strategy_mcp分析 這兩個要不要放在測試管理workflow?"

經過深入分析，我們制定了重構方案：

### ✅ 重構決策
- **performance_analysis_mcp**: 保留在 Coding Workflow MCP
- **testing_strategy_mcp**: 移動到 Test Management Workflow MCP

## 📁 目錄結構

```
adminboard/test_component_management/
├── backend/
│   ├── ui_backend_server.py    # Flask後端服務
│   └── requirements.txt        # Python依賴
├── config/
│   └── config.py              # 配置文件
├── docs/
│   └── README.md              # 本文檔
└── frontend/
    └── index.html             # 前端HTML頁面
```

## 🚀 功能特性

### 前端界面
- **響應式設計**: 支持桌面和移動設備
- **組件可視化**: 直觀顯示Coding和Test Management Workflow的組件
- **實時測試**: 可以直接測試兩個workflow的功能
- **架構驗證**: 驗證重構後的組件歸屬是否正確

### 後端API
- **健康檢查**: `/api/health-check` - 檢查系統狀態
- **Coding Workflow測試**: `/api/test-coding-workflow` - 測試編碼工作流
- **Test Management測試**: `/api/test-test-workflow` - 測試管理工作流
- **組件狀態**: 實時檢查各組件的運行狀態

## 🔧 部署說明

### 本地部署
1. 安裝依賴：`pip install -r backend/requirements.txt`
2. 啟動服務：`python backend/ui_backend_server.py`
3. 訪問界面：`http://localhost:5001`

### EC2部署
1. 上傳代碼到服務器
2. 配置環境和依賴
3. 啟動服務並配置防火牆
4. 通過公網IP訪問

## 📊 驗證內容

### Coding Workflow MCP (6個組件)
- ✅ **kilocode_mcp**: 代碼生成引擎
- ✅ **code_quality_mcp**: 代碼質量分析
- ✅ **architecture_design_mcp**: 架構設計分析
- ✅ **performance_analysis_mcp**: 性能分析 (保留)
- ✅ **security_audit_mcp**: 安全審計
- ✅ **code_documentation_mcp**: 代碼文檔分析
- ✅ **dependency_analysis_mcp**: 依賴關係分析

### Test Management Workflow MCP (4個組件)
- ✅ **testing_strategy_mcp**: 測試策略分析 (新增)
- ✅ **test_execution_mcp**: 測試執行管理
- ✅ **test_automation_mcp**: 測試自動化
- ✅ **quality_assurance_mcp**: 質量保證分析

## 🎯 使用方法

1. **訪問界面**: 打開瀏覽器訪問部署地址
2. **查看組件**: 界面會顯示兩個workflow的所有組件
3. **執行測試**: 點擊測試按鈕驗證workflow功能
4. **檢查健康**: 使用健康檢查功能確認系統狀態
5. **查看報告**: 查看架構重構的詳細報告

## 📈 預期結果

- **Coding Workflow**: 應該包含performance_analysis_mcp，不包含testing_strategy_mcp
- **Test Management Workflow**: 應該包含testing_strategy_mcp作為核心組件
- **AI選擇邏輯**: 應該能正確選擇合適的組件組合
- **系統健康**: 所有組件應該正常運行

## 🔗 相關文檔

- [架構重構建議_測試組件歸屬分析.md](../../docs/架構重構建議_測試組件歸屬分析.md)
- [測試組件歸屬重構完成報告.md](../../docs/測試組件歸屬重構完成報告.md)
- [AICore0620目錄規範3.0.md](../../AICore0620_目錄規範3.0.md)

## 📞 技術支持

如有問題，請參考相關文檔或聯繫開發團隊。

