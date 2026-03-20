#!/usr/bin/env python3
"""
Hello World Python脚本
这是一个简单的Python程序，展示基本的Python语法和功能
"""

import datetime
import os
import platform
import sys

def say_hello(name="World"):
    """向指定的人打招呼"""
    return f"Hello, {name}! 👋"

def show_system_info():
    """显示系统信息"""
    print("=== 系统信息 ===")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"工作目录: {os.getcwd()}")

def interactive_mode():
    """交互模式"""
    print("\n=== 交互模式 ===")
    name = input("请输入你的名字: ").strip()
    if not name:
        name = "World"
    
    greeting = say_hello(name)
    print(greeting)
    
    # 添加一些个性化内容
    if name.lower() != "world":
        print(f"很高兴认识你，{name}！🎉")
        print(f"你的名字有 {len(name)} 个字符")

def main():
    """主函数"""
    print("🚀 Hello World Python程序启动！")
    print("=" * 50)
    
    # 基本问候
    print(say_hello())
    
    # 显示系统信息
    show_system_info()
    
    # 交互模式
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用！再见！")
        return
    
    # 结束语
    print("\n" + "=" * 50)
    print("✅ Hello World程序运行完成！")
    print("🎯 这是你的第一个Python程序上传到GitHub！")

if __name__ == "__main__":
    main()