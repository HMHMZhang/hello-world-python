#!/usr/bin/env python3
"""
PyTorch功能测试程序
验证PyTorch在当前Python 3.14.3环境下的运行情况
"""

import torch
import torchvision
import torchaudio

def test_pytorch_basic():
    """测试PyTorch基础功能"""
    print("=== PyTorch基础功能测试 ===")
    
    # 检查版本
    print(f"PyTorch版本: {torch.__version__}")
    print(f"TorchVision版本: {torchvision.__version__}")
    print(f"TorchAudio版本: {torchaudio.__version__}")
    
    # 创建张量
    x = torch.rand(5, 3)
    print(f"随机张量:\n{x}")
    
    # 检查CUDA可用性
    print(f"CUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA设备数量: {torch.cuda.device_count()}")
        print(f"当前CUDA设备: {torch.cuda.current_device()}")
    else:
        print("当前使用CPU版本")
    
    return True

def test_pytorch_nn():
    """测试PyTorch神经网络功能"""
    print("\n=== PyTorch神经网络测试 ===")
    
    # 创建一个简单的神经网络
    model = torch.nn.Sequential(
        torch.nn.Linear(10, 5),
        torch.nn.ReLU(),
        torch.nn.Linear(5, 1)
    )
    
    # 创建随机输入
    input_data = torch.randn(1, 10)
    output = model(input_data)
    
    print(f"输入形状: {input_data.shape}")
    print(f"输出形状: {output.shape}")
    print(f"输出值: {output.item():.4f}")
    
    return True

def test_pytorch_autograd():
    """测试PyTorch自动求导功能"""
    print("\n=== PyTorch自动求导测试 ===")
    
    # 创建需要梯度的张量
    x = torch.tensor([2.0], requires_grad=True)
    y = x ** 2 + 3 * x + 2
    
    # 反向传播
    y.backward()
    
    print(f"x = {x.item()}")
    print(f"y = x² + 3x + 2 = {y.item()}")
    print(f"dy/dx = {x.grad.item()} (应该是 2x + 3 = {2*x.item() + 3})")
    
    return True

def test_pytorch_vision():
    """测试PyTorch视觉功能"""
    print("\n=== PyTorch视觉功能测试 ===")
    
    # 测试图像转换
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToPILImage(),
        torchvision.transforms.Resize((224, 224)),
        torchvision.transforms.ToTensor(),
    ])
    
    # 创建随机图像
    image = torch.randn(3, 64, 64)
    transformed = transform(image)
    
    print(f"原始图像形状: {image.shape}")
    print(f"转换后图像形状: {transformed.shape}")
    print(f"像素值范围: [{transformed.min():.3f}, {transformed.max():.3f}]")
    
    return True

if __name__ == "__main__":
    try:
        print("🚀 开始测试PyTorch功能...")
        
        test_pytorch_basic()
        test_pytorch_nn()
        test_pytorch_autograd()
        test_pytorch_vision()
        
        print("\n✅ 所有PyTorch测试通过！")
        print("🎉 PyTorch在当前Python 3.14.3环境下运行正常！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()