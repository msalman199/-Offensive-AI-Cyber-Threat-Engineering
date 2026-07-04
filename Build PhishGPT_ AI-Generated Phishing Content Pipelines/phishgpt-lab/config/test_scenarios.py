#!/usr/bin/env python3
import json
from phishing_pipeline import PhishingPipeline

def run_banking_scenario():
    print("=== Banking Phishing Scenario ===")
    pipeline = PhishingPipeline()
    
    targets = [
        {'name': 'Michael Johnson', 'email': 'michael@company.com', 'phone': '+1555123456'},
        {'name': 'Sarah Wilson', 'email': 'sarah@business.com', 'phone': '+1555654321'}
    ]
    
    config = {
        'content_types': ['email', 'sms', 'form'],
        'email_type': 'banking',
        'sms_type': 'banking',
        'form_type': 'login'
    }
    
    return pipeline.run_campaign(targets, config)

def run_social_scenario():
    print("=== Social Media Phishing Scenario ===")
    pipeline = PhishingPipeline()
    
    targets = [
        {'name': 'David Brown', 'email': 'david@email.com', 'phone': '+1555789012'}
    ]
    
    config = {
        'content_types': ['email', 'form'],
        'email_type': 'social',
        'form_type': 'survey'
    }
    
    return pipeline.run_campaign(targets, config)

def run_corporate_scenario():
    print("=== Corporate Phishing Scenario ===")
    pipeline = PhishingPipeline()
    
    targets = [
        {'name': 'Lisa Davis', 'email': 'lisa@corp.com', 'phone': '+1555345678'}
    ]
    
    config = {
        'content_types': ['email', 'sms', 'form'],
        'email_type': 'corporate',
        'sms_type': 'delivery',
        'form_type': 'support'
    }
    
    return pipeline.run_campaign(targets, config)

if __name__ == "__main__":
    scenarios = [
        run_banking_scenario,
        run_social_scenario,
        run_corporate_scenario
    ]
    
    for scenario in scenarios:
        try:
            result = scenario()
            print(f"Scenario completed successfully\n")
        except Exception as e:
            print(f"Scenario failed: {e}\n")
