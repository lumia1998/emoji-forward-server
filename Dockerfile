FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY app.py .

# 创建图片集合目录并设置权限
RUN mkdir -p image_collections && chmod 777 image_collections

# 如果有默认的txt文件，可以一起复制
COPY image_collections/ image_collections/
RUN chmod -R 755 image_collections/

# 暴露端口
EXPOSE 6667

# 使用Flask内置服务器运行应用（避免Gunicorn的问题）
CMD ["python", "app.py"]
