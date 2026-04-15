import subprocess
import sys
import webbrowser
from threading import Timer
import os

# 获取当前项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(BASE_DIR, "app.py")

# 自动打开浏览器
def open_browser():
    webbrowser.open_new("http://localhost:8501")

# 启动Streamlit服务（核心：无警告！）
if __name__ == "__main__":
    print("🚀 正在启动数据展示网站...")
    # 延迟1秒打开浏览器
    Timer(1, open_browser).start()
    # 官方标准命令启动（彻底消除所有警告）
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", APP_FILE, "--server.headless=false"],
        cwd=BASE_DIR
    )