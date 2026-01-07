"""
Example of continuous monitoring with the LogAnalyzer module
"""

import time
import threading
from log_analyzer_module import LogAnalyzer

def continuous_monitoring_example():
    """Example of continuous monitoring"""
    print("=== Continuous Monitoring Example ===")
    
    # Create analyzer for monitoring
    analyzer = LogAnalyzer(
        directory_path=".",
        startup_msg="started",
        stop_msg="shutdown",
        search_list=["ERROR", "CRITICAL", "WARNING"],
        monitor_interval=10  # Check every 10 seconds
    )
    
    print("Starting continuous monitoring...")
    print("This will monitor for new log entries every 10 seconds.")
    print("Press Ctrl+C to stop.")
    
    try:
        analyzer.run_continuous_monitoring()
    except KeyboardInterrupt:
        print("\n✅ Monitoring stopped by user.")

def simulate_log_updates():
    """Simulate log file updates by appending new entries"""
    import os
    from datetime import datetime
    
    log_file = "./test_monitoring.log"
    
    print(f"=== Simulating Log Updates ===")
    print(f"Writing to {log_file}")
    
    # Create or append to test log file
    test_entries = [
        "INFO System started successfully",
        "DEBUG Loading user preferences",
        "ERROR Database connection failed",  
        "WARNING Memory usage high: 85%",
        "CRITICAL Service unavailable",
        "INFO System shutdown initiated"
    ]
    
    for i, entry in enumerate(test_entries):
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_line = f"{timestamp} {entry}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_line)
        
        print(f"Added: {log_line.strip()}")
        time.sleep(5)  # Wait 5 seconds between entries
    
    print("✅ Finished adding test entries")

def monitoring_with_custom_interval():
    """Example with custom monitoring interval"""
    print("\n=== Custom Monitoring Interval ===")
    
    analyzer = LogAnalyzer(
        directory_path=".",
        startup_msg="started",
        stop_msg="shutdown",
        search_list=["ERROR", "CRITICAL"],
        monitor_interval=5  # Very frequent monitoring
    )
    
    print("Monitoring with 5-second intervals...")
    print("This is useful for high-frequency log systems.")
    
    # Run for a limited time (30 seconds) as an example
    def stop_after_delay():
        time.sleep(30)
        print("\n⏱️  30-second demo completed")
        import os
        os._exit(0)
    
    # Start the timeout in a separate thread
    timeout_thread = threading.Thread(target=stop_after_delay)
    timeout_thread.daemon = True
    timeout_thread.start()
    
    try:
        analyzer.run_continuous_monitoring()
    except (KeyboardInterrupt, SystemExit):
        print("\n✅ Monitoring demo completed.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "simulate":
            simulate_log_updates()
        elif sys.argv[1] == "monitor":
            continuous_monitoring_example()
        elif sys.argv[1] == "custom":
            monitoring_with_custom_interval()
        else:
            print("Usage: python monitoring_example.py [simulate|monitor|custom]")
    else:
        print("Choose an example:")
        print("1. python monitoring_example.py simulate  # Simulate log updates")
        print("2. python monitoring_example.py monitor   # Run continuous monitoring")
        print("3. python monitoring_example.py custom    # Custom interval example")