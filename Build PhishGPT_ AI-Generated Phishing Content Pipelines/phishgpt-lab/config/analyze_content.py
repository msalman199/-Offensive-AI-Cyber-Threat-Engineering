#!/usr/bin/env python3
import json
import os
from collections import Counter

class ContentAnalyzer:
    def __init__(self):
        self.output_dir = 'outputs'
        
    def analyze_campaigns(self):
        campaign_files = [f for f in os.listdir(f'{self.output_dir}/campaigns') 
                         if f.endswith('_summary.json')]
        
        total_campaigns = len(campaign_files)
        total_emails = 0
        total_sms = 0
        total_forms = 0
        
        campaign_types = Counter()
        
        for campaign_file in campaign_files:
            with open(f'{self.output_dir}/campaigns/{campaign_file}', 'r') as f:
                campaign = json.load(f)
                
            total_emails += len(campaign['results']['emails'])
            total_sms += len(campaign['results']['sms'])
            total_forms += len(campaign['results']['forms'])
            
            # Count campaign types
            config = campaign['config']
            if 'email_type' in config:
                campaign_types[config['email_type']] += 1
        
        print("=== PhishGPT Campaign Analysis ===")
        print(f"Total Campaigns: {total_campaigns}")
        print(f"Total Emails Generated: {total_emails}")
        print(f"Total SMS Generated: {total_sms}")
        print(f"Total Forms Generated: {total_forms}")
        print(f"Campaign Types: {dict(campaign_types)}")
        
        return {
            'campaigns': total_campaigns,
            'emails': total_emails,
            'sms': total_sms,
            'forms': total_forms,
            'types': dict(campaign_types)
        }

if __name__ == "__main__":
    analyzer = ContentAnalyzer()
    results = analyzer.analyze_campaigns()
