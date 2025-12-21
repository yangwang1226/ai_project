@echo off
chcp 65001 >nul
echo === 启动SaaS管理系统后端 ===
echo.

cd /d "%~dp0"

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

:: 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 安装依赖...
pip install -r requirements.txt

:: 检查.env文件
if not exist ".env" (
    echo 复制环境变量文件...
    copy .env.example .env
    echo 警告：请修改 .env 文件中的配置
)

echo 启动服务...
python main.py

pause

