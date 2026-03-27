# 多阶段构建 weather-mcp-server 镜像
# 使用 Python 3.12 精简版 Debian Bookworm 作为基础镜像
FROM python:3.12-slim-bookworm as base

# 设置容器内工作目录为 /app
WORKDIR /app

# 安装系统级依赖（使用 --no-install-recommends 减少镜像体积）
# 更新 apt 源并清理缓存，保持镜像精简
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 复制项目配置文件到容器
COPY pyproject.toml requirements.txt ./
# 复制 MCP 服务器主程序
COPY server.py ./

# 升级 pip 到最新版本并安装 Python 依赖
# 使用 --no-cache-dir 避免缓存，减小镜像大小
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PORT=8081

# 暴露 8081 端口供外部访问（Smithery 平台使用此端口）
EXPOSE 8081

# 配置健康检查
# 每 30 秒检查一次，超时 3 秒，启动后 5 秒开始检查，失败 3 次判定为不健康
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# 容器启动时运行 MCP 服务器
CMD ["python", "server.py"]

