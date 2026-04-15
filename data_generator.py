import time

import pandas as pd
import numpy as np
from datetime import datetime
import os

# 获取当前脚本的绝对路径（核心修复：固定文件位置）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "latest_data.csv")


# ===================== 数据生成逻辑 =====================
def generate_latest_data():
    """生成最新数据，保存为CSV（绝对路径）"""

    while True:
        times = pd.date_range(start="2025-01-01", periods=30, freq="D")
        values = np.random.randint(100, 500, size=30)
        df = pd.DataFrame({"日期": times, "数据值": values, "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # 用绝对路径保存文件
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        print(f"✅ 数据已更新，文件路径：{DATA_FILE}")
        print(df)
        print('-------------> Next it will be sleeping 10 seconds....')
        time.sleep(10)


if __name__ == "__main__":
    generate_latest_data()