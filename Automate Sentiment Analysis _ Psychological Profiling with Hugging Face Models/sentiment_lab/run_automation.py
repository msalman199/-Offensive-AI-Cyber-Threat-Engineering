#!/usr/bin/env python3
import subprocess
import time
import schedule
from datetime import datetime

def run_phishing_analysis():
    """Run the phishing detection analysis"""
    print(f"[{datetime.now()}] Starting automated phishing analysis...")
    try:
        result = subprocess.run(['python3', 'phishing_detector.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Analysis completed successfully!")
        else:
            print(f"Analysis failed: {result.stderr}")
    except Exception as e:
        print(f"Error running analysis: {e}")

def show_dashboard():
    """Show monitoring dashboard"""
    print(f"[{datetime.now()}] Updating dashboard...")
    try:
        subprocess.run(['python3', 'monitoring_dashboard.py'])
    except Exception as e:
        print(f"Error showing dashboard: {e}")

if __name__ == "__main__":
    print("Automated Phishing Detection System")
    print("=" * 40)
    
    # Run initial analysis
    run_phishing_analysis()
    time.sleep(2)
    show_dashboard()
    
    print("\nAutomation system ready!")
    print("Analysis results are saved in the 'analysis_results' directory")
