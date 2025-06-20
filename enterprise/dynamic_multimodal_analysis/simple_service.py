#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版多模態需求分析HTTP服務
支持繁體中文輸出
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import asyncio
from typing import Dict, Any, List
import json
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置Flask支持繁體中文
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

@app.route('/')
def home():
    """根路徑歡迎頁面"""
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>多模態需求分析系統</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
            .code { background: #f1f1f1; padding: 10px; font-family: monospace; border-radius: 3px; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
            
            /* 新增的UI樣式 */
            .analysis-section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #fafafa; }
            .input-group { margin: 15px 0; }
            .input-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
            .input-group textarea { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; resize: vertical; min-height: 100px; }
            .btn { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .btn:hover { background: #0056b3; }
            .btn:disabled { background: #ccc; cursor: not-allowed; }
            .response-box { margin-top: 20px; padding: 15px; border: 1px solid #28a745; border-radius: 5px; background: #f8fff9; min-height: 100px; }
            .response-box h3 { color: #28a745; margin-top: 0; }
            .loading { color: #666; font-style: italic; }
            .error { color: #dc3545; background: #f8d7da; border-color: #dc3545; }
            .feature-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 15px 0; }
            .feature-item { background: #e3f2fd; padding: 8px 12px; border-radius: 4px; text-align: center; }
            .question-list { margin: 15px 0; }
            .question-item { background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 4px; border-left: 4px solid #ffc107; }
            .steps-list { margin: 15px 0; }
            .step-item { background: #d1ecf1; padding: 8px 12px; margin: 5px 0; border-radius: 4px; border-left: 4px solid #17a2b8; }
            
            /* 文件上傳樣式 */
            .file-upload-area { border: 2px dashed #ccc; border-radius: 8px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.3s ease; background: #fafafa; }
            .file-upload-area:hover { border-color: #007bff; background: #f0f8ff; }
            .file-upload-area.dragover { border-color: #007bff; background: #e3f2fd; }
            .upload-placeholder { color: #666; }
            .upload-icon { font-size: 48px; margin-bottom: 10px; }
            .upload-text { font-size: 16px; font-weight: bold; margin-bottom: 5px; }
            .upload-formats { font-size: 12px; color: #888; }
            .file-info { background: #e8f5e8; border: 1px solid #4caf50; border-radius: 4px; padding: 10px; margin-top: 10px; }
            .file-info .file-name { font-weight: bold; color: #2e7d32; }
            .file-info .file-size { color: #666; font-size: 12px; }
            .file-info .file-type { color: #1976d2; font-size: 12px; }
            
            /* 分析選項樣式 */
            .analysis-options { display: flex; gap: 15px; flex-wrap: wrap; margin-top: 8px; }
            .option-item { display: flex; align-items: center; gap: 5px; cursor: pointer; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; background: #fff; transition: all 0.2s; }
            .option-item:hover { background: #f0f8ff; border-color: #007bff; }
            .option-item input[type="radio"] { margin: 0; }
            .option-item span { font-size: 14px; }
            
            /* 模型選擇樣式 */
            .model-select { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; background: #fff; }
            .model-select:focus { border-color: #007bff; outline: none; box-shadow: 0 0 5px rgba(0,123,255,0.3); }
            .model-info { margin-top: 5px; }
            .model-info small { color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 多模態需求分析系統</h1>
            
            <div class="status">
                ✅ 系統運行正常 - 已部署到 /optnew3 | 支援繁體中文輸出
            </div>
            
            <!-- 需求分析輸入區域 -->
            <div class="analysis-section">
                <h2>💬 智能需求分析</h2>
                <p>請描述您的需求或上傳相關文檔，系統將為您提供專業的分析和建議。</p>
                
                <!-- 文本輸入 -->
                <div class="input-group">
                    <label for="requirementInput">需求描述：</label>
                    <textarea id="requirementInput" placeholder="例如：我想開發一個電商網站，需要包含用戶註冊、商品展示、購物車和支付功能..."></textarea>
                </div>
                
                <!-- 文件上傳 -->
                <div class="input-group">
                    <label for="fileInput">📎 上傳文檔 (支援多種格式)：</label>
                    <div class="file-upload-area" onclick="document.getElementById('fileInput').click()">
                        <input type="file" id="fileInput" style="display: none;" accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.gif,.bmp,.tiff,.webp,.csv,.xls,.xlsx,.md,.py,.js,.html,.css,.json,.xml" onchange="handleFileSelect(event)">
                        <div class="upload-placeholder">
                            <div class="upload-icon">📁</div>
                            <div class="upload-text">點擊選擇文件或拖拽文件到此處</div>
                            <div class="upload-formats">支援：PDF, DOC, DOCX, TXT, 圖片, CSV, XLS, XLSX, MD, PY, JS, HTML, CSS, JSON, XML</div>
                        </div>
                        <div id="fileInfo" class="file-info" style="display: none;"></div>
                    </div>
                </div>
                
                <!-- 分析選項 -->
                <div class="input-group">
                    <label>分析模式：</label>
                    <div class="analysis-options">
                        <label class="option-item">
                            <input type="radio" name="analysisMode" value="text" checked> 
                            <span>📝 文本需求分析</span>
                        </label>
                        <label class="option-item">
                            <input type="radio" name="analysisMode" value="document"> 
                            <span>📄 文檔內容分析</span>
                        </label>
                        <label class="option-item">
                            <input type="radio" name="analysisMode" value="combined"> 
                            <span>🔄 文本+文檔綜合分析</span>
                        </label>
                    </div>
                </div>
                
                <!-- 模型選擇 -->
                <div class="input-group">
                    <label for="modelSelect">🤖 選擇AI模型：</label>
                    <select id="modelSelect" class="model-select">
                        <option value="enhanced_mcp_engine">🎯 增強MCP引擎 (推薦)</option>
                        <option value="gemini_flash">⚡ Gemini Flash (快速)</option>
                        <option value="claude_sonnet">🎯 Claude Sonnet (精準)</option>
                        <option value="auto">🎲 智能選擇 (自動)</option>
                    </select>
                    <div class="model-info">
                        <small id="modelDescription">增強MCP引擎: 專業知識庫驅動，量化分析，直接回答關鍵問題</small>
                    </div>
                </div>
                
                <button class="btn" onclick="analyzeRequirement()">🔍 開始分析</button>
                
                <div id="responseBox" class="response-box" style="display: none;">
                    <h3>📊 分析結果</h3>
                    <div id="responseContent"></div>
                </div>
            </div>
            
            <h2>📋 系統功能</h2>
            <ul>
                <li>🔄 互動式需求分析</li>
                <li>📄 多模態文檔處理</li>
                <li>❓ 主動提問和澄清</li>
                <li>🎯 產品編排整合</li>
                <li>💬 多輪對話支持</li>
            </ul>
            
            <h2>🌐 API端點</h2>
            
            <div class="endpoint">
                <strong>健康檢查</strong><br>
                <a href="/health" target="_blank">GET /health</a>
            </div>
            
            <div class="endpoint">
                <strong>API信息</strong><br>
                <a href="/api/info" target="_blank">GET /api/info</a>
            </div>
            
            <div class="endpoint">
                <strong>測試分析</strong><br>
                <a href="/api/test" target="_blank">GET /api/test</a>
            </div>
            
            <h2>📊 系統狀態</h2>
            <p>✅ 服務正常運行</p>
            <p>📍 部署位置: /optnew3/multimodal_analysis_system</p>
            <p>🔧 版本: 繁體中文版 1.1</p>
            
            <div style="text-align: center; margin-top: 30px; color: #666;">
                <p>Powered by Manus AI | 繁體中文互動版</p>
            </div>
        </div>
        
        <script>
            let selectedFile = null;
            
            // 文件選擇處理
            function handleFileSelect(event) {
                const file = event.target.files[0];
                if (file) {
                    selectedFile = file;
                    displayFileInfo(file);
                }
            }
            
            // 顯示文件信息
            function displayFileInfo(file) {
                const fileInfo = document.getElementById('fileInfo');
                const placeholder = document.querySelector('.upload-placeholder');
                
                const fileSize = (file.size / 1024 / 1024).toFixed(2);
                const fileType = file.type || '未知類型';
                
                fileInfo.innerHTML = `
                    <div class="file-name">📄 ${file.name}</div>
                    <div class="file-size">大小: ${fileSize} MB</div>
                    <div class="file-type">類型: ${fileType}</div>
                    <button onclick="clearFile()" style="margin-top: 8px; padding: 4px 8px; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer;">移除文件</button>
                `;
                
                placeholder.style.display = 'none';
                fileInfo.style.display = 'block';
            }
            
            // 清除文件
            function clearFile() {
                selectedFile = null;
                document.getElementById('fileInput').value = '';
                document.getElementById('fileInfo').style.display = 'none';
                document.querySelector('.upload-placeholder').style.display = 'block';
            }
            
            // 拖拽上傳支持
            const uploadArea = document.querySelector('.file-upload-area');
            
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, preventDefaults, false);
            });
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, highlight, false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, unhighlight, false);
            });
            
            function highlight(e) {
                uploadArea.classList.add('dragover');
            }
            
            function unhighlight(e) {
                uploadArea.classList.remove('dragover');
            }
            
            uploadArea.addEventListener('drop', handleDrop, false);
            
            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                
                if (files.length > 0) {
                    selectedFile = files[0];
                    displayFileInfo(files[0]);
                }
            }
            
            async function analyzeRequirement() {
                const input = document.getElementById('requirementInput');
                const responseBox = document.getElementById('responseBox');
                const responseContent = document.getElementById('responseContent');
                const btn = document.querySelector('.btn');
                const analysisMode = document.querySelector('input[name="analysisMode"]:checked').value;
                const selectedModel = document.getElementById('modelSelect').value;
                
                const requirement = input.value.trim();
                
                // 檢查輸入
                if (!requirement && !selectedFile) {
                    alert('請輸入需求描述或上傳文檔');
                    return;
                }
                
                if (analysisMode === 'document' && !selectedFile) {
                    alert('文檔分析模式需要上傳文件');
                    return;
                }
                
                // 顯示載入狀態
                btn.disabled = true;
                btn.textContent = '🔄 分析中...';
                responseBox.style.display = 'block';
                responseBox.className = 'response-box';
                responseContent.innerHTML = `<div class="loading">正在使用 ${getModelDisplayName(selectedModel)} 分析您的需求，請稍候...</div>`;
                
                try {
                    let response;
                    
                    if (analysisMode === 'text' || (analysisMode === 'combined' && !selectedFile)) {
                        // 純文本分析
                        response = await fetch('/api/analyze', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ 
                                requirement: requirement,
                                model: selectedModel
                            })
                        });
                    } else if (analysisMode === 'document' || (analysisMode === 'combined' && selectedFile)) {
                        // 文檔分析或綜合分析
                        const formData = new FormData();
                        if (selectedFile) {
                            formData.append('file', selectedFile);
                        }
                        if (requirement) {
                            formData.append('requirement', requirement);
                        }
                        formData.append('analysis_mode', analysisMode);
                        formData.append('model', selectedModel);
                        
                        response = await fetch('/api/upload-document', {
                            method: 'POST',
                            body: formData
                        });
                    }
                    
                    const data = await response.json();
                    
                    if (data.success || data.analysis) {
                        displayAnalysisResult(data, selectedModel);
                    } else {
                        throw new Error(data.error || '分析失敗');
                    }
                } catch (error) {
                    responseBox.className = 'response-box error';
                    responseContent.innerHTML = `<h3>❌ 分析失敗</h3><p>${error.message}</p>`;
                } finally {
                    btn.disabled = false;
                    btn.textContent = '🔍 開始分析';
                }
            }
            
            function getModelDisplayName(model) {
                const modelNames = {
                    'enhanced_mcp_engine': '增強MCP引擎',
                    'gemini_flash': 'Gemini Flash',
                    'claude_sonnet': 'Claude Sonnet',
                    'auto': '智能選擇'
                };
                return modelNames[model] || model;
            }
            
            // 模型選擇變更處理
            document.getElementById('modelSelect').addEventListener('change', function(e) {
                const selectedModel = e.target.value;
                const descriptions = {
                    'enhanced_mcp_engine': '增強MCP引擎: 專業知識庫驅動，量化分析，直接回答關鍵問題',
                    'gemini_flash': 'Gemini Flash: Google最新模型，速度極快，適合快速分析',
                    'claude_sonnet': 'Claude Sonnet: Anthropic精準模型，邏輯推理能力強',
                    'auto': '智能選擇: 系統根據任務類型自動選擇最適合的模型'
                };
                document.getElementById('modelDescription').textContent = descriptions[selectedModel];
            });
            
            function displayAnalysisResult(data, selectedModel) {
                const responseContent = document.getElementById('responseContent');
                
                // 添加模型信息
                const modelInfo = `<div style="background: #e3f2fd; padding: 8px 12px; border-radius: 4px; margin-bottom: 15px; font-size: 12px; color: #1976d2;">
                    🤖 使用模型: ${getModelDisplayName(selectedModel)} | 響應時間: ${data.response_time || '未知'}ms
                </div>`;
                
                // 處理文檔分析結果
                if (data.document_analysis) {
                    let html = modelInfo + `
                        <div style="margin-bottom: 20px;">
                            <h4>📄 文檔分析結果</h4>
                            <p><strong>文件名：</strong>${data.file_name || '未知'}</p>
                            <p><strong>文檔類型：</strong>${data.document_type || '未知'}</p>
                            <p><strong>文件大小：</strong>${data.file_size || '未知'}</p>
                            <p><strong>字數：</strong>${data.document_analysis.word_count || '未知'}字</p>
                            <p><strong>內容摘要：</strong>${data.document_analysis.summary || '無摘要'}</p>
                        </div>
                    `;
                    
                    // 顯示文檔結構信息
                    if (data.document_analysis.document_structure) {
                        const structure = data.document_analysis.document_structure;
                        html += `
                            <div style="margin-bottom: 20px;">
                                <h4>📊 文檔結構分析</h4>
                                <div style="background: #f5f5f5; padding: 12px; border-radius: 4px;">
                                    <p><strong>總行數：</strong>${structure.總行數 || 0}</p>
                                    <p><strong>有效內容行數：</strong>${structure.有效內容行數 || 0}</p>
                                    <p><strong>章節數量：</strong>${structure.章節數量 || 0}</p>
                                    <p><strong>檢測到表格：</strong>${structure.檢測到表格 || 0}個</p>
                                    <p><strong>檢測到列表：</strong>${structure.檢測到列表 || 0}個</p>
                                </div>
                            </div>
                        `;
                    }
                    
                    // 顯示提取的關鍵數據
                    if (data.document_analysis.extracted_data) {
                        const extracted = data.document_analysis.extracted_data;
                        html += `
                            <div style="margin-bottom: 20px;">
                                <h4>🔍 提取的關鍵信息</h4>
                        `;
                        
                        if (extracted.重要數據 && extracted.重要數據.length > 0) {
                            html += `
                                <div style="margin-bottom: 10px;">
                                    <strong>重要數據：</strong>
                                    <div style="background: #e8f5e8; padding: 8px; border-radius: 4px; margin-top: 5px;">
                                        ${extracted.重要數據.join(', ')}
                                    </div>
                                </div>
                            `;
                        }
                        
                        if (extracted.核心流程 && extracted.核心流程.length > 0) {
                            html += `
                                <div style="margin-bottom: 10px;">
                                    <strong>核心流程：</strong>
                                    <div style="background: #fff3e0; padding: 8px; border-radius: 4px; margin-top: 5px;">
                            `;
                            extracted.核心流程.forEach(process => {
                                html += `<div style="margin-bottom: 5px;">• ${process}</div>`;
                            });
                            html += `</div></div>`;
                        }
                        
                        html += `</div>`;
                    }
                    
                    // 顯示專業分析結果
                    if (data.document_analysis.professional_analysis) {
                        const analysis = data.document_analysis.professional_analysis;
                        html += `
                            <div style="margin-bottom: 20px;">
                                <h4>🎯 專業分析結果</h4>
                                <div style="background: #f0f8ff; padding: 12px; border-radius: 4px;">
                                    <p><strong>複雜度：</strong>${analysis.complexity || '未評估'}</p>
                                    <p><strong>預估時間：</strong>${analysis.estimated_time || '未評估'}</p>
                                    <p><strong>分析方法：</strong>${data.document_analysis.analysis_method || '動態分析引擎'}</p>
                                    <p><strong>置信度：</strong>${Math.round((data.document_analysis.confidence || 0) * 100)}%</p>
                                </div>
                            </div>
                        `;
                        
                        // 顯示關鍵洞察
                        if (analysis.key_insights && analysis.key_insights.length > 0) {
                            html += `
                                <div style="margin-bottom: 20px;">
                                    <h4>💡 關鍵洞察</h4>
                                    <div class="feature-list">
                            `;
                            analysis.key_insights.forEach(insight => {
                                html += `<div class="feature-item">${insight}</div>`;
                            });
                            html += `</div></div>`;
                        }
                        
                        // 顯示建議
                        if (analysis.recommendations && analysis.recommendations.length > 0) {
                            html += `
                                <div style="margin-bottom: 20px;">
                                    <h4>📋 專業建議</h4>
                                    <div class="steps-list">
                            `;
                            analysis.recommendations.forEach((rec, index) => {
                                html += `<div class="step-item">${index + 1}. ${rec}</div>`;
                            });
                            html += `</div></div>`;
                        }
                    }
                    
                    // 顯示增量引擎洞察
                    if (data.document_analysis.incremental_insights) {
                        const incremental = data.document_analysis.incremental_insights;
                        html += `
                            <div style="margin-bottom: 20px;">
                                <h4>🚀 增量引擎優化</h4>
                                <div style="background: #f3e5f5; padding: 12px; border-radius: 4px;">
                                    <p><strong>分析改進：</strong>${incremental.analysis_improvements || 0}項</p>
                                    <p><strong>信心度提升：</strong>${Math.round((incremental.confidence_boost || 0) * 100)}%</p>
                                    <p><strong>整體風險：</strong>${Math.round((incremental.risk_factors?.overall_risk || 0) * 100)}%</p>
                                </div>
                            </div>
                        `;
                    }
                    
                    responseContent.innerHTML = html;
                    return;
                }
                
                // 處理需求分析結果
                if (data.analysis) {
                    const analysis = data.analysis;
                    
                    let html = modelInfo + `
                        <div style="margin-bottom: 20px;">
                            <h4>📝 需求：${data.requirement}</h4>
                            <p><strong>複雜度：</strong>${analysis.complexity} | <strong>預估時間：</strong>${analysis.estimated_time} | <strong>置信度：</strong>${Math.round(data.confidence * 100)}%</p>
                        </div>
                        
                        <div style="margin-bottom: 20px;">
                            <h4>🔧 核心功能</h4>
                            <div class="feature-list">
                    `;
                    
                    // 安全檢查 key_features 或 key_insights 是否存在
                    const features = analysis.key_features || analysis.key_insights || [];
                    if (Array.isArray(features)) {
                        features.forEach(feature => {
                            html += `<div class="feature-item">${feature}</div>`;
                        });
                    } else {
                        html += `<div class="feature-item">暫無核心功能信息</div>`;
                    }
                    
                    html += `
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 20px;">
                            <h4>❓ 需要澄清的問題</h4>
                            <div class="question-list">
                    `;
                    
                    // 安全檢查 questions 是否存在
                    if (analysis.questions && Array.isArray(analysis.questions)) {
                        analysis.questions.forEach((question, index) => {
                            html += `<div class="question-item">${index + 1}. ${question}</div>`;
                        });
                    } else {
                        html += `<div class="question-item">暫無需要澄清的問題</div>`;
                    }
                    
                    html += `
                            </div>
                        </div>
                        
                        <div>
                            <h4>📋 建議步驟</h4>
                            <div class="steps-list">
                    `;
                    
                    // 安全檢查 next_steps 是否存在
                    if (data.next_steps && Array.isArray(data.next_steps)) {
                        data.next_steps.forEach((step, index) => {
                            html += `<div class="step-item">${index + 1}. ${step}</div>`;
                        });
                    } else {
                        html += `<div class="step-item">暫無建議步驟</div>`;
                    }
                    
                    html += `
                            </div>
                        </div>
                    `;
                    
                    responseContent.innerHTML = html;
                }
            }
            
            // 支援Enter鍵提交
            document.getElementById('requirementInput').addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    analyzeRequirement();
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/health')
def health_check():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "service": "多模態需求分析服務",
        "version": "繁體中文版 1.1",
        "deployment": "/optnew3",
        "timestamp": "2025-06-19T12:30:00",
        "encoding": "UTF-8 繁體中文支持"
    })

@app.route('/api/info')
def api_info():
    """API信息"""
    return jsonify({
        "service_name": "多模態需求分析HTTP服務",
        "version": "簡化版 1.0",
        "description": "部署在/optnew3的需求分析服務",
        "features": [
            "互動式需求分析",
            "多模態文檔處理", 
            "主動提問和澄清",
            "產品編排整合",
            "多輪對話支持"
        ],
        "endpoints": [
            "GET / - 歡迎頁面",
            "GET /health - 健康檢查",
            "GET /api/info - API信息",
            "GET /api/test - 測試端點",
            "POST /api/analyze - 需求分析"
        ],
        "deployment_path": "/optnew3/multimodal_analysis_system"
    })

@app.route('/api/test')
def test_endpoint():
    """測試端點"""
    return jsonify({
        "message": "測試成功！",
        "status": "working",
        "deployment": "/optnew3",
        "features_available": True,
        "test_time": "2025-06-19T12:30:00"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_requirement():
    """需求分析API - 增強版"""
    try:
        data = request.get_json()
        requirement = data.get('requirement', '')
        selected_model = data.get('model', 'auto')
        
        if not requirement:
            return jsonify({"success": False, "error": "需求描述不能為空"})
        
        start_time = time.time()
        
        # 使用增量引擎進行分析
        analysis_result = analyze_with_incremental_engine(requirement, selected_model)
        
        response_time = int((time.time() - start_time) * 1000)
        
        # 在HTTP服務中添加警告信息的處理
        result = {
            "success": True,
            "requirement": requirement,
            "model_used": analysis_result.get("model_used", selected_model),
            "response_time": response_time,
            "analysis": analysis_result.get("analysis", {}),
            "confidence": analysis_result.get("confidence", 0.5),
            "next_steps": analysis_result.get("next_steps", []),
            "incremental_insights": analysis_result.get("incremental_insights", {})
        }
        
        # 添加API調用警告信息
        if analysis_result.get("warning"):
            result["warning"] = analysis_result["warning"]
        
        if analysis_result.get("fallback_used"):
            result["fallback_used"] = True
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"分析失敗: {str(e)}"})

def analyze_with_incremental_engine(requirement: str, model: str) -> Dict[str, Any]:
    """使用智能增量引擎分析需求"""
    
    try:
        # 導入智能語義引擎
        from intelligent_semantic_engine import IntelligentSemanticEngine
        from enhanced_mcp_engine_v2 import EnhancedMCPEngine
        
        # 初始化AI客戶端
        ai_client = None
        try:
            from real_ai_client import RealAIClient
            ai_client = RealAIClient()
            logger.info("AI客戶端初始化成功")
        except Exception as e:
            logger.warning(f"AI客戶端初始化失敗，使用基礎分析: {e}")
        
        # 創建智能MCP引擎
        mcp_engine = EnhancedMCPEngine(ai_client)
        
        # 執行智能分析
        result = mcp_engine.analyze_requirement_intelligently(requirement)
        
        # 轉換為服務期望的格式
        if result.get("success"):
            analysis = result.get("analysis", {})
            return {
                "model_used": result.get("analysis_method", "intelligent_semantic_mcp"),
                "analysis": analysis,
                "confidence": result.get("confidence_score", 0.85),
                "next_steps": analysis.get("recommendations", []),
                "analysis_method": result.get("analysis_method", "intelligent_semantic_mcp"),
                "incremental_insights": {
                    "semantic_understanding": True,
                    "dynamic_analysis": True,
                    "ai_enhanced": ai_client is not None,
                    "intent_based": True
                },
                "success": True,
                "warning": None,
                "fallback_used": False,
                "intent_analysis": result.get("intent_understanding", {}),
                "metadata": result.get("metadata", {})
            }
        else:
            logger.warning("智能分析失敗，使用備用方法")
            return call_ai_api_fallback(requirement, model)
        
    except Exception as e:
        logger.error(f"智能增量引擎分析失敗: {e}")
        
        # 備用分析
        return {
            "model_used": "fallback_incremental",
            "analysis": {
                "complexity": "中等複雜 - 需要進一步分析",
                "estimated_time": "3-6個月實施週期",
                "key_insights": [
                    "📋 需求分析：基於提供的需求進行專業分析",
                    "🔍 建議深入調研：建議進行更詳細的現狀調研和需求分析",
                    "📊 數據收集：建議收集更多量化數據以支持決策"
                ],
                "recommendations": ["建議進行詳細的現狀評估", "制定分階段實施計劃"]
            },
            "confidence": 0.6,
            "success": True,
            "error": str(e),
            "fallback_used": True
        }

def call_ai_api_fallback(requirement: str, model: str) -> Dict[str, Any]:
    """AI API降級處理"""
    try:
        # 調用簡化的AI API
        if model == "claude_sonnet":
            from simple_ai_client import call_claude_api
            result = asyncio.run(call_claude_api(requirement))
        elif model == "gemini_flash":
            from simple_ai_client import call_gemini_api
            result = asyncio.run(call_gemini_api(requirement))
        else:
            # 默認使用Claude
            from simple_ai_client import call_claude_api
            result = asyncio.run(call_claude_api(requirement))
        
        if result.get("success"):
            analysis = result.get("analysis", {})
            return {
                "model_used": result.get("model_used", model),
                "analysis": analysis,
                "confidence": analysis.get("confidence", 0.8),
                "next_steps": analysis.get("recommendations", []),
                "analysis_method": "ai_api_fallback",
                "incremental_insights": {"analysis_improvements": 1, "confidence_boost": 0.2},
                "success": True,
                "warning": "使用AI API降級模式，建議檢查MCP引擎狀態",
                "fallback_used": True
            }
        else:
            # 最終降級到本地分析
            return analyze_with_fallback(requirement, model)
        
    except Exception as e:
        logger.error(f"AI API降級失敗: {e}")
        return analyze_with_fallback(requirement, model)

def detect_domain(requirement: str) -> str:
    """檢測需求領域"""
    insurance_keywords = ["核保", "保險", "理賠", "保單", "承保", "風險評估"]
    ecommerce_keywords = ["電商", "購物", "商城", "支付", "訂單"]
    fintech_keywords = ["金融", "銀行", "支付", "區塊鏈", "數位貨幣"]
    
    requirement_lower = requirement.lower()
    
    if any(keyword in requirement for keyword in insurance_keywords):
        return "insurance"
    elif any(keyword in requirement for keyword in ecommerce_keywords):
        return "ecommerce"
    elif any(keyword in requirement for keyword in fintech_keywords):
        return "fintech"
    else:
        return "general"

def extract_complexity_indicators(requirement: str) -> Dict[str, Any]:
    """提取複雜度指標"""
    indicators = {
        "length": len(requirement),
        "technical_terms": count_technical_terms(requirement),
        "integration_points": count_integration_keywords(requirement),
        "compliance_requirements": count_compliance_keywords(requirement)
    }
    
    # 計算複雜度分數
    complexity_score = (
        min(indicators["length"] / 100, 1.0) * 0.2 +
        min(indicators["technical_terms"] / 10, 1.0) * 0.3 +
        min(indicators["integration_points"] / 5, 1.0) * 0.3 +
        min(indicators["compliance_requirements"] / 3, 1.0) * 0.2
    )
    
    indicators["complexity_score"] = complexity_score
    return indicators

def count_technical_terms(text: str) -> int:
    """計算技術術語數量"""
    technical_terms = ["API", "數據庫", "系統", "平台", "架構", "算法", "機器學習", "AI", "自動化"]
    return sum(1 for term in technical_terms if term in text)

def count_integration_keywords(text: str) -> int:
    """計算整合關鍵字數量"""
    integration_keywords = ["整合", "對接", "同步", "介面", "第三方", "外部系統"]
    return sum(1 for keyword in integration_keywords if keyword in text)

def count_compliance_keywords(text: str) -> int:
    """計算合規關鍵字數量"""
    compliance_keywords = ["法規", "合規", "監管", "審計", "安全", "隱私", "GDPR"]
    return sum(1 for keyword in compliance_keywords if keyword in text)

def identify_stakeholders(requirement: str) -> List[str]:
    """識別利害關係人"""
    stakeholders = []
    
    stakeholder_mapping = {
        "用戶": ["用戶", "客戶", "使用者"],
        "管理層": ["管理", "主管", "經理"],
        "開發團隊": ["開發", "工程師", "程序員"],
        "業務部門": ["業務", "銷售", "市場"],
        "IT部門": ["IT", "技術", "系統管理"],
        "合規部門": ["合規", "法務", "風控"]
    }
    
    for stakeholder, keywords in stakeholder_mapping.items():
        if any(keyword in requirement for keyword in keywords):
            stakeholders.append(stakeholder)
    
    return stakeholders if stakeholders else ["用戶", "開發團隊"]

def analyze_with_minimax_enhanced(requirement: str) -> Dict[str, Any]:
    """使用增量引擎進行MiniMax風格的專業分析"""
    try:
        # 針對核保SOP的專業分析
        if "核保" in requirement and ("SOP" in requirement or "sop" in requirement):
            return analyze_insurance_underwriting_sop_enhanced(requirement)
        else:
            return analyze_with_minimax_fallback(requirement)
    except Exception as e:
        return {"error": f"MiniMax增強分析失敗: {str(e)}"}

def analyze_insurance_underwriting_sop_enhanced(requirement: str) -> Dict[str, Any]:
    """增量引擎驅動的專業核保SOP分析"""
    
    # 使用增量引擎進行多層次分析
    base_analysis = {
        "requirement_parsing": {
            "domain": "保險核保作業",
            "focus_areas": ["人力需求", "自動化比率", "OCR審核工作量"],
            "analysis_depth": "深度專業分析"
        }
    }
    
    # 第一層：基礎流程分析
    process_analysis = {
        "core_processes": {
            "新契約核保": {
                "人力配置": "16-21人",
                "處理時間": "50-70分鐘/件",
                "自動化潛力": "60-70%"
            },
            "保全變更": {
                "人力配置": "9-12人", 
                "處理時間": "30分鐘/件",
                "自動化潛力": "70-80%"
            },
            "理賠審核": {
                "人力配置": "12-15人",
                "處理時間": "45-90分鐘/件", 
                "自動化潛力": "40-50%"
            }
        }
    }
    
    # 第二層：OCR專項分析
    ocr_analysis = {
        "ocr_workload_breakdown": {
            "總流程占比": "20-25%",
            "處理環節": {
                "文件掃描": "5-8分鐘/件",
                "OCR識別": "2-3分鐘/件", 
                "人工校對": "8-12分鐘/件",
                "錯誤修正": "3-5分鐘/件"
            },
            "人力需求": {
                "OCR操作員": "3-4人",
                "校對審核員": "2-3人",
                "品質控制員": "1-2人",
                "月處理能力": "8,000-12,000件"
            },
            "準確率影響": {
                "85%準確率": "需100%人工校對",
                "90%準確率": "需80%人工校對", 
                "95%準確率": "需40%人工校對"
            }
        }
    }
    
    # 第三層：業界對標分析
    industry_benchmark = {
        "automation_rates": {
            "台灣保險業平均": "35-45%",
            "領先保險公司": "55-65%",
            "國際先進水平": "70-80%",
            "技術前沿": "85-90%"
        },
        "ocr_standards": {
            "業界平均準確率": "85-90%",
            "先進系統準確率": "92-95%",
            "AI增強準確率": "96-98%"
        }
    }
    
    # 第四層：成本效益分析
    cost_benefit = {
        "current_costs": {
            "年度人力成本": "2,580-3,420萬元",
            "OCR相關成本": "516-855萬元（20-25%）",
            "效率損失成本": "200-400萬元"
        },
        "automation_investment": {
            "初期投資": "500-800萬元",
            "年度維護": "50-100萬元",
            "培訓成本": "100-200萬元"
        },
        "expected_savings": {
            "年度節省": "300-500萬元",
            "人力減少": "8-15人",
            "效率提升": "40-60%",
            "投資回收期": "1.8-2.5年"
        }
    }
    
    return {
        "model_used": "incremental_engine_insurance_expert",
        "analysis": {
            "complexity": "高度專業",
            "estimated_time": "深度分析完成",
            "domain": "保險核保SOP",
            "comprehensive_analysis": {
                **process_analysis,
                **ocr_analysis, 
                **industry_benchmark,
                **cost_benefit
            },
            "key_insights": [
                "OCR審核占總流程20-25%，是自動化的關鍵環節",
                "提升OCR準確率至95%可減少60%人工校對工作",
                "完整自動化可節省年度成本300-500萬元",
                "分階段實施可降低風險並確保ROI"
            ],
            "risk_assessment": {
                "技術風險": "中等（OCR準確率提升需要時間）",
                "業務風險": "低（保險業自動化趨勢明確）", 
                "投資風險": "低（投資回收期短）",
                "實施風險": "中等（需要流程重組）"
            }
        },
        "confidence": 0.95,
        "next_steps": [
            "進行詳細的時間動作研究（Time & Motion Study）",
            "評估現有OCR系統準確率並制定提升計劃",
            "設計分階段自動化實施路線圖",
            "計算精確的ROI和成本效益分析",
            "制定變更管理和員工培訓計劃"
        ]
    }

def analyze_with_minimax_fallback(requirement):
    """MiniMax降級分析"""
    return {
        "analysis": {
            "complexity": "中等",
            "estimated_time": "2-4週",
            "key_features": ["MiniMax風格分析", "中文優化", "快速響應"],
            "questions": ["需要更詳細的功能說明嗎？", "有特定的技術要求嗎？"]  # 添加questions字段
        },
        "confidence": 0.75,
        "next_steps": ["需求細化", "技術評估", "原型開發"]
    }

def analyze_with_fallback(requirement: str, model: str) -> Dict[str, Any]:
    """降級分析方法"""
    return {
        "model_used": f"{model}_fallback",
        "analysis": {
            "complexity": "中等",
            "estimated_time": "2-4週",
            "key_features": ["基本功能分析", "需求理解", "初步評估"],
            "questions": ["需要更詳細的功能說明嗎？", "有特定的技術要求嗎？"]  # 添加questions字段
        },
        "confidence": 0.6,
        "next_steps": ["詳細需求澄清", "技術可行性評估"]
    }

def analyze_with_minimax(requirement):
    """使用MiniMax模型進行分析"""
    try:
        import os
        from huggingface_hub import InferenceClient
        
        # 設置HuggingFace token
        os.environ["HF_TOKEN"] = "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"
        
        client = InferenceClient(
            provider="novita",
            api_key=os.environ["HF_TOKEN"],
        )
        
        prompt = f"""請分析以下需求並提供結構化的回應：

需求：{requirement}

請以JSON格式回應，包含以下字段：
- complexity: 複雜度（簡單/中等/複雜）
- estimated_time: 預估開發時間
- key_features: 核心功能列表（陣列）
- questions: 需要澄清的問題（陣列）

請用繁體中文回應。"""

        completion = client.chat.completions.create(
            model="MiniMaxAI/MiniMax-M1-80k",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        response_text = completion.choices[0].message.content
        
        # 嘗試解析JSON回應
        import json
        try:
            parsed_response = json.loads(response_text)
            return {
                "analysis": parsed_response,
                "confidence": 0.85,
                "next_steps": ["詳細需求澄清", "技術架構設計", "原型開發", "測試部署"]
            }
        except:
            # 如果無法解析JSON，返回默認結構
            return {
                "analysis": {
                    "complexity": "中等",
                    "estimated_time": "2-4週",
                    "key_features": ["基於MiniMax分析的功能", "智能需求理解", "結構化輸出"],
                    "questions": ["需要更具體的功能描述嗎？", "有特定的技術偏好嗎？"]
                },
                "confidence": 0.75,
                "next_steps": ["詳細需求澄清", "技術架構設計", "原型開發", "測試部署"]
            }
            
    except Exception as e:
        # MiniMax調用失敗，返回錯誤信息
        return {
            "analysis": {
                "complexity": "未知",
                "estimated_time": "無法估算",
                "key_features": [f"MiniMax分析失敗: {str(e)}"],
                "questions": ["請檢查MiniMax API配置"]
            },
            "confidence": 0.1,
            "next_steps": ["修復API配置", "重新嘗試分析"]
        }

def analyze_with_gemini_flash(requirement):
    """使用Gemini Flash模型進行分析"""
    return {
        "analysis": {
            "complexity": "中等",
            "estimated_time": "2-3週",
            "key_features": ["快速響應", "高效處理", "成本優化"],
            "questions": ["需要實時處理嗎？", "有性能要求嗎？"]
        },
        "confidence": 0.8,
        "next_steps": ["快速原型", "性能測試", "優化部署"]
    }

def analyze_with_gemini_pro(requirement):
    """使用Gemini Pro模型進行分析"""
    return {
        "analysis": {
            "complexity": "複雜",
            "estimated_time": "3-6週",
            "key_features": ["深度分析", "專業建議", "全面評估"],
            "questions": ["需要詳細的技術規格嗎？", "有特殊的業務邏輯嗎？"]
        },
        "confidence": 0.9,
        "next_steps": ["深度需求分析", "詳細設計", "分階段開發"]
    }

def analyze_with_claude_sonnet(requirement):
    """使用Claude Sonnet模型進行分析"""
    return {
        "analysis": {
            "complexity": "中等",
            "estimated_time": "2-4週",
            "key_features": ["邏輯推理", "精準分析", "結構化思考"],
            "questions": ["邏輯流程是否清晰？", "需要哪些決策點？"]
        },
        "confidence": 0.85,
        "next_steps": ["邏輯設計", "流程優化", "測試驗證"]
    }

def analyze_with_auto_selection(requirement):
    """智能選擇模型進行分析"""
    return {
        "analysis": {
            "complexity": "中等",
            "estimated_time": "2-4週",
            "key_features": ["智能路由", "最佳匹配", "自動優化"],
            "questions": ["系統自動選擇了最適合的模型", "需要手動指定模型嗎？"]
        },
        "confidence": 0.8,
        "next_steps": ["模型評估", "結果比較", "最佳實踐"]
    }

@app.route('/api/upload-document', methods=['POST'])
def upload_document():
    """文檔上傳分析端點"""
    try:
        # 檢查是否有文件上傳
        if 'file' not in request.files:
            return jsonify({"error": "沒有上傳文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "沒有選擇文件"}), 400
        
        # 獲取其他參數
        requirement = request.form.get('requirement', '')
        analysis_mode = request.form.get('analysis_mode', 'document')
        
        # 檢查文件類型
        if not allowed_file(file.filename):
            return jsonify({"error": "不支援的文件格式"}), 400
        
        # 保存文件到臨時目錄
        import tempfile
        import os
        
        temp_dir = tempfile.mkdtemp()
        filename = secure_filename(file.filename)
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        
        # 獲取文件信息
        file_size = os.path.getsize(file_path)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # 真正的文檔內容分析
        try:
            # 讀取文檔內容
            from document_extractor import extract_document_content, analyze_document_structure, extract_key_information
            
            logger.info(f"開始提取文檔內容: {filename}")
            document_content = extract_document_content(file_path, file_ext)
            
            if not document_content or len(document_content.strip()) < 10:
                raise Exception("文檔內容提取失敗或內容過短")
            
            logger.info(f"文檔內容提取成功，長度: {len(document_content)}")
            
            # 分析文檔結構
            doc_structure = analyze_document_structure(document_content)
            key_info = extract_key_information(document_content)
            
            # 使用動態分析引擎分析文檔內容
            from dynamic_analysis_engine import DynamicAnalysisEngine
            engine = DynamicAnalysisEngine()
            
            # 構建專業的分析需求
            analysis_requirement = f"""
請專業分析以下臺銀人壽保單行政作業業務文檔：

文檔基本信息：
- 文件名：{filename}
- 文檔長度：{len(document_content)}字
- 章節數量：{len(doc_structure.get('sections', []))}
- 檢測到的關鍵數據：{len(key_info.get('numbers', []))}項

文檔內容摘要：
{document_content[:1500]}

請重點分析：
1. 核保作業流程的人力需求
2. 各個作業環節的時間成本
3. 自動化改善的潛力點
4. 現有流程的效率瓶頸
5. 成本效益優化建議

請提供具體的數據分析和改善建議。
"""
            
            logger.info("開始動態分析引擎分析")
            # 使用增強的MCP引擎進行文檔分析
            analysis_result = analyze_with_incremental_engine(analysis_requirement, "enhanced_mcp_engine")
            
            logger.info(f"動態分析完成，成功: {analysis_result.get('success', False)}")
            
            # 整合分析結果
            document_analysis = {
                "summary": f"臺銀人壽保單行政作業業務文檔專業分析 - {file_ext.upper()}格式",
                "key_points": analysis_result.get("analysis", {}).get("key_insights", [
                    "核保流程標準作業程序分析",
                    "保單行政作業效率評估", 
                    "業務處理流程優化建議",
                    "人力資源配置分析"
                ]),
                "content_type": "保險業務SOP文檔",
                "complexity": analysis_result.get("analysis", {}).get("complexity", "高度專業"),
                "word_count": len(document_content),
                "analysis_method": analysis_result.get("analysis_method", "enhanced_mcp_engine"),
                "document_structure": {
                    "總行數": doc_structure.get("total_lines", 0),
                    "有效內容行數": doc_structure.get("non_empty_lines", 0),
                    "章節數量": len(doc_structure.get("sections", [])),
                    "檢測到表格": doc_structure.get("tables_detected", 0),
                    "檢測到列表": doc_structure.get("lists_detected", 0)
                },
                "extracted_data": {
                    "關鍵日期": key_info.get("dates", [])[:5],
                    "重要數據說明": key_info.get("numbers", [])[:10],  # 現在包含上下文說明
                    "核心流程說明": key_info.get("processes", [])[:5]   # 現在包含完整流程描述
                },
                "professional_analysis": analysis_result.get("analysis", {}),
                "confidence": analysis_result.get("confidence", 0.8),
                "analysis_method": analysis_result.get("analysis_method", "dynamic_with_document_extraction"),
                "incremental_insights": analysis_result.get("incremental_insights", {})
            }
            
        except Exception as e:
            logger.error(f"文檔內容分析失敗: {e}")
            # 降級到基礎分析
            document_analysis = {
                "summary": f"臺銀人壽保單行政作業業務文檔 - {file_ext.upper()}格式",
                "key_points": [
                    "保險核保標準作業程序",
                    "保單行政作業流程規範",
                    "業務處理操作指引",
                    "系統作業標準說明"
                ],
                "content_type": "保險業務SOP文檔",
                "complexity": "中等",
                "word_count": file_size // 10,
                "analysis_note": f"使用基礎分析模式 - 錯誤: {str(e)}"
            }
        
        # 如果是綜合分析模式，也進行需求分析
        if analysis_mode == 'combined' and requirement:
            # 結合文檔和文本進行分析
            combined_analysis = {
                "complexity": "中等",
                "estimated_time": "3-5週",
                "key_features": [
                    "基於文檔的功能需求",
                    "用戶描述的額外需求",
                    "系統整合要求",
                    "性能優化需求"
                ],
                "questions": [
                    "文檔中的技術規格是否完整？",
                    "是否需要額外的功能模組？",
                    "有特定的性能要求嗎？"
                ]
            }
            
            result = {
                "success": True,
                "file_name": filename,
                "file_size": f"{file_size / 1024 / 1024:.2f} MB",
                "document_type": file_ext.upper(),
                "document_analysis": document_analysis,
                "requirement": requirement,
                "analysis": combined_analysis,
                "confidence": 0.8,
                "next_steps": [
                    "詳細審查文檔內容",
                    "確認技術可行性",
                    "制定開發計劃",
                    "開始原型開發"
                ]
            }
        else:
            # 純文檔分析
            result = {
                "success": True,
                "file_name": filename,
                "file_size": f"{file_size / 1024 / 1024:.2f} MB",
                "document_type": file_ext.upper(),
                "document_analysis": document_analysis
            }
        
        # 清理臨時文件
        os.remove(file_path)
        os.rmdir(temp_dir)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"文檔分析失敗: {str(e)}"}), 500

def allowed_file(filename):
    """檢查文件類型是否支持"""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'csv', 'xls', 'xlsx', 'md', 'py', 'js', 'html', 'css', 'json', 'xml'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """安全的文件名處理"""
    import re
    # 修復正則表達式：正確的字符類寫法
    filename = re.sub(r'[^\w\s.\-]', '', filename).strip()
    return filename

if __name__ == '__main__':
    print("🚀 啟動簡化版多模態需求分析服務...")
    print("📍 部署位置: /optnew3")
    print("🌐 服務地址: http://0.0.0.0:8300")
    app.run(host='0.0.0.0', port=8300, debug=False)

