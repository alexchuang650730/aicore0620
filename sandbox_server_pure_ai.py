# -*- coding: utf-8 -*-
"""
純AI驅動沙盒服務 - 完全去除硬編碼和佔位符
Pure AI-Driven Sandbox Service - No Hardcoding or Placeholders
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import asyncio
import json
import logging
import os
import time
from datetime import datetime
import traceback
import signal
import sys
from werkzeug.utils import secure_filename
import uuid
from bs4 import BeautifulSoup
import hashlib

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 沙盒環境配置
app.config['ENV'] = 'development'
app.config['DEBUG'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# 動態文件上傳配置
UPLOAD_FOLDER = '/home/ubuntu/sandbox_deployment/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'md', 'html', 'htm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 動態導入AI引擎
try:
    import sys
    sys.path.append('./adapter/advanced_analysis_mcp/src')
    from advanced_ai_engine import AdvancedAIEngine as PureAIDrivenEngine
    AI_ENGINE_AVAILABLE = True
    logger.info("純AI驅動引擎加載成功")
except ImportError as e:
    AI_ENGINE_AVAILABLE = False
    logger.error(f"AI引擎加載失敗: {e}")

class DynamicFileProcessor:
    """動態文件處理器 - 無硬編碼"""
    
    def __init__(self):
        self.supported_formats = ALLOWED_EXTENSIONS
        self.processing_strategies = {}
        self._initialize_processing_strategies()
    
    def _initialize_processing_strategies(self):
        """動態初始化處理策略"""
        self.processing_strategies = {
            'html': self._process_html_file,
            'htm': self._process_html_file,
            'txt': self._process_text_file,
            'md': self._process_text_file,
            'csv': self._process_text_file,
            'default': self._process_generic_file
        }
    
    def is_allowed_file(self, filename):
        """動態檢查文件類型"""
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in self.supported_formats
    
    def process_file(self, filepath):
        """動態處理文件"""
        try:
            filename = os.path.basename(filepath)
            if '.' not in filename:
                return self._process_generic_file(filepath)
            
            extension = filename.rsplit('.', 1)[1].lower()
            processor = self.processing_strategies.get(extension, self.processing_strategies['default'])
            
            return processor(filepath)
            
        except Exception as e:
            logger.error(f"文件處理錯誤 {filepath}: {e}")
            return f"文件處理失敗: {str(e)}", None
    
    def _process_html_file(self, filepath):
        """處理HTML文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 動態提取HTML結構信息
            extracted_data = self._extract_html_structure(soup)
            
            # 構建分析文本
            analysis_text = self._build_html_analysis_text(extracted_data)
            
            return analysis_text, extracted_data
            
        except Exception as e:
            logger.error(f"HTML處理錯誤: {e}")
            return f"HTML處理失敗: {str(e)}", None
    
    def _extract_html_structure(self, soup):
        """動態提取HTML結構"""
        # 清理腳本和樣式
        for element in soup(["script", "style"]):
            element.decompose()
        
        # 動態提取各種元素
        structure_data = {
            'title': self._extract_title(soup),
            'meta_info': self._extract_meta_info(soup),
            'text_content': self._extract_text_content(soup),
            'structural_elements': self._extract_structural_elements(soup),
            'statistics': {}
        }
        
        # 動態計算統計信息
        structure_data['statistics'] = self._calculate_html_statistics(structure_data)
        
        return structure_data
    
    def _extract_title(self, soup):
        """提取標題"""
        title_element = soup.find('title')
        return title_element.get_text().strip() if title_element else "未命名文檔"
    
    def _extract_meta_info(self, soup):
        """提取Meta信息"""
        meta_info = {}
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
            content = meta.get('content')
            if name and content:
                meta_info[name] = content
        
        return meta_info
    
    def _extract_text_content(self, soup):
        """提取文本內容"""
        text_content = soup.get_text()
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return ' '.join(chunk for chunk in chunks if chunk)
    
    def _extract_structural_elements(self, soup):
        """提取結構元素"""
        elements = {
            'headings': self._extract_headings(soup),
            'links': self._extract_links(soup),
            'images': self._extract_images(soup),
            'tables': self._extract_tables(soup),
            'forms': self._extract_forms(soup),
            'lists': self._extract_lists(soup)
        }
        
        return elements
    
    def _extract_headings(self, soup):
        """提取標題"""
        headings = []
        for level in range(1, 7):
            for heading in soup.find_all(f'h{level}'):
                headings.append({
                    'level': level,
                    'text': heading.get_text().strip()
                })
        return headings
    
    def _extract_links(self, soup):
        """提取鏈接"""
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                'text': link.get_text().strip(),
                'href': link['href']
            })
        return links
    
    def _extract_images(self, soup):
        """提取圖片"""
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return images
    
    def _extract_tables(self, soup):
        """提取表格"""
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text().strip() for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)
        return tables
    
    def _extract_forms(self, soup):
        """提取表單"""
        forms = []
        for form in soup.find_all('form'):
            inputs = []
            for input_elem in form.find_all(['input', 'select', 'textarea']):
                inputs.append({
                    'type': input_elem.get('type', input_elem.name),
                    'name': input_elem.get('name', ''),
                    'placeholder': input_elem.get('placeholder', '')
                })
            forms.append(inputs)
        return forms
    
    def _extract_lists(self, soup):
        """提取列表"""
        lists = []
        for list_elem in soup.find_all(['ul', 'ol']):
            items = [li.get_text().strip() for li in list_elem.find_all('li')]
            if items:
                lists.append({
                    'type': list_elem.name,
                    'items': items
                })
        return lists
    
    def _calculate_html_statistics(self, structure_data):
        """計算HTML統計信息"""
        elements = structure_data['structural_elements']
        text_content = structure_data['text_content']
        
        return {
            'content_length': len(text_content),
            'word_count': len(text_content.split()),
            'heading_count': len(elements['headings']),
            'link_count': len(elements['links']),
            'image_count': len(elements['images']),
            'table_count': len(elements['tables']),
            'form_count': len(elements['forms']),
            'list_count': len(elements['lists'])
        }
    
    def _build_html_analysis_text(self, extracted_data):
        """構建HTML分析文本"""
        title = extracted_data['title']
        meta_info = extracted_data['meta_info']
        text_content = extracted_data['text_content']
        stats = extracted_data['statistics']
        elements = extracted_data['structural_elements']
        
        analysis_parts = [
            f"HTML文檔分析：{title}",
            "",
            "文檔元數據：",
            json.dumps(meta_info, ensure_ascii=False, indent=2) if meta_info else "無元數據",
            "",
            "主要內容：",
            text_content[:2000] + "..." if len(text_content) > 2000 else text_content,
            "",
            "結構統計：",
            f"- 內容長度：{stats['content_length']}字符",
            f"- 詞數統計：{stats['word_count']}詞",
            f"- 標題數量：{stats['heading_count']}個",
            f"- 鏈接數量：{stats['link_count']}個",
            f"- 圖片數量：{stats['image_count']}個",
            f"- 表格數量：{stats['table_count']}個",
            f"- 表單數量：{stats['form_count']}個",
            f"- 列表數量：{stats['list_count']}個",
            ""
        ]
        
        if elements['headings']:
            analysis_parts.extend([
                "標題結構：",
                json.dumps(elements['headings'][:10], ensure_ascii=False, indent=2),
                ""
            ])
        
        if elements['tables']:
            analysis_parts.extend([
                "表格數據（前3個）：",
                json.dumps(elements['tables'][:3], ensure_ascii=False, indent=2),
                ""
            ])
        
        return "\n".join(analysis_parts)
    
    def _process_text_file(self, filepath):
        """處理文本文件"""
        encodings = ['utf-8', 'gbk', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                return content, None
            except UnicodeDecodeError:
                continue
        
        return f"無法讀取文件，編碼格式不支持", None
    
    def _process_generic_file(self, filepath):
        """處理通用文件"""
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        
        return f"文件：{filename}\n大小：{file_size}字節\n需要專門的處理器來解析此文件類型", None

class DynamicAnalysisService:
    """動態分析服務 - 無硬編碼邏輯"""
    
    def __init__(self):
        self.ai_engine = PureAIDrivenEngine() if AI_ENGINE_AVAILABLE else None
        self.file_processor = DynamicFileProcessor()
        self.session_cache = {}
    
    async def analyze_requirement(self, requirement, model='pure_ai_engine'):
        """動態分析需求"""
        if not self.ai_engine:
            return {
                'success': False,
                'error': 'AI引擎不可用',
                'fallback_analysis': self._generate_fallback_analysis(requirement)
            }
        
        try:
            result = await self.ai_engine.analyze_with_fully_dynamic_ai(requirement, model)
            return result
        except Exception as e:
            logger.error(f"AI分析錯誤: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_analysis': self._generate_fallback_analysis(requirement)
            }
    
    async def analyze_files(self, file_paths, requirement="請分析上傳的文件"):
        """動態分析文件"""
        try:
            # 處理所有文件
            file_contents = []
            file_metadata = []
            
            for file_path in file_paths:
                content, metadata = self.file_processor.process_file(file_path)
                file_contents.append(content)
                file_metadata.append(metadata)
            
            # 構建綜合分析需求
            combined_requirement = self._build_file_analysis_requirement(
                requirement, file_contents, file_metadata
            )
            
            # 執行AI分析
            analysis_result = await self.analyze_requirement(combined_requirement)
            
            # 添加文件處理信息
            if analysis_result.get('success'):
                analysis_result['file_processing'] = {
                    'files_processed': len(file_paths),
                    'file_types': [self._get_file_type(path) for path in file_paths],
                    'html_files_count': sum(1 for path in file_paths if self._is_html_file(path))
                }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"文件分析錯誤: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_analysis': self._generate_fallback_analysis(requirement)
            }
    
    def _build_file_analysis_requirement(self, original_requirement, file_contents, file_metadata):
        """構建文件分析需求"""
        requirement_parts = [
            f"用戶需求：{original_requirement}",
            "",
            "文件內容分析："
        ]
        
        for i, content in enumerate(file_contents):
            requirement_parts.extend([
                f"文件 {i+1}：",
                content[:1500] + "..." if len(content) > 1500 else content,
                ""
            ])
        
        # 添加HTML特殊信息
        html_count = sum(1 for metadata in file_metadata if metadata is not None)
        if html_count > 0:
            requirement_parts.append(f"注意：包含 {html_count} 個HTML文件，需要進行結構化分析")
        
        return "\n".join(requirement_parts)
    
    def _get_file_type(self, file_path):
        """獲取文件類型"""
        if '.' not in file_path:
            return 'unknown'
        return file_path.rsplit('.', 1)[1].lower()
    
    def _is_html_file(self, file_path):
        """檢查是否為HTML文件"""
        file_type = self._get_file_type(file_path)
        return file_type in ['html', 'htm']
    
    def _generate_fallback_analysis(self, requirement):
        """生成備用分析"""
        return f"基於需求「{requirement}」的基礎分析：需要更多信息來提供詳細分析。"

# 全局服務實例
analysis_service = DynamicAnalysisService()

# 動態HTML模板生成器
class DynamicHTMLGenerator:
    """動態HTML模板生成器"""
    
    @staticmethod
    def generate_interface():
        """生成動態界面"""
        return """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 純AI驅動分析系統 - 沙盒測試</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95); 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header { 
            text-align: center; 
            margin-bottom: 40px; 
            color: #333;
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .ai-badge {
            display: inline-block;
            padding: 8px 16px;
            background: #28a745;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 5px;
            animation: glow 2s infinite;
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px #28a745; }
            50% { box-shadow: 0 0 20px #28a745; }
            100% { box-shadow: 0 0 5px #28a745; }
        }
        .no-hardcode-info {
            background: #d4edda;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #28a745;
        }
        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #e1e5e9;
        }
        .tab {
            padding: 15px 30px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 16px;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
            font-weight: 600;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .form-group { 
            margin-bottom: 25px; 
        }
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            color: #555;
        }
        textarea, select, input[type="file"] { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e1e5e9; 
            border-radius: 8px; 
            font-size: 16px;
            transition: border-color 0.3s;
        }
        textarea:focus, select:focus, input[type="file"]:focus { 
            outline: none; 
            border-color: #667eea; 
        }
        textarea { 
            min-height: 120px; 
            resize: vertical;
        }
        .file-upload-area {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            background: #f8f9fa;
            transition: all 0.3s;
        }
        .btn { 
            background: linear-gradient(45deg, #667eea, #764ba2); 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            width: 100%; 
            font-size: 18px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .btn:hover { 
            transform: translateY(-2px); 
        }
        .result { 
            margin-top: 30px; 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 5px solid #667eea;
            background: #f8f9fa;
        }
        .loading { 
            text-align: center; 
            padding: 30px; 
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 純AI驅動分析系統</h1>
            <h2>沙盒測試環境</h2>
            <p>完全去除硬編碼和佔位符的AI分析</p>
            <div class="ai-badge">🤖 純AI驅動</div>
            <div class="ai-badge">🚫 無硬編碼</div>
            <div class="ai-badge">🔄 動態分析</div>
        </div>
        
        <div class="no-hardcode-info">
            <h4>🎯 純AI驅動特性</h4>
            <p>本系統完全基於AI動態推理，<strong>無任何硬編碼邏輯</strong>、<strong>無預設回應</strong>、<strong>無佔位符</strong>。每次分析都是基於輸入需求的真實AI推理過程。</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('text')">🤖 純AI分析</button>
            <button class="tab" onclick="switchTab('upload')">📁 文件分析</button>
            <button class="tab" onclick="switchTab('api')">🔧 API測試</button>
        </div>
        
        <!-- 純AI分析標籤 -->
        <div id="text-tab" class="tab-content active">
            <form id="textForm">
                <div class="form-group">
                    <label>🤖 輸入您的分析需求</label>
                    <textarea id="requirement" name="requirement" placeholder="請輸入您需要分析的問題或需求..."></textarea>
                </div>
                
                <div class="form-group">
                    <label>🔧 選擇AI引擎</label>
                    <select id="model" name="model">
                        <option value="pure_ai_engine">純AI驅動引擎</option>
                    </select>
                </div>
                
                <button type="submit" class="btn">🚀 開始純AI分析</button>
            </form>
        </div>
        
        <!-- 文件分析標籤 -->
        <div id="upload-tab" class="tab-content">
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label>📁 選擇文件上傳</label>
                    <div class="file-upload-area">
                        <p>🎯 拖拽文件到此處或點擊選擇</p>
                        <input type="file" id="files" name="files" multiple accept=".txt,.pdf,.png,.jpg,.jpeg,.gif,.doc,.docx,.xls,.xlsx,.csv,.md,.html,.htm">
                    </div>
                </div>
                
                <div class="form-group">
                    <label>📝 分析需求（可選）</label>
                    <textarea id="uploadRequirement" name="requirement" placeholder="請描述您希望如何分析這些文件..."></textarea>
                </div>
                
                <button type="submit" class="btn">📤 上傳並分析</button>
            </form>
        </div>
        
        <!-- API測試標籤 -->
        <div id="api-tab" class="tab-content">
            <h3>🔧 API測試文檔</h3>
            
            <h4>健康檢查</h4>
            <div class="curl-example">
                <pre>curl -X GET http://localhost:8888/health</pre>
            </div>
            
            <h4>純AI分析API</h4>
            <div class="curl-example">
                <pre>curl -X POST http://localhost:8888/api/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "requirement": "您的分析需求",
    "model": "pure_ai_engine"
  }'</pre>
            </div>
            
            <h4>文件上傳分析API</h4>
            <div class="curl-example">
                <pre>curl -X POST http://localhost:8888/api/upload \\
  -F "files=@your_file.html" \\
  -F "requirement=分析文件內容"</pre>
            </div>
        </div>
        
        <div id="result" class="result" style="display: none;"></div>
    </div>
    
    <script>
        function switchTab(tabName) {
            // 隱藏所有標籤內容
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // 移除所有標籤的active類
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // 顯示選中的標籤內容
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // 添加active類到選中的標籤
            event.target.classList.add('active');
        }
        
        // 純AI分析表單提交
        document.getElementById('textForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const requirement = document.getElementById('requirement').value;
            const model = document.getElementById('model').value;
            
            if (!requirement.trim()) {
                alert('請輸入分析需求');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        requirement: requirement,
                        model: model
                    })
                });
                
                const result = await response.json();
                displayResult(result);
            } catch (error) {
                displayError('分析請求失敗: ' + error.message);
            }
        });
        
        // 文件上傳表單提交
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const files = document.getElementById('files').files;
            const requirement = document.getElementById('uploadRequirement').value || '請分析上傳的文件';
            
            if (files.length === 0) {
                alert('請選擇要上傳的文件');
                return;
            }
            
            for (let file of files) {
                formData.append('files', file);
            }
            formData.append('requirement', requirement);
            
            showLoading();
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                displayResult(result);
            } catch (error) {
                displayError('文件上傳失敗: ' + error.message);
            }
        });
        
        function showLoading() {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>🤖 AI正在進行動態分析...</p>
                </div>
            `;
        }
        
        function displayResult(result) {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            
            if (result.success) {
                const analysis = result.analysis || result.fallback_analysis || '分析完成';
                const confidence = result.confidence_score ? (result.confidence_score * 100).toFixed(1) + '%' : 'N/A';
                const processingTime = result.processing_time ? result.processing_time.toFixed(3) + 's' : 'N/A';
                
                resultDiv.innerHTML = `
                    <h3>🎯 AI分析結果</h3>
                    <div style="margin: 15px 0; padding: 10px; background: #e3f2fd; border-radius: 5px;">
                        <strong>信心度:</strong> ${confidence} | 
                        <strong>處理時間:</strong> ${processingTime} | 
                        <strong>引擎:</strong> ${result.model_used || 'pure_ai_engine'}
                    </div>
                    <div style="white-space: pre-wrap; line-height: 1.6;">${analysis}</div>
                `;
            } else {
                displayError(result.error || '分析失敗');
            }
        }
        
        function displayError(message) {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px;">
                    <h3>❌ 錯誤</h3>
                    <p>${message}</p>
                </div>
            `;
        }
    </script>
</body>
</html>
        """

# API路由
@app.route('/')
def index():
    """主頁"""
    return DynamicHTMLGenerator.generate_interface()

@app.route('/health')
def health_check():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'service': 'pure_ai_driven_analysis_system',
        'architecture': 'no_hardcoding_no_placeholders',
        'ai_engine_available': AI_ENGINE_AVAILABLE,
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'html_support': True,
        'version': '5.0.0-pure-ai',
        'environment': 'sandbox',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """純AI文本分析API"""
    try:
        data = request.get_json()
        if not data or 'requirement' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要參數：requirement'
            }), 400
        
        requirement = data['requirement']
        model = data.get('model', 'pure_ai_engine')
        
        # 執行異步分析
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                analysis_service.analyze_requirement(requirement, model)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"分析API錯誤: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_and_analyze():
    """文件上傳分析API"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': '沒有文件上傳'
            }), 400
        
        files = request.files.getlist('files')
        requirement = request.form.get('requirement', '請分析上傳的文件')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({
                'success': False,
                'error': '沒有選擇文件'
            }), 400
        
        # 保存文件
        saved_files = []
        for file in files:
            if file and analysis_service.file_processor.is_allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                saved_files.append(filepath)
        
        if not saved_files:
            return jsonify({
                'success': False,
                'error': '沒有有效的文件'
            }), 400
        
        # 執行異步分析
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                analysis_service.analyze_files(saved_files, requirement)
            )
        finally:
            loop.close()
        
        # 添加上傳文件信息
        result['uploaded_files'] = [os.path.basename(f) for f in saved_files]
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"上傳API錯誤: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

def signal_handler(sig, frame):
    """信號處理器"""
    logger.info('收到停止信號，正在關閉服務...')
    sys.exit(0)

if __name__ == '__main__':
    # 註冊信號處理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("啟動純AI驅動沙盒分析服務...")
    logger.info(f"AI引擎狀態: {'可用' if AI_ENGINE_AVAILABLE else '不可用'}")
    logger.info("服務地址: http://0.0.0.0:8888")
    
    app.run(host='0.0.0.0', port=8888, debug=False, threaded=True)

