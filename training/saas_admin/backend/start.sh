#!/bin/bash

echo "=== 启动SaaS管理系统后端 ==="

cd "$(dirname "$0")"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "复制环境变量文件..."
    cp .env.example .env
    echo "警告：请修改 .env 文件中的配置"
fi

echo "启动服务..."
python main.py

