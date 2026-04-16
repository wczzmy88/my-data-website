import shutil
import subprocess
import os

# ===================== 固定配置 =====================
# 获取当前脚本的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 本地原始图片路径（和脚本同目录）
SOURCE_IMAGE_PATH = os.path.join(BASE_DIR, "wcz_original.jpg")
# 上传到GitHub的新文件名
TARGET_IMAGE_NAME = "wcz_display.jpg"
# 目标路径（项目根目录）
TARGET_IMAGE_PATH = os.path.join(BASE_DIR, TARGET_IMAGE_NAME)

def push_image_to_github():
    # 1. 检查本地原始图片是否存在
    if not os.path.exists(SOURCE_IMAGE_PATH):
        print(f"❌ 错误：未找到原始图片！路径：{SOURCE_IMAGE_PATH}")
        return

    try:
        # 2. 复制并重命名图片
        shutil.copy2(SOURCE_IMAGE_PATH, TARGET_IMAGE_PATH)
        print(f"✅ 图片已复制并重命名：{TARGET_IMAGE_NAME}")

        # ===================== 核心修复：只提交这一个图片 =====================
        # 仅添加目标图片
        subprocess.run(["git", "add", TARGET_IMAGE_NAME], check=True)
        # 仅提交这个图片，忽略其他所有文件
        subprocess.run(["git", "commit", TARGET_IMAGE_NAME, "-m", "📸 上传 wcz_display.jpg"], check=True)
        # 推送到GitHub
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("🎉 图片成功上传到 GitHub 仓库！")

    except Exception as e:
        print(f"❌ 执行失败：{str(e)}")

if __name__ == "__main__":
    push_image_to_github()