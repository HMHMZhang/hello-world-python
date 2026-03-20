import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import PythonDevEnvironment

class TestPythonDevEnvironment:
    """测试Python开发环境类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.env = PythonDevEnvironment()
    
    def test_init(self):
        """测试初始化"""
        assert self.env.project_name == "PythonDevDemo"
        assert self.env.version == "1.0.0"
        assert self.env.created_at is not None
    
    def test_create_sample_data(self):
        """测试创建示例数据"""
        data = self.env.create_sample_data()
        assert "users" in data
        assert "products" in data
        assert len(data["users"]) == 2
        assert len(data["products"]) == 2
    
    def test_run_demo(self):
        """测试运行演示"""
        # 这里主要测试不抛出异常
        try:
            self.env.run_demo()
            assert True
        except Exception as e:
            pytest.fail(f"运行演示失败: {e}")

if __name__ == "__main__":
    pytest.main([__file__])