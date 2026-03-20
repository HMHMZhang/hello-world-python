#!/usr/bin/env python3
"""
Python开发环境示例程序
展示基本的Python项目结构和功能
"""

import os
import sys
from datetime import datetime

class PythonDevEnvironment:
    """Python开发环境配置类"""
    
    def __init__(self):
        self.project_name = "PythonDevDemo"
        self.version = "1.0.0"
        self.created_at = datetime.now()
    
    def check_environment(self):
        """检查Python环境配置"""
        print("=== Python开发环境检查 ===")
        print(f"Python版本: {sys.version}")
        print(f"项目路径: {os.getcwd()}")
        print(f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 检查关键模块
        required_modules = ['os', 'sys', 'datetime', 'json', 'urllib']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"✓ {module} 模块可用")
            except ImportError:
                missing_modules.append(module)
                print(f"✗ {module} 模块缺失")
        
        if missing_modules:
            print(f"缺失模块: {missing_modules}")
        else:
            print("所有基础模块都已就绪！")
    
    def create_sample_data(self):
        """创建示例数据"""
        sample_data = {
            "users": [
                {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
                {"id": 2, "name": "李四", "email": "lisi@example.com"}
            ],
            "products": [
                {"id": 1, "name": "笔记本电脑", "price": 5999.99},
                {"id": 2, "name": "智能手机", "price": 2999.99}
            ]
        }
        return sample_data
    
    def run_demo(self):
        """运行演示程序"""
        print("\n=== Python开发环境演示 ===")
        
        # 基础功能演示
        data = self.create_sample_data()
        print("示例数据创建成功:")
        for category, items in data.items():
            print(f"  {category}: {len(items)} 条记录")
        
        # 数学计算演示
        prices = [item["price"] for item in data["products"]]
        total = sum(prices)
        average = total / len(prices) if prices else 0
        print(f"\n产品价格统计:")
        print(f"  总价: ¥{total:.2f}")
        print(f"  均价: ¥{average:.2f}")

if __name__ == "__main__":
    env = PythonDevEnvironment()
    env.check_environment()
    env.run_demo()
    print("\n🎉 Python开发环境配置完成！")