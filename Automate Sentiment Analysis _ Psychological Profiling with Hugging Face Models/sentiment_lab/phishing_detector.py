# phishing_detector.py
from integrated_analyzer import IntegratedAnalyzer
import pandas as pd
import json
import os
from datetime import datetime
import re

class PhishingDetector:
    def __init__(self):
        self.analyzer = IntegratedAnalyzer()
        self.results_dir = "analysis_results"
        os.makedirs(self.results_dir, exist_ok=True)
    
    def load_email_samples(self, file_path=None):
        """Load email samples for analysis"""
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            # Create sample phishing emails for testing
            return [
                {
                    "id": 1,
                    "subject": "Urgent: Your Account Will Be Closed",
                    "body": "Dear Customer, Your account will be permanently closed in 24 hours unless you verify your information immediately. Click here to prevent account closure. This is your final warning!",
                    "sender": "security@fake-bank.com"
                },
                {
                    "id": 2,
                    "subject": "Congratulations! You've Won!",
                    "body": "You are our lucky winner! You've won $5000 cash prize! Click here now to claim your reward. Limited time offer - act fast!",
                    "sender": "winner@lottery-fake.com"
                },
                {
                    "id": 3,
                    "subject": "Meeting Reminder",
                    "body": "Hi, just a friendly reminder about our meeting tomorrow at 2 PM. Please let me know if you need to reschedule. Thanks!",
                    "sender": "colleague@company.com"
                },
                {
                    "id": 4,
                    "subject": "IRS Tax Notice",
                    "body": "IMMEDIATE ACTION REQUIRED: You owe $2,847 in back taxes. Pay now to avoid arrest warrant. Call 1-800-FAKE-IRS immediately!",
                    "sender": "notices@fake-irs.gov"
                }
            ]
    
    def analyze_email_batch(self, emails):
        """Analyze a batch of emails for phishing indicators"""
        results = []
        
        for email in emails:
            # Combine subject and body for analysis
            full_text = f"{email['subject']} {email['body']}"
            
            analysis = self.analyzer.comprehensive_analysis(full_text)
            
            # Add email metadata
            analysis['email_id'] = email['id']
            analysis['subject'] = email['subject']
            analysis['sender'] = email['sender']
            analysis['body_preview'] = email['body'][:100] + "..."
            
            results.append(analysis)
        
        return results
    
    def generate_report(self, results):
        """Generate comprehensive analysis report"""
        report = {
            'analysis_summary': {
                'total_emails': len(results),
                'high_risk': len([r for r in results if r['risk_level'] == 'HIGH RISK']),
                'medium_risk': len([r for r in results if r['risk_level'] == 'MEDIUM RISK']),
                'low_risk': len([r for r in results if r['risk_level'] == 'LOW RISK']),
                'average_threat_score': sum(r['threat_score'] for r in results) / len(results)
            },
            'detailed_results': results,
            'report_timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def save_results(self, report):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_file = f"{self.results_dir}/phishing_analysis_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save CSV summary
        csv_data = []
        for result in report['detailed_results']:
            csv_data.append({
                'Email_ID': result['email_id'],
                'Subject': result['subject'],
                'Sender': result['sender'],
                'Sentiment': result['sentiment_analysis']['sentiment'],
                'Emotion': result['sentiment_analysis']['emotion'],
                'Manipulation_Score': result['psychological_profile']['manipulation_score'],
                'Threat_Score': result['threat_score'],
                'Risk_Level': result['risk_level']
            })
        
        df = pd.DataFrame(csv_data)
        csv_file = f"{self.results_dir}/phishing_summary_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        
        return json_file, csv_file
    
    def run_automated_analysis(self):
        """Run complete automated phishing analysis"""
        print("Starting Automated Phishing Detection Analysis...")
        print("=" * 60)
        
        # Load email samples
        emails = self.load_email_samples()
        print(f"Loaded {len(emails)} email samples for analysis")
        
        # Analyze emails
        print("Analyzing emails...")
        results = self.analyze_email_batch(emails)
        
        # Generate report
        report = self.generate_report(results)
        
        # Save results
        json_file, csv_file = self.save_results(report)
        
        # Display summary
        print("\nAnalysis Complete!")
        print(f"Total Emails Analyzed: {report['analysis_summary']['total_emails']}")
        print(f"High Risk: {report['analysis_summary']['high_risk']}")
        print(f"Medium Risk: {report['analysis_summary']['medium_risk']}")
        print(f"Low Risk: {report['analysis_summary']['low_risk']}")
        print(f"Average Threat Score: {report['analysis_summary']['average_threat_score']:.1f}/100")
        print(f"\nResults saved to:")
        print(f"- JSON Report: {json_file}")
        print(f"- CSV Summary: {csv_file}")
        
        return report

if __name__ == "__main__":
    detector = PhishingDetector()
    report = detector.run_automated_analysis()
    
    # Display detailed results
    print("\nDetailed Analysis Results:")
    print("=" * 80)
    
    for result in report['detailed_results']:
        print(f"\nEmail ID: {result['email_id']}")
        print(f"Subject: {result['subject']}")
        print(f"Sender: {result['sender']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Threat Score: {result['threat_score']:.1f}/100")
        print(f"Manipulation Score: {result['psychological_profile']['manipulation_score']:.1f}/100")
        print(f"Sentiment: {result['sentiment_analysis']['sentiment']}")
        print(f"Primary Emotion: {result['sentiment_analysis']['emotion']}")
        print("-" * 60)
