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

# 使用Gunicorn运行应用
CMD ["gunicorn", "--bind", "0.0.0.0:6667", "app:app"]
