import os
import re
import glob
from collections import Counter
from datetime import datetime   
import ollama


class LogAnalyzer:
    def __init__(self, directory_path,startup_msg,stop_msg , search_list):
        self.directory_path = directory_path
        self.startup_msg = startup_msg
        self.stop_msg = stop_msg
        self.search_list = search_list
        self.time_pattern = re.compile(r'(\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})')
    
    def parse_logs(self):
        """Read all the logs and create a dict out of it for processing"""
        stats={
            "startup_events": [],
            "stop_events": [],
            "message_counts": Counter()
            }
        
        "Get all log files in the directory"
        log_files = glob.glob(f"{self.directory_path}/*.log")

        if not log_files:
            print("No log files found in the specified directory.")
            return None
        
        print(f"No. of files have to scan {len(log_files)}")
        
        for log_file in log_files:
            with open(log_file,'r',encoding='utf-8') as file:
                for line in file:
                    time_match = self.time_pattern.search(line)
                    timestamp = time_match.group(0) if time_match else "Unknown Time"

                    "Check for startup events"
                    if self.startup_msg in line:
                        stats["startup_events"].append({"timestamp": timestamp, "file":os.path.basename(log_file), "line": line.strip()})
                    
                    if self.stop_msg in line:
                        stats["stop_events"].append({"timestamp": timestamp, "file":os.path.basename(log_file), "line": line.strip()})
                    
                    for msg in self.search_list:
                        if msg in line:
                            stats["message_counts"][msg] += 1
        return stats
    
    def generate_ai_summary(self, stats):
        """Sends the raw stats to a Local LLM for a nice summary."""
        if not stats:
            return

        # Prepare the context for the LLM
        prompt_data = f"""
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

        print("\n--- Sending data to Local LLM (Llama2) ---")
        try:
            response = ollama.generate(
                model='llama2',
                prompt=prompt_data
            )
            print("\n=== AI LOG ANALYSIS SUMMARY ===\n")
            print(response['response'])
            
        except Exception as e:
            print(f"Error connecting to Local LLM: {e}")
            print("Ensure Ollama is running ('ollama serve') and the model is pulled.")

# --- Configuration & Execution ---
if __name__ == "__main__":
    # 1. Define Variables
    LOG_DIR = "."  # Make sure this folder exists
    START_MSG = "System initialized successfully"
    STOP_MSG = "Shutting down system"
    INTERESTING_MESSAGES = [
        "ConnectionTimeout",
        "OutOfMemoryError",
        "Database connection failed",
        "Retry attempt"
        "BUFFER OVERFLOW"
    ]

    # 2. Run Analyzer
    analyzer = LogAnalyzer(LOG_DIR, START_MSG, STOP_MSG, INTERESTING_MESSAGES)
    log_data = analyzer.parse_logs()

    # 3. Generate Summary
    if log_data:
        analyzer.generate_ai_summary(log_data)

            


        
