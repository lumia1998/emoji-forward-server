# 图床式表情包随机显示程序

这是一个简单的图床式表情包随机显示服务，可以通过访问不同的路径随机显示对应文件中的一张图片。类似图床，程序可以读取多个txt文件中的图片URL，并通过访问不同的路径随机显示对应文件中的一张图片。

## 功能特点

- 多集合支持：可以管理多个表情包集合，每个集合对应一个txt文件
- 随机显示：访问特定路径时随机展示对应集合中的图片
- 自动加载：启动时自动扫描并加载所有txt文件
- 缓存机制：将URL列表缓存在内存中，避免频繁读取文件
- 动态重载：通过访问 `/reload` 可以重新加载所有集合，无需重启服务
- 首页导航：访问根路径可以看到所有可用的图片集合列表
- Docker支持：提供Docker构建和运行方式，方便部署

## 安装与使用

### 本地运行

1. 克隆仓库：
```
git clone https://github.com/yourusername/image-server.git
cd image-server
```
2.安装依赖:
```
pip install -r requirements.txt
```
3.准备表情包集合:
将示例txt文件拷贝并修改：
```
cp image_collections/a.txt.example image_collections/a.txt
cp image_collections/b.txt.example image_collections/b.txt
```

也可以创建自己的集合，每行一个图片URL

4.运行服务:
```
python app.py
```
### docker运行:
1. 克隆仓库：
```
git clone https://github.com/yourusername/image-server.git
cd image-server
```
2.构建Docker镜像：
```
docker build -t image-server .
```
3.运行Docker容器:
```
docker run -d -p 6667:6667 -v $(pwd)/image_collections:/app/image_collections --name image-server image-server
```

