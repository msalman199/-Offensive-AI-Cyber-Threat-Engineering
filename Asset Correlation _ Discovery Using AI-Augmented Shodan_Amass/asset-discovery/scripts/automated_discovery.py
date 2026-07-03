#!/usr/bin/env python3
import subprocess
import json
import time
import schedule
import argparse
from datetime import datetime, timedelta
import os

class AutomatedAssetDiscovery:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.results_dir = "results"
        self.ensure_directories()
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Creating default...")
            default_config = {
                "targets": {
                    "domains": ["example.com"],
                    "shodan_queries": ["apache", "nginx"]
                },
                "schedule": {
                    "interval_hours": 24,
                    "max_results": 100
                },
                "notifications": {
                    "enabled": False,
                    "webhook_url": ""
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def run_discovery_cycle(self):
        """Execute a complete discovery cycle"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/discovery_{timestamp}.log"
        
        print(f"Starting discovery cycle at {datetime.now()}")
        
        with open(log_file, 'w') as log:
            log.write(f"Discovery cycle started: {datetime.now()}\n")
            
            # Run for each domain
            for domain in self.config['targets']['domains']:
                log.write(f"Processing domain: {domain}\n")
                
                # Run Amass
                amass_output = f"{self.results_dir}/amass_{domain}_{timestamp}.json"
                amass_cmd = f"amass enum -passive -d {domain} -json -o {amass_output}"
                
                try:
                    subprocess.run(amass_cmd, shell=True, check=True, timeout=300)
                    log.write(f"Amass completed for {domain}\n")
                except subprocess.TimeoutExpired:
                    log.write(f"Amass timeout for {domain}\n")
                except subprocess.CalledProcessError as e:
                    log.write(f"Amass error for {domain}: {e}\n")
            
            # Run Shodan queries
            for query in self.config['targets']['shodan_queries']:
                log.write(f"Processing Shodan query: {query}\n")
                
                shodan_output = f"{self.results_dir}/shodan_{query.replace(' ', '_')}_{timestamp}.json"
                shodan_cmd = f"shodan search --fields ip_str,port,org,hostnames,product,version '{query}' --limit {self.config['schedule']['max_results']} > {shodan_output}"
                
                try:
                    subprocess.run(shodan_cmd, shell=True, check=True, timeout=120)
                    log.write(f"Shodan completed for query: {query}\n")
                except subprocess.TimeoutExpired:
                    log.write(f"Shodan timeout for query: {query}\n")
                except subprocess.CalledProcessError as e:
                    log.write(f"Shodan error for query {query}: {e}\n")
            
            # Run correlation analysis
            if self.config['targets']['domains'] and self.config['targets']['shodan_queries']:
                correlation_cmd = f"python3 scripts/ai_asset_correlator.py '{self.config['targets']['shodan_queries'][0]}' {self.config['targets']['domains'][0]}"
                
                try:
                    subprocess.run(correlation_cmd, shell=True, check=True, timeout=180)
                    log.write("AI correlation completed\n")
                    
                    # Generate visualization
                    subprocess.run("python3 scripts/visualize_correlations.py results/correlation_report.json", 
                                 shell=True, check=True, timeout=60)
                    log.write("Visualization generated\n")
                    
                except subprocess.TimeoutExpired:
                    log.write("Correlation analysis timeout\n")
                except subprocess.CalledProcessError as e:
                    log.write(f"Correlation analysis error: {e}\n")
            
            log.write(f"Discovery cycle completed: {datetime.now()}\n")
        
        print(f"Discovery cycle completed. Log: {log_file}")
        
        # Send notification if enabled
        if self.config['notifications']['enabled']:
            self.send_notification(f"Asset discovery completed at {datetime.now()}")
    
    def send_notification(self, message):
        """Send notification via webhook"""
        if self.config['notifications']['webhook_url']:
            try:
                import requests
                payload = {"text": message}
                requests.post(self.config['notifications']['webhook_url'], json=payload)
            except Exception as e:
                print(f"Notification failed: {e}")
    
    def start_scheduler(self):
        """Start the automated scheduler"""
        interval = self.config['schedule']['interval_hours']
        schedule.every(interval).hours.do(self.run_discovery_cycle)
        
        print(f"Scheduler started. Running every {interval} hours.")
        print("Press Ctrl+C to stop.")
        
        # Run initial discovery
        self.run_discovery_cycle()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automated Asset Discovery')
    parser.add_argument('--config', default='config/discovery_config.json', 
                       help='Configuration file path')
    parser.add_argument('--once', action='store_true', 
                       help='Run once instead of scheduling')
    
    args = parser.parse_args()
    
    # Create config directory
    os.makedirs('config', exist_ok=True)
    
    discovery = AutomatedAssetDiscovery(args.config)
    
    if args.once:
        discovery.run_discovery_cycle()
    else:
        discovery.start_scheduler()
