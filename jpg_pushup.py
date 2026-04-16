import shutil
import subprocess
import os
from random import random
from typing import Optional

# ===================== 核心配置（需修改） =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_IMAGE_PATH = os.path.join(BASE_DIR, "wcz_original.jpg")
TARGET_IMAGE_NAME = "wcz_display.jpg"
TARGET_IMAGE_PATH = os.path.join(BASE_DIR, TARGET_IMAGE_NAME)

# ------------------- Token 认证配置（必填） -------------------
GITHUB_USERNAME = "wczzmy88"  # 替换为自己的用户名
GITHUB_TOKEN = "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"  # 替换为第一步生成的PAT
GITHUB_REPO = "my-data-website"  # 如：repo-name
GIT_BRANCH = "main"  # 仓库默认分支（master/main）


def run_git_command(cmd: list[str], cwd: Optional[str] = None) -> tuple[bool, str, str]:
    """增强版Git命令执行函数（兼容Token认证、超时/异常处理）"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", f"命令超时：{' '.join(cmd)}"
    except Exception as e:
        return False, "", f"命令执行异常：{' '.join(cmd)} - {str(e)}"


def config_git_token_auth():
    """配置Git使用Token认证（核心步骤）"""
    # 方式1：修改远程仓库URL，拼接Token（推荐，无需手动输入密码）
    # 格式：https://<用户名>:<Token>@github.com/<用户名>/<仓库名>.git
    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"

    # 先删除原有origin远程（避免冲突）
    run_git_command(["git", "remote", "rm", "origin"])
    # 添加新的origin远程（带Token）
    success, out, err = run_git_command(["git", "remote", "add", "origin", remote_url])
    if not success and "remote origin already exists" not in err:
        print(f"❌ 配置Token远程仓库失败：{err}")
        return False

    # 验证远程配置
    success, out, err = run_git_command(["git", "remote", "-v"])
    if success:
        print(f"✅ Token认证配置完成，远程仓库信息：\n{out}")
    return True


def push_image_to_github():
    # 1. 前置检查：图片存在性
    if not os.path.exists(SOURCE_IMAGE_PATH):
        print(f"❌ 原始图片不存在！路径：{SOURCE_IMAGE_PATH}")
        return

    # 2. 配置Token认证
    if not config_git_token_auth():
        print("❌ Token认证配置失败，终止推送")
        return

    # 3. 切换工作目录
    os.chdir(BASE_DIR)
    print(f"✅ 工作目录切换至：{BASE_DIR}")

    # 4. 复制图片（覆盖已有文件）
    try:
        shutil.copy2(SOURCE_IMAGE_PATH, TARGET_IMAGE_PATH)
        print(f"✅ 图片复制完成：{TARGET_IMAGE_NAME}")
    except Exception as e:
        print(f"❌ 图片复制失败：{str(e)}")
        return

    # 5. Git Add
    add_success, add_out, add_err = run_git_command(["git", "add", TARGET_IMAGE_PATH])
    if not add_success:
        print(f"❌ git add 失败：{add_err}")
        return
    print(f"✅ git add 执行成功：{add_out or '无输出'}")

    # 6. Git Commit（修复原脚本：无变更时仍执行提交，避免提前return）
    status_success, status_out, status_err = run_git_command(
        ["git", "status", "--porcelain", TARGET_IMAGE_PATH]
    )
    commit_msg = f"📸 上传 wcz_display.jpg {random()}"
    if not status_success:
        print(f"❌ 检查文件状态失败：{status_err}")
        return

    if not status_out.strip():
        print("ℹ️ 图片内容无变更，执行强制提交")
        commit_success, commit_out, commit_err = run_git_command(
            ["git", "commit", "-m", commit_msg, "--allow-empty"]
        )
    else:
        commit_success, commit_out, commit_err = run_git_command(
            ["git", "commit", TARGET_IMAGE_PATH, "-m", commit_msg]
        )

    if not commit_success:
        print(f"❌ git commit 失败：{commit_err}")
        return
    print(f"✅ git commit 执行成功：{commit_out}")

    # 7. Git Push（Token认证核心步骤）
    print("📤 执行git push（Token认证）...")
    push_success, push_out, push_err = run_git_command(["git", "push", "origin", GIT_BRANCH])
    if not push_success:
        print(f"❌ git push 失败：{push_err}")
        # 常见错误提示
        if "Authentication failed" in push_err:
            print("💡 认证失败排查：")
            print("  1. 检查Token是否正确（是否勾选repo权限）；")
            print("  2. 检查用户名/仓库名是否拼写错误；")
            print("  3. Token是否过期（重新生成PAT）；")
        return

    print(f"✅ git push 执行成功：{push_out}")
    print("\n🎉 图片成功上传到 GitHub 仓库！")


if __name__ == "__main__":
    # 执行主函数
    push_image_to_github()