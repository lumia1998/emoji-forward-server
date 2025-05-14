FROM python:3.9-slim

WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY app.py .

# 创建图片集合目录
RUN mkdir -p image_collections

# 如果有默认的txt文件，可以一起复制
COPY image_collections/ image_collections/

# 暴露端口
EXPOSE 6667

# 使用更合适的Gunicorn配置运行应用
# 增加超时时间，减少工作进程数量，添加访问日志
CMD ["gunicorn", "--bind", "0.0.0.0:6667", "--timeout", "120", "--workers", "2", "--threads", "2", "--access-logfile", "-", "app:app"]
