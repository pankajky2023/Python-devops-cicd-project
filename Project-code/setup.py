from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="log-analyzer-ai",
    version="1.0.0",
    author="Pankaya D",
    author_email="pankayad@example.com",
    description="AI-powered log file analyzer with executive summaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pankayad/log-analyzer-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: DevOps Engineers",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ollama>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
        "monitoring": [
            "watchdog>=2.0.0",  # For real-time file monitoring
        ],
    },
    entry_points={
        "console_scripts": [
            "log-analyzer=log_analyzer_module.cli:main",
        ],
    },
    keywords="log analysis ai ollama monitoring system-administration devops",
    project_urls={
        "Bug Reports": "https://github.com/pankayad/log-analyzer-ai/issues",
        "Source": "https://github.com/pankayad/log-analyzer-ai/",
    },
)