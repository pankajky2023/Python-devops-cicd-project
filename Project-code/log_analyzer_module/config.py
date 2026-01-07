from dataclasses import dataclass
from typing import List

@dataclass
class LogAnalyzerConfig:
    """Configuration class for LogAnalyzer"""
    
    # Directory settings
    log_directory: str = "."
    
    # Event detection patterns
    startup_message: str = "started"
    shutdown_message: str = "shutdown"
    
    # Search patterns
    search_patterns: List[str] = None
    
    # LLM settings
    llm_model: str = "llama2"
    
    # Monitoring settings
    monitor_interval: int = 60
    
    def __post_init__(self):
        """Set default search patterns if none provided"""
        if self.search_patterns is None:
            self.search_patterns = [
                "ERROR",
                "WARNING", 
                "CRITICAL",
                "timeout",
                "failed",
                "exception"
            ]

# Predefined configurations
class Configurations:
    """Predefined configuration templates"""
    
    @staticmethod
    def web_server_config():
        """Configuration for web server logs"""
        return LogAnalyzerConfig(
            startup_message="server started",
            shutdown_message="server stopped",
            search_patterns=[
                "ERROR",
                "500",
                "404", 
                "timeout",
                "connection refused",
                "Internal Server Error"
            ]
        )
    
    @staticmethod
    def database_config():
        """Configuration for database logs"""
        return LogAnalyzerConfig(
            startup_message="database initialized",
            shutdown_message="database shutdown",
            search_patterns=[
                "ERROR",
                "deadlock",
                "connection timeout",
                "out of memory",
                "table lock",
                "query timeout"
            ]
        )
    
    @staticmethod
    def application_config():
        """Configuration for general application logs"""
        return LogAnalyzerConfig(
            startup_message="application started",
            shutdown_message="application stopped",
            search_patterns=[
                "ERROR",
                "CRITICAL",
                "OutOfMemoryError",
                "NullPointerException",
                "retry",
                "failed"
            ]
        )
    
    @staticmethod
    def system_config():
        """Configuration for system/infrastructure logs"""
        return LogAnalyzerConfig(
            startup_message="system initialized",
            shutdown_message="system shutdown",
            search_patterns=[
                "ERROR",
                "CRITICAL",
                "disk full",
                "memory exhausted",
                "network unreachable",
                "service unavailable"
            ]
        )