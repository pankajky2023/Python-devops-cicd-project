import os
import re
import glob
import time
from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional, Union
import ollama

class LogAnalyzer:
    """
    A class for analyzing log files and generating AI-powered summaries.
    
    This class parses log files in a specified directory, extracts startup/shutdown
    events, counts specific message patterns, and generates executive summaries
    using a local LLM.
    """
    
    def __init__(self, directory_path: str, startup_msg: str, stop_msg: str, 
                 search_list: List[str], monitor_interval: int = 60):
        """
        Initialize the LogAnalyzer.
        
        Args:
            directory_path (str): Path to directory containing log files
            startup_msg (str): String pattern to identify startup events
            stop_msg (str): String pattern to identify shutdown events  
            search_list (List[str]): List of message patterns to count
            monitor_interval (int): Seconds between scans for continuous monitoring
        """
        self.directory_path = directory_path
        self.startup_msg = startup_msg
        self.stop_msg = stop_msg
        self.search_list = search_list
        self.monitor_interval = monitor_interval
        self.time_pattern = re.compile(r'(\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})')
        self.file_positions = {}  # Track file read positions for continuous monitoring
        
    def parse_logs(self) -> Optional[Dict]:
        """
        Parse all log files and extract events and message counts.
        
        Returns:
            Dict containing startup_events, stop_events, and message_counts,
            or None if no log files found
        """
        stats = {
            "startup_events": [],
            "stop_events": [],
            "message_counts": Counter()
        }
        
        log_files = glob.glob(f"{self.directory_path}/*.log")

        if not log_files:
            print("No log files found in the specified directory.")
            return None
        
        print(f"No. of files to scan: {len(log_files)}")
        
        for log_file in log_files:
            self._process_log_file(log_file, stats)
            
        return stats
    
    def parse_new_logs_only(self) -> Optional[Dict]:
        """
        Parse only new log entries since last scan (for continuous monitoring).
        
        Returns:
            Dict containing new events and message counts, or None if no new entries
        """
        stats = {
            "startup_events": [],
            "stop_events": [],
            "message_counts": Counter()
        }
        
        log_files = glob.glob(f"{self.directory_path}/*.log")
        
        if not log_files:
            return None
            
        new_entries_found = False
        
        for log_file in log_files:
            # Check if file was modified since last check
            try:
                file_stat = os.stat(log_file)
                file_size = file_stat.st_size
                
                # Get last known position for this file
                last_position = self.file_positions.get(log_file, 0)
                
                # Only process if file has grown
                if file_size > last_position:
                    new_entries_found = True
                    
                    with open(log_file, 'r', encoding='utf-8') as file:
                        # Seek to last known position
                        file.seek(last_position)
                        
                        # Process new lines
                        for line in file:
                            self._process_log_line(line, log_file, stats)
                        
                        # Update file position
                        self.file_positions[log_file] = file.tell()
            except IOError as e:
                print(f"Error reading file {log_file}: {e}")
        
        return stats if new_entries_found else None
    
    def _process_log_file(self, log_file: str, stats: Dict) -> None:
        """
        Process a single log file and update statistics.
        
        Args:
            log_file (str): Path to the log file
            stats (Dict): Statistics dictionary to update
        """
        try:
            with open(log_file, 'r', encoding='utf-8') as file:
                for line in file:
                    self._process_log_line(line, log_file, stats)
        except IOError as e:
            print(f"Error reading file {log_file}: {e}")
    
    def _process_log_line(self, line: str, log_file: str, stats: Dict) -> None:
        """
        Process a single log line and update statistics.
        
        Args:
            line (str): Log line to process
            log_file (str): Source file path
            stats (Dict): Statistics dictionary to update
        """
        time_match = self.time_pattern.search(line)
        timestamp = time_match.group(0) if time_match else "Unknown Time"

        # Check for startup events
        if self.startup_msg in line:
            stats["startup_events"].append({
                "timestamp": timestamp, 
                "file": os.path.basename(log_file), 
                "line": line.strip()
            })
        
        # Check for stop events
        if self.stop_msg in line:
            stats["stop_events"].append({
                "timestamp": timestamp, 
                "file": os.path.basename(log_file), 
                "line": line.strip()
            })
        
        # Count search terms
        for msg in self.search_list:
            if msg in line:
                stats["message_counts"][msg] += 1
    
    def generate_ai_summary(self, stats: Dict, model: str = 'llama2') -> None:
        """
        Generate AI-powered executive summary of log analysis.
        
        Args:
            stats (Dict): Statistics from parse_logs()
            model (str): LLM model to use for summary generation
        """
        if not stats:
            print("No statistics available for summary generation.")
            return

        prompt_data = self._build_prompt(stats)
        
        print(f"\n--- Sending data to Local LLM ({model}) ---")
        try:
            response = ollama.generate(
                model=model,
                prompt=prompt_data
            )
            print("\n=== AI LOG ANALYSIS SUMMARY ===\n")
            print(response['response'])
            
        except Exception as e:
            print(f"Error connecting to Local LLM: {e}")
            print("Ensure Ollama is running ('ollama serve') and the model is pulled.")
    
    def _build_prompt(self, stats: Dict) -> str:
        """
        Build the prompt for the LLM.
        
        Args:
            stats (Dict): Statistics dictionary
            
        Returns:
            str: Formatted prompt for the LLM
        """
        return f"""
        Here is the technical analysis of the application logs:
        
        1. Startup Events Detected: {len(stats['startup_events'])}
           Timestamps: {[e['timestamp'] for e in stats['startup_events']]}
        
        2. Shutdown Events Detected: {len(stats['stop_events'])}
           Timestamps: {[e['timestamp'] for e in stats['stop_events']]}
           
        3. Critical Message Counts:
           {dict(stats['message_counts'])}
        
        Please provide a professional "Executive Summary" of the system health. 
        Highlight any potential uptime issues based on the start/stop times and 
        flag high frequencies of specific errors.
        """
    
    def run_analysis(self, generate_summary: bool = True, model: str = 'llama2') -> Optional[Dict]:
        """
        Run complete log analysis workflow.
        
        Args:
            generate_summary (bool): Whether to generate AI summary
            model (str): LLM model to use
            
        Returns:
            Dict: Analysis results
        """
        log_data = self.parse_logs()
        
        if log_data and generate_summary:
            self.generate_ai_summary(log_data, model)
            
        return log_data
    
    def run_continuous_monitoring(self):
        """Run continuous log monitoring with change detection"""
        print(f"🚀 Starting continuous log monitoring...")
        print(f"📁 Directory: {self.directory_path}")
        print(f"⏱️  Scan interval: {self.monitor_interval} seconds")
        print("⏹️  Press Ctrl+C to stop\n")
        
        # Initial scan to set file positions
        print("📋 Initial scan...")
        initial_data = self.parse_logs()
        if initial_data:
            self.generate_ai_summary(initial_data)
        
        try:
            scan_count = 0
            while True:
                scan_count += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"[{timestamp}] 🔍 Scan #{scan_count} - Checking for new entries...")
                
                # Check for new log entries only
                new_data = self.parse_new_logs_only()
                
                if new_data and any([
                    new_data['startup_events'],
                    new_data['stop_events'], 
                    new_data['message_counts']
                ]):
                    print("🆕 New events detected!")
                    self.generate_ai_summary(new_data)
                else:
                    print("✅ No new events detected.")
                
                print(f"⏳ Next scan in {self.monitor_interval} seconds...\n")
                time.sleep(self.monitor_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user.")
        except Exception as e:
            print(f"❌ Error in monitoring: {e}")