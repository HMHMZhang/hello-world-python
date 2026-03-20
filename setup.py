from setuptools import setup, find_packages

setup(
    name="python-dev-demo",
    version="1.0.0",
    description="Python开发环境示例项目",
    author="开发者",
    author_email="dev@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "flask>=3.0.0",
        "numpy>=1.26.0",
        "pandas>=2.1.0",
        "matplotlib>=3.8.0",
        "scikit-learn>=1.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "jupyter>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "python-dev-demo=main:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
)