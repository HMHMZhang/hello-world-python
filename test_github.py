#!/usr/bin/env python3
"""
GitHub连接测试脚本
用于测试SSH连接和GitHub集成
"""

import subprocess
import sys
import os

def run_command(command):
    """运行shell命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def test_ssh_agent():
    """测试SSH代理"""
    print("=== 测试SSH代理 ===")
    
    # 启动SSH代理
    success, _, _ = run_command("ssh-agent -s")
    if success:
        print("✅ SSH代理已启动")
    else:
        print("⚠️ 无法启动SSH代理")
    
    # 检查SSH密钥是否已添加到代理
    success, output, _ = run_command("ssh-add -l")
    if success:
        print("✅ SSH密钥已添加到代理")
    else:
        print("⚠️ SSH密钥未添加到代理")
        print("运行: ssh-add ~/.ssh/id_ed25519")

def test_github_ssh():
    """测试GitHub SSH连接"""
    print("\n=== 测试GitHub SSH连接 ===")
    
    success, output, error = run_command("ssh -T git@github.com")
    
    # GitHub SSH测试的特殊处理
    if "successfully authenticated" in output.lower() or "successfully authenticated" in error.lower():
        print("✅ GitHub SSH连接成功")
        return True
    elif "permission denied" in error.lower():
        print("❌ GitHub SSH连接失败")
        print("可能的原因:")
        print("1. SSH密钥未添加到GitHub账户")
        print("2. SSH密钥权限问题")
        print("3. SSH代理未运行")
        return False
    elif "connection refused" in error.lower():
        print("❌ 无法连接到GitHub")
        print("请检查网络连接")
        return False
    else:
        # GitHub的特殊响应处理
        if "You've successfully authenticated" in error:
            print("✅ GitHub SSH连接成功")
            return True
        else:
            print(f"⚠️ 连接测试结果: {error}")
            return False

def check_git_config():
    """检查Git配置"""
    print("\n=== 检查Git配置 ===")
    
    # 检查用户名
    success, username, _ = run_command("git config --global user.name")
    if success and username:
        print(f"✅ 用户名: {username}")
    else:
        print("❌ 未配置用户名")
    
    # 检查邮箱
    success, email, _ = run_command("git config --global user.email")
    if success and email:
        print(f"✅ 邮箱: {email}")
    else:
        print("❌ 未配置邮箱")
    
    return username, email

def check_ssh_key():
    """检查SSH密钥"""
    print("\n=== 检查SSH密钥 ===")
    
    ssh_dir = os.path.expanduser("~/.ssh")
    key_files = ["id_ed25519", "id_ed25519.pub", "id_rsa", "id_rsa.pub"]
    
    found_keys = []
    for key_file in key_files:
        key_path = os.path.join(ssh_dir, key_file)
        if os.path.exists(key_path):
            found_keys.append(key_file)
            print(f"✅ 找到: {key_file}")
    
    if not found_keys:
        print("❌ 未找到SSH密钥")
        print("请先生成SSH密钥")
    
    return found_keys

def show_github_setup_guide():
    """显示GitHub设置指南"""
    print("\n=== GitHub设置指南 ===")
    print("1. 访问: https://github.com/settings/keys")
    print("2. 点击 'New SSH key'")
    print("3. 标题填写: Trae Development")
    print("4. 将以下公钥内容复制到Key字段:")
    
    # 读取公钥内容
    ssh_dir = os.path.expanduser("~/.ssh")
    pub_key_path = os.path.join(ssh_dir, "id_ed25519.pub")
    
    if os.path.exists(pub_key_path):
        with open(pub_key_path, 'r') as f:
            public_key = f.read().strip()
            print(f"\n{public_key}")
    else:
        print("❌ 未找到公钥文件")

def main():
    """主函数"""
    print("🚀 开始测试GitHub配置...")
    
    # 检查Git配置
    check_git_config()
    
    # 检查SSH密钥
    check_ssh_key()
    
    # 测试SSH代理
    test_ssh_agent()
    
    # 测试GitHub连接
    success = test_github_ssh()
    
    if not success:
        show_github_setup_guide()
    
    print("\n📋 故障排除:")
    print("1. 确保SSH密钥已添加到GitHub")
    print("2. 运行: ssh-add ~/.ssh/id_ed25519")
    print("3. 检查网络连接")
    print("4. 查看详细错误: ssh -vT git@github.com")

if __name__ == "__main__":
    main()