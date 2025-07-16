import subprocess
import datetime
import os
import sys
import time


def auto_git_commit_push(repo_path, commit_message=None, branch="main", timeout=600):
    """
    修复编码问题的增强版自动提交函数
    """
    try:
        # 设置正确的编码环境（关键修复）
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['GIT_PYTHON_REFRESH'] = 'quiet'

        # 切换到仓库目录
        os.chdir(repo_path)

        # 检查变更
        print("🔍 检查文件变更...")
        status = subprocess.run(
            "git status",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',  # 显式指定编码
            errors='replace',  # 替换无法解码的字符
            env=env
        )

        if "nothing to commit" in status.stdout.lower():
            print("🟡 没有检测到文件变更，跳过提交")
            return False

        # 添加文件
        print("⏳ 正在添加文件...")
        add_process = subprocess.Popen(
            "git add .",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',  # 显式指定编码
            errors='replace',  # 替换无法解码的字符
            env=env
        )

        # 等待添加完成
        try:
            stdout, stderr = add_process.communicate(timeout=timeout)
            if stderr:
                print(f"⚠️ 添加文件警告: {stderr.strip()}")
        except subprocess.TimeoutExpired:
            add_process.kill()
            print("❌ 添加文件超时，操作已终止")
            return False

        # 生成提交信息
        if not commit_message:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"自动提交于 {timestamp}"

        # 修复提交信息中的特殊字符
        safe_commit_message = commit_message.replace('"', "'").replace('`', "'")

        # 提交变更 - 使用字节模式避免编码问题
        print("📝 正在提交变更...")
        commit_cmd = f'git commit -m "{safe_commit_message}"'
        commit_process = subprocess.Popen(
            commit_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # 使用字节模式，稍后手动解码
            text=False,  # 关键：禁用文本模式
            env=env
        )

        try:
            # 直接获取字节输出
            stdout_bytes, stderr_bytes = commit_process.communicate(timeout=timeout)

            # 手动解码输出
            stdout = stdout_bytes.decode('utf-8', errors='replace')
            stderr = stderr_bytes.decode('utf-8', errors='replace')

            if stdout.strip():
                print(f"ℹ️ 提交输出: {stdout.strip()}")
            if stderr.strip():
                print(f"⚠️ 提交警告: {stderr.strip()}")

        except subprocess.TimeoutExpired:
            commit_process.kill()
            print("❌ 提交操作超时")
            return False

        # 推送变更
        print("🚀 正在推送至远程仓库...")
        push_process = subprocess.Popen(
            f"git push origin {branch}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',  # 显式指定编码
            errors='replace',  # 替换无法解码的字符
            env=env
        )

        # 实时显示推送进度
        start_time = time.time()
        while push_process.poll() is None:
            if time.time() - start_time > timeout:
                push_process.kill()
                print(f"❌ 推送超时（超过 {timeout} 秒）")
                return False
            time.sleep(1)

        # 检查推送结果
        stdout, stderr = push_process.communicate()
        if push_process.returncode == 0:
            print(f"✅ 成功推送到 {branch} 分支")
            if stdout.strip():
                print(f"ℹ️ 推送输出: {stdout.strip()}")
            return True
        else:
            print(f"❌ 推送失败: {stderr.strip()}")
            return False

    except Exception as e:
        print(f"❌ 发生未预期错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# 使用示例
if __name__ == "__main__":
    # 配置参数
    REPO_PATH = "G:/Code/image-understanding-test-dataset"  # 替换为你的本地仓库路径
    COMMIT_MESSAGE = "[feat]：完善README.md说明"
    TARGET_BRANCH = "main"

    # 执行自动提交
    auto_git_commit_push(REPO_PATH, COMMIT_MESSAGE, TARGET_BRANCH)