#!/usr/bin/env python3
import json
import os
from datetime import datetime
from email_generator import EmailGenerator
from sms_generator import SMSGenerator
from form_generator import FormGenerator

class PhishingPipeline:
    def __init__(self):
        self.email_gen = EmailGenerator()
        self.sms_gen = SMSGenerator()
        self.form_gen = FormGenerator()
        self.ensure_output_dirs()
        
    def ensure_output_dirs(self):
        os.makedirs('outputs/emails', exist_ok=True)
        os.makedirs('outputs/sms', exist_ok=True)
        os.makedirs('outputs/forms', exist_ok=True)
        os.makedirs('outputs/campaigns', exist_ok=True)
        
    def run_campaign(self, targets, campaign_config):
        campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        campaign_results = {
            'campaign_id': campaign_id,
            'timestamp': datetime.now().isoformat(),
            'config': campaign_config,
            'targets': len(targets),
            'results': {
                'emails': [],
                'sms': [],
                'forms': []
            }
        }
        
        print(f"Starting campaign: {campaign_id}")
        
        for target in targets:
            print(f"Processing target: {target['name']}")
            
            # Generate email content
            if 'email' in campaign_config['content_types']:
                email = self.email_gen.generate_phishing_email(
                    target, campaign_config['email_type']
                )
                campaign_results['results']['emails'].append(email)
                self.save_content('emails', f"{campaign_id}_{target['name']}_email.json", email)
                
            # Generate SMS content
            if 'sms' in campaign_config['content_types']:
                sms = self.sms_gen.generate_phishing_sms(
                    target, campaign_config['sms_type']
                )
                campaign_results['results']['sms'].append(sms)
                self.save_content('sms', f"{campaign_id}_{target['name']}_sms.json", sms)
                
            # Generate form content
            if 'form' in campaign_config['content_types']:
                form = self.form_gen.generate_phishing_form(
                    target, campaign_config['form_type']
                )
                campaign_results['results']['forms'].append(form)
                self.save_content('forms', f"{campaign_id}_{target['name']}_form.json", form)
                self.save_html_form(f"{campaign_id}_{target['name']}_form.html", form['html_form'])
        
        # Save campaign summary
        self.save_content('campaigns', f"{campaign_id}_summary.json", campaign_results)
        print(f"Campaign completed: {campaign_id}")
        return campaign_results
        
    def save_content(self, content_type, filename, data):
        filepath = f"outputs/{content_type}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def save_html_form(self, filename, html_content):
        filepath = f"outputs/forms/{filename}"
        with open(filepath, 'w') as f:
            f.write(html_content)

if __name__ == "__main__":
    pipeline = PhishingPipeline()
    
    # Sample targets
    targets = [
        {'name': 'John Doe', 'email': 'john@example.com', 'phone': '+1234567890'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '+0987654321'}
    ]
    
    # Campaign configuration
    config = {
        'content_types': ['email', 'sms', 'form'],
        'email_type': 'banking',
        'sms_type': 'banking',
        'form_type': 'login'
    }
    
    # Run campaign
    results = pipeline.run_campaign(targets, config)
    print(f"Generated {len(results['results']['emails'])} emails")
    print(f"Generated {len(results['results']['sms'])} SMS messages")
    print(f"Generated {len(results['results']['forms'])} forms")
