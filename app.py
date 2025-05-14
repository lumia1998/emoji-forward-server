import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# 在load_image_urls函数中添加更多日志
def load_image_urls(collection_name):
    """从指定的集合文件中加载图片URL列表"""
    # 如果已经在缓存中，直接返回
    if collection_name in url_cache:
        return url_cache[collection_name]
    
    file_path = os.path.join(TXT_DIR, f"{collection_name}.txt")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.warning(f"Collection file not found: {file_path}")
        return None
    
    # 读取文件中的所有URL
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        # 存入缓存
        url_cache[collection_name] = urls
        logger.info(f"Loaded collection '{collection_name}' with {len(urls)} URLs")
        return urls
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None

# 在random_image函数中添加超时处理
@app.route('/<collection_name>')
def random_image(collection_name):
    """随机返回指定集合中的一张图片"""
    logger.info(f"Request for collection: {collection_name}")
    
    urls = load_image_urls(collection_name)
    
    if not urls:
        logger.warning(f"Collection '{collection_name}' not found or empty")
        abort(404, description=f"Collection '{collection_name}' not found or empty")
    
    # 随机选择一个URL并重定向
    random_url = random.choice(urls)
    logger.info(f"Redirecting to: {random_url[:50]}...")  # 只记录URL的前50个字符
    return redirect(random_url)
