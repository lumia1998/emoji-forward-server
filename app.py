from flask import Flask, redirect, abort
import os
import random

app = Flask(__name__)

# 存储所有txt文件的目录
TXT_DIR = "image_collections"
# 缓存各文件的URL列表，避免频繁读取文件
url_cache = {}

def load_image_urls(collection_name):
    """从指定的集合文件中加载图片URL列表"""
    # 如果已经在缓存中，直接返回
    if collection_name in url_cache:
        return url_cache[collection_name]
    
    file_path = os.path.join(TXT_DIR, f"{collection_name}.txt")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return None
    
    # 读取文件中的所有URL
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        # 存入缓存
        url_cache[collection_name] = urls
        return urls
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def reload_all_collections():
    """重新加载所有集合文件"""
    global url_cache
    url_cache = {}
    
    if not os.path.exists(TXT_DIR):
        os.makedirs(TXT_DIR)
        print(f"Created directory: {TXT_DIR}")
        return
    
    for filename in os.listdir(TXT_DIR):
        if filename.endswith('.txt'):
            collection_name = filename[:-4]  # 移除.txt后缀
            load_image_urls(collection_name)
    
    print(f"Loaded {len(url_cache)} image collections")

@app.route('/<collection_name>')
def random_image(collection_name):
    """随机返回指定集合中的一张图片"""
    urls = load_image_urls(collection_name)
    
    if not urls:
        abort(404, description=f"Collection '{collection_name}' not found or empty")
    
    # 随机选择一个URL并重定向
    random_url = random.choice(urls)
    return redirect(random_url)

@app.route('/reload')
def reload_collections():
    """重新加载所有集合的端点"""
    reload_all_collections()
    return "All collections reloaded successfully"

@app.route('/')
def index():
    """显示所有可用的集合"""
    collections = list(url_cache.keys())
    html = "<h1>Image Collections Service</h1><ul>"
    for collection in sorted(collections):
        html += f'<li><a href="/{collection}">{collection}</a> ({len(url_cache[collection])} images)</li>'
    html += "</ul>"
    html += '<p><a href="/reload">Reload all collections</a></p>'
    return html

if __name__ == '__main__':
    # 启动前加载所有集合
    reload_all_collections()
    # 启动服务器，监听所有网络接口的6667端口
    app.run(host='0.0.0.0', port=6667)
