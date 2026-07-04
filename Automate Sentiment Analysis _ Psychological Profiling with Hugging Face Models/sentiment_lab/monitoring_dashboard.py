import os
import json
import pandas as pd
from datetime import datetime, timedelta
import glob

class MonitoringDashboard:
    def __init__(self, results_dir="analysis_results"):
        self.results_dir = results_dir
    
    def load_recent_analyses(self, days=7):
        """Load analyses from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        json_files = glob.glob(f"{self.results_dir}/phishing_analysis_*.json")
        recent_analyses = []
        
        for file_path in json_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    report_time = datetime.fromisoformat(data['report_timestamp'])
                    if report_time >= cutoff_date:
                        recent_analyses.append(data)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return recent_analyses
    
    def generate_dashboard_summary(self):
        """Generate dashboard summary"""
        analyses = self.load_recent_analyses()
        
        if not analyses:
            print("No recent analyses found.")
            return
        
        total_emails = sum(a['analysis_summary']['total_emails'] for a in analyses)
        total_high_risk = sum(a['analysis_summary']['high_risk'] for a in analyses)
        total_medium_risk = sum(a['analysis_summary']['medium_risk'] for a in analyses)
        total_low_risk = sum(a['analysis_summary']['low_risk'] for a in analyses)
        
        print("Phishing Detection Dashboard")
        print("=" * 50)
        print(f"Analysis Period: Last 7 days")
        print(f"Total Analyses: {len(analyses)}")
        print(f"Total Emails Processed: {total_emails}")
        print(f"High Risk Emails: {total_high_risk} ({total_high_risk/total_emails*100:.1f}%)")
        print(f"Medium Risk Emails: {total_medium_risk} ({total_medium_risk/total_emails*100:.1f}%)")
        print(f"Low Risk Emails: {total_low_risk} ({total_low_risk/total_emails*100:.1f}%)")
        
        # Show recent high-risk emails
        print("\nRecent High-Risk Emails:")
        print("-" * 30)
        
        for analysis in analyses[-3:]:  # Show last 3 analyses
            high_risk_emails = [r for r in analysis['detailed_results'] if r['risk_level'] == 'HIGH RISK']
            for email in high_risk_emails[:2]:  # Show top 2 high-risk emails per analysis
                print(f"Subject: {email['subject']}")
                print(f"Threat Score: {email['threat_score']:.1f}/100")
                print(f"Sender: {email['sender']}")
                print()

if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    dashboard.generate_dashboard_summary()
