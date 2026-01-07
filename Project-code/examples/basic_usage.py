"""
Example usage of the LogAnalyzer module - Basic functionality
"""

from log_analyzer_module import LogAnalyzer, LogAnalyzerConfig
from log_analyzer_module.config import Configurations

def basic_example():
    """Basic usage example"""
    print("=== Basic LogAnalyzer Usage ===")
    
    # Create analyzer with custom settings
    analyzer = LogAnalyzer(
        directory_path=".",
        startup_msg="started",
        stop_msg="shutdown", 
        search_list=["ERROR", "WARNING", "INFO"]
    )
    
    # Run analysis
    results = analyzer.run_analysis()
    
    if results:
        print(f"\nResults Summary:")
        print(f"- Startup events: {len(results['startup_events'])}")
        print(f"- Stop events: {len(results['stop_events'])}")
        print(f"- Message counts: {dict(results['message_counts'])}")
    
    return results

def config_example():
    """Usage with configuration object"""
    print("\n=== Using Configuration Object ===")
    
    # Create custom configuration
    config = LogAnalyzerConfig(
        log_directory=".",
        startup_message="application started",
        shutdown_message="application stopped",
        search_patterns=["CRITICAL", "ERROR", "timeout"],
        llm_model="llama2"
    )
    
    # Create analyzer from config
    analyzer = LogAnalyzer(
        config.log_directory,
        config.startup_message,
        config.shutdown_message,
        config.search_patterns
    )
    
    results = analyzer.run_analysis(model=config.llm_model)
    return results

def preset_example():
    """Usage with preset configurations"""
    print("\n=== Using Preset Configuration ===")
    
    # Use web server preset
    config = Configurations.web_server_config()
    
    analyzer = LogAnalyzer(
        ".",
        config.startup_message,
        config.shutdown_message,
        config.search_patterns
    )
    
    results = analyzer.run_analysis()
    return results

def analysis_only_example():
    """Run analysis without AI summary"""
    print("\n=== Analysis Without AI Summary ===")
    
    analyzer = LogAnalyzer(".", "started", "shutdown", ["ERROR", "WARNING"])
    
    # Get results without AI summary
    results = analyzer.run_analysis(generate_summary=False)
    
    if results:
        print("Manual analysis of results:")
        startup_count = len(results['startup_events'])
        stop_count = len(results['stop_events'])
        
        print(f"System restarts detected: {min(startup_count, stop_count)}")
        
        if startup_count > stop_count:
            print(f"Warning: {startup_count - stop_count} unmatched startup(s)")
        elif stop_count > startup_count:
            print(f"Warning: {stop_count - startup_count} unmatched shutdown(s)")
            
        # Show most common errors
        if results['message_counts']:
            most_common = results['message_counts'].most_common(3)
            print("Top error patterns:")
            for error, count in most_common:
                print(f"  {error}: {count} occurrences")
    
    return results

if __name__ == "__main__":
    try:
        # Run all examples
        basic_example()
        config_example() 
        preset_example()
        analysis_only_example()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")