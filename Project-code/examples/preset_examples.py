"""
Example showing different configuration presets
"""

from log_analyzer_module import LogAnalyzer
from log_analyzer_module.config import Configurations

def web_server_analysis():
    """Analyze web server logs"""
    print("=== Web Server Log Analysis ===")
    
    config = Configurations.web_server_config()
    
    print(f"Using web server preset:")
    print(f"- Startup pattern: '{config.startup_message}'")
    print(f"- Shutdown pattern: '{config.shutdown_message}'")
    print(f"- Search patterns: {config.search_patterns}")
    
    analyzer = LogAnalyzer(
        ".",
        config.startup_message,
        config.shutdown_message,
        config.search_patterns
    )
    
    results = analyzer.run_analysis()
    return results

def database_analysis():
    """Analyze database logs"""
    print("\n=== Database Log Analysis ===")
    
    config = Configurations.database_config()
    
    print(f"Using database preset:")
    print(f"- Startup pattern: '{config.startup_message}'")
    print(f"- Shutdown pattern: '{config.shutdown_message}'")
    print(f"- Search patterns: {config.search_patterns}")
    
    analyzer = LogAnalyzer(
        ".",
        config.startup_message,
        config.shutdown_message,
        config.search_patterns
    )
    
    results = analyzer.run_analysis()
    return results

def application_analysis():
    """Analyze general application logs"""
    print("\n=== Application Log Analysis ===")
    
    config = Configurations.application_config()
    
    print(f"Using application preset:")
    print(f"- Startup pattern: '{config.startup_message}'")
    print(f"- Shutdown pattern: '{config.shutdown_message}'")
    print(f"- Search patterns: {config.search_patterns}")
    
    analyzer = LogAnalyzer(
        ".",
        config.startup_message,
        config.shutdown_message,
        config.search_patterns
    )
    
    results = analyzer.run_analysis()
    return results

def system_analysis():
    """Analyze system/infrastructure logs"""
    print("\n=== System Log Analysis ===")
    
    config = Configurations.system_config()
    
    print(f"Using system preset:")
    print(f"- Startup pattern: '{config.startup_message}'")
    print(f"- Shutdown pattern: '{config.shutdown_message}'")
    print(f"- Search patterns: {config.search_patterns}")
    
    analyzer = LogAnalyzer(
        ".",
        config.startup_message,
        config.shutdown_message,
        config.search_patterns
    )
    
    results = analyzer.run_analysis()
    return results

def compare_configurations():
    """Compare results across different configurations"""
    print("\n=== Configuration Comparison ===")
    
    configurations = {
        "Web Server": Configurations.web_server_config(),
        "Database": Configurations.database_config(),
        "Application": Configurations.application_config(),
        "System": Configurations.system_config()
    }
    
    results = {}
    
    for name, config in configurations.items():
        print(f"\nAnalyzing with {name} configuration...")
        
        analyzer = LogAnalyzer(
            ".",
            config.startup_message,
            config.shutdown_message,
            config.search_patterns
        )
        
        # Run without AI summary for comparison
        analysis = analyzer.run_analysis(generate_summary=False)
        
        if analysis:
            results[name] = {
                'startup_events': len(analysis['startup_events']),
                'stop_events': len(analysis['stop_events']),
                'message_counts': dict(analysis['message_counts']),
                'total_issues': sum(analysis['message_counts'].values())
            }
    
    # Print comparison
    print("\n" + "="*60)
    print("CONFIGURATION COMPARISON RESULTS")
    print("="*60)
    
    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  Startup Events: {data['startup_events']}")
        print(f"  Stop Events: {data['stop_events']}")
        print(f"  Total Issues: {data['total_issues']}")
        if data['message_counts']:
            print(f"  Top Issues: {dict(list(data['message_counts'].items())[:3])}")
        else:
            print(f"  Top Issues: None detected")

if __name__ == "__main__":
    try:
        # Run individual analyses
        web_server_analysis()
        database_analysis()
        application_analysis()
        system_analysis()
        
        # Compare all configurations
        compare_configurations()
        
        print("\n✅ All preset examples completed!")
        
    except Exception as e:
        print(f"❌ Error running preset examples: {e}")