"""
Log Analyzer Module - A Python package for analyzing log files with AI-powered summaries.

This module provides tools to:
- Parse log files for startup, shutdown, and error events
- Generate statistical summaries of log data
- Create AI-powered executive summaries using local LLMs
"""

from .log_analyzer import LogAnalyzer
from .config import LogAnalyzerConfig

__version__ = "1.0.0"
__author__ = "Pankaya D"
__email__ = "pankayad@example.com"

# Package-level exports
__all__ = [
    'LogAnalyzer',
    'LogAnalyzerConfig'
]