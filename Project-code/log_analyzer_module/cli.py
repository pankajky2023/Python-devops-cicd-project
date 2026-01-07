import argparse
import sys
from .log_analyzer import LogAnalyzer
from .config import LogAnalyzerConfig, Configurations

def main():
    """Command line interface for LogAnalyzer"""
    parser = argparse.ArgumentParser(
        description='Analyze log files with AI-powered summaries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --directory ./logs
  %(prog)s -d ./logs -s "server started" -t "server stopped"
  %(prog)s --preset web --directory ./logs
  %(prog)s --continuous --interval 30
        """
    )
    
    parser.add_argument(
        '--directory', '-d', 
        default='.',
        help='Directory containing log files (default: current directory)'
    )
    
    parser.add_argument(
        '--startup-msg', '-s',
        default='started',
        help='Pattern to identify startup events (default: "started")'
    )
    
    parser.add_argument(
        '--stop-msg', '-t',
        default='shutdown',
        help='Pattern to identify shutdown events (default: "shutdown")'
    )
    
    parser.add_argument(
        '--search-terms', '-e',
        nargs='+',
        default=['ERROR', 'WARNING', 'CRITICAL'],
        help='Terms to search for and count (default: ERROR WARNING CRITICAL)'
    )
    
    parser.add_argument(
        '--model', '-m',
        default='llama2',
        help='LLM model to use for summary (default: llama2)'
    )
    
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip AI summary generation'
    )
    
    parser.add_argument(
        '--preset', '-p',
        choices=['web', 'database', 'application', 'system'],
        help='Use predefined configuration preset'
    )
    
    parser.add_argument(
        '--continuous', '-c',
        action='store_true',
        help='Run in continuous monitoring mode'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=60,
        help='Monitoring interval in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        # Use preset configuration if specified
        if args.preset:
            if args.preset == 'web':
                config = Configurations.web_server_config()
            elif args.preset == 'database':
                config = Configurations.database_config()
            elif args.preset == 'application':
                config = Configurations.application_config()
            elif args.preset == 'system':
                config = Configurations.system_config()
                
            analyzer = LogAnalyzer(
                args.directory,
                config.startup_message,
                config.shutdown_message,
                config.search_patterns,
                args.interval
            )
        else:
            # Use command line arguments
            analyzer = LogAnalyzer(
                args.directory,
                args.startup_msg,
                args.stop_msg,
                args.search_terms,
                args.interval
            )
        
        # Run analysis
        if args.continuous:
            print("Starting continuous monitoring mode...")
            analyzer.run_continuous_monitoring()
        else:
            analyzer.run_analysis(
                generate_summary=not args.no_summary,
                model=args.model
            )
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()