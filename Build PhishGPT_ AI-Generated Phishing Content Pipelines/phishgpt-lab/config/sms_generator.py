#!/usr/bin/env python3
import json
from phishgpt_engine import PhishGPTEngine
from datetime import datetime

class SMSGenerator:
    def __init__(self):
        self.engine = PhishGPTEngine()
        
    def generate_phishing_sms(self, target_data, campaign_type):
        scenarios = {
            'banking': {
                'sender': 'BANK-ALERT',
                'topic': 'account suspended - verify immediately',
                'urgency': 'high'
            },
            'delivery': {
                'sender': 'DELIVERY',
                'topic': 'package delivery failed - reschedule',
                'urgency': 'medium'
            },
            'prize': {
                'sender': 'WINNER',
                'topic': 'congratulations you won - claim prize',
                'urgency': 'high'
            }
        }
        
        scenario = scenarios.get(campaign_type, scenarios['banking'])
        
        # Generate SMS content
        content = self.engine.generate_content('sms', target_data, scenario)
        
        # Create SMS structure
        sms_data = {
            'timestamp': datetime.now().isoformat(),
            'target': target_data,
            'campaign_type': campaign_type,
            'sender': scenario['sender'],
            'content': content[0][:160] if content else "Generated content unavailable",
            'urgency': scenario['urgency'],
            'link': f"https://secure-verify-{campaign_type}.com/verify?id=12345"
        }
        
        return sms_data

if __name__ == "__main__":
    generator = SMSGenerator()
    target = {'name': 'Jane Smith', 'phone': '+1234567890'}
    sms = generator.generate_phishing_sms(target, 'banking')
    print(json.dumps(sms, indent=2))
