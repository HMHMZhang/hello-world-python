#!/usr/bin/env python3
"""
Git和GitHub配置脚本
用于在Trae中配置GitHub集成
"""

import os
import subprocess
import sys

def run_command(command):
    """运行shell命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_git_config():
    """检查Git配置"""
    print("=== 检查Git配置 ===")
    
    # 检查用户名
    success, username, _ = run_command("git config --global user.name")
    if success and username:
        print(f"✅ 已配置用户名: {username}")
    else:
        print("❌ 未配置用户名")
    
    # 检查邮箱
    success, email, _ = run_command("git config --global user.email")
    if success and email:
        print(f"✅ 已配置邮箱: {email}")
    else:
        print("❌ 未配置邮箱")
    
    return username, email

def configure_git():
    """配置Git用户信息"""
    print("\n=== 配置Git用户信息 ===")
    
    username = input("请输入你的GitHub用户名: ").strip()
    email = input("请输入你的GitHub注册邮箱: ").strip()
    
    if username:
        success, _, _ = run_command(f'git config --global user.name "{username}"')
        if success:
            print(f"✅ 用户名已配置: {username}")
        else:
            print("❌ 用户名配置失败")
    
    if email:
        success, _, _ = run_command(f'git config --global user.email "{email}"')
        if success:
            print(f"✅ 邮箱已配置: {email}")
        else:
            print("❌ 邮箱配置失败")
    
    return username, email

def generate_ssh_key():
    """生成SSH密钥"""
    print("\n=== 生成SSH密钥 ===")
    
    ssh_dir = os.path.expanduser("~/.ssh")
    key_path = os.path.join(ssh_dir, "id_ed25519")
    
    if os.path.exists(key_path):
        print("✅ SSH密钥已存在")
        return True
    
    email = input("请输入用于SSH密钥的邮箱: ").strip()
    if not email:
        print("❌ 需要邮箱地址")
        return False
    
    # 生成SSH密钥
    command = f'ssh-keygen -t ed25519 -C "{email}" -f "{key_path}" -N ""'
    success, _, error = run_command(command)
    
    if success:
        print("✅ SSH密钥生成成功")
        print(f"公钥文件: {key_path}.pub")
        
        # 显示公钥内容
        with open(f"{key_path}.pub", 'r') as f:
            public_key = f.read().strip()
            print(f"\n公钥内容:\n{public_key}")
            print(f"\n请将此公钥添加到GitHub: https://github.com/settings/keys")
    else:
        print(f"❌ SSH密钥生成失败: {error}")
    
    return success

def test_github_connection():
    """测试GitHub连接"""
    print("\n=== 测试GitHub连接 ===")
    
    success, output, error = run_command("ssh -T git@github.com")
    
    if "successfully authenticated" in output.lower() or "successfully authenticated" in error.lower():
        print("✅ GitHub SSH连接成功")
        return True
    elif "permission denied" in error.lower():
        print("❌ GitHub SSH连接失败 - 请检查SSH密钥配置")
        print("请确保已将公钥添加到GitHub账户")
    else:
        print(f"⚠️ 连接测试结果: {error}")
    
    return False

def create_gitignore():
    """创建.gitignore文件"""
    print("\n=== 创建.gitignore文件 ===")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Local configuration
config.local.py
settings.local.py"""

    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore文件已创建")

def main():
    """主函数"""
    print("🚀 开始配置Git和GitHub...")
    
    # 检查Git配置
    username, email = check_git_config()
    
    # 如果未配置，则配置用户信息
    if not username or not email:
        username, email = configure_git()
    
    # 生成SSH密钥
    generate_ssh_key()
    
    # 创建.gitignore
    create_gitignore()
    
    print("\n📋 配置完成！下一步：")
    print("1. 将SSH公钥添加到GitHub: https://github.com/settings/keys")
    print("2. 运行: python test_github.py 测试连接")
    print("3. 运行: git init 初始化仓库")

if __name__ == "__main__":
    main()