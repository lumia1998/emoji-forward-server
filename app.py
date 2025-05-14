from flask import Flask, redirect, abort, jsonify
import os
import random
import logging
import sys
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 存储所有txt文件的目录
TXT_DIR = "image_collections"
# 缓存各文件的URL列表，避免频繁读取文件
url_cache = {}

def load_image_urls(collection_name):
    """从指定的集合文件中加载图片URL列表"""
    try:
        # 如果已经在缓存中，直接返回
        if collection_name in url_cache:
            logger.info(f"Using cached collection: {collection_name}")
            return url_cache[collection_name]
        
        file_path = os.path.join(TXT_DIR, f"{collection_name}.txt")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.warning(f"Collection file not found: {file_path}")
            return None
        
        # 读取文件中的所有URL
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
        
        # 存入缓存
        url_cache[collection_name] = urls
        logger.info(f"Loaded collection '{collection_name}' with {len(urls)} URLs")
        return urls
    except Exception as e:
        logger.error(f"Error loading {collection_name}: {str(e)}")
        return None

def reload_all_collections():
    """重新加载所有集合文件"""
    global url_cache
    start_time = time.time()
    url_cache = {}
    
    try:
        if not os.path.exists(TXT_DIR):
            os.makedirs(TXT_DIR)
            logger.info(f"Created directory: {TXT_DIR}")
            return
        
        logger.info(f"Scanning directory: {TXT_DIR}")
        files = os.listdir(TXT_DIR)
        logger.info(f"Found files: {files}")
        
        txt_files = [f for f in files if f.endswith('.txt')]
        logger.info(f"Found {len(txt_files)} txt files")
        
        for filename in txt_files:
            try:
                collection_name = filename[:-4]  # 移除.txt后缀
                urls = load_image_urls(collection_name)
                if urls:
                    logger.info(f"Loaded collection '{collection_name}' with {len(urls)} URLs")
                else:
                    logger.warning(f"Failed to load collection '{collection_name}'")
            except Exception as e:
                logger.error(f"Error processing file {filename}: {str(e)}")
        
        logger.info(f"Loaded {len(url_cache)} image collections: {list(url_cache.keys())}")
        logger.info(f"Reload completed in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error during reload: {str(e)}")

@app.route('/<collection_name>')
def random_image(collection_name):
    """随机返回指定集合中的一张图片"""
    try:
        logger.info(f"Request for collection: {collection_name}")
        
        urls = load_image_urls(collection_name)
        
        if not urls:
            logger.warning(f"Collection '{collection_name}' not found or empty")
            return f"Collection '{collection_name}' not found or empty. Available collections: {list(url_cache.keys())}", 404
        
        # 随机选择一个URL并重定向
        random_url = random.choice(urls)
        logger.info(f"Redirecting to URL (length: {len(random_url)})")
        return redirect(random_url)
    except Exception as e:
        logger.error(f"Error in random_image: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/reload')
def reload_collections():
    """重新加载所有集合的端点"""
    try:
        reload_all_collections()
        return jsonify({
            "status": "success",
            "message": "All collections reloaded successfully",
            "collections": list(url_cache.keys())
        })
    except Exception as e:
        logger.error(f"Error in reload_collections: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/status')
def status():
    """返回服务状态"""
    return jsonify({
        "status": "ok",
        "collections": {k: len(v) for k, v in url_cache.items()},
        "total_collections": len(url_cache),
        "total_images": sum(len(v) for v in url_cache.values())
    })

@app.route('/')
def index():
    """显示所有可用的集合和诊断信息"""
    try:
        # 确保集合已加载
        if not url_cache:
            reload_all_collections()
            
        collections = list(url_cache.keys())
        
        # 添加诊断信息
        html = "<h1>Image Collections Service</h1>"
        
        # 显示诊断信息
        html += "<h2>Diagnostic Information</h2>"
        html += f"<p>Collections directory: {os.path.abspath(TXT_DIR)}</p>"
        
        try:
            files = os.listdir(TXT_DIR)
            html += f"<p>Files in directory: {', '.join(files) if files else 'No files found'}</p>"
        except Exception as e:
            html += f"<p>Error reading directory: {str(e)}</p>"
        
        # 显示集合列表
        html += "<h2>Available Collections</h2>"
        if collections:
            html += "<ul>"
            for collection in sorted(collections):
                html += f'<li><a href="/{collection}">{collection}</a> ({len(url_cache[collection])} images)</li>'
            html += "</ul>"
        else:
            html += "<p>No collections found. Please add .txt files to the image_collections directory.</p>"
            html += "<p>Each .txt file should contain one image URL per line.</p>"
        
        html += '<p><a href="/reload">Reload all collections</a> | <a href="/status">Service Status</a></p>'
        return html
    except Exception as e:
        logger.error(f"Error in index: {str(e)}")
        return f"Error rendering index page: {str(e)}", 500

# 替代 before_first_request 的初始化方法
with app.app_context():
    logger.info("Initializing application...")
    reload_all_collections()

if __name__ == '__main__':
    # 启动服务器，监听所有网络接口的6667端口
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=6667, threaded=True)
