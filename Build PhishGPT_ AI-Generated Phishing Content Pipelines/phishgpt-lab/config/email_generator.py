#!/usr/bin/env python3
import json
from phishgpt_engine import PhishGPTEngine
from datetime import datetime

class EmailGenerator:
    def __init__(self):
        self.engine = PhishGPTEngine()
        
    def generate_phishing_email(self, target_data, campaign_type):
        scenarios = {
            'banking': {
                'sender': 'security@bank-alerts.com',
                'topic': 'account security verification required',
                'subject_templates': [
                    'Urgent: Account Security Alert',
                    'Action Required: Verify Your Account',
                    'Security Notice: Unusual Activity Detected'
                ]
            },
            'social': {
                'sender': 'notifications@social-network.com',
                'topic': 'account login from new device',
                'subject_templates': [
                    'New Login Alert',
                    'Security: Unrecognized Device Access',
                    'Account Access Notification'
                ]
            },
            'corporate': {
                'sender': 'it-support@company.com',
                'topic': 'mandatory security update required',
                'subject_templates': [
                    'IT Security Update Required',
                    'Mandatory: System Security Patch',
                    'Action Required: Security Compliance'
                ]
            }
        }
        
        scenario = scenarios.get(campaign_type, scenarios['banking'])
        
        # Generate email content
        content = self.engine.generate_content('email', target_data, scenario)
        
        # Create complete email structure
        email_data = {
            'timestamp': datetime.now().isoformat(),
            'target': target_data,
            'campaign_type': campaign_type,
            'sender': scenario['sender'],
            'subject': scenario['subject_templates'][0],
            'content': content[0] if content else "Generated content unavailable",
            'html_template': self.create_html_template(content[0] if content else "")
        }
        
        return email_data
        
    def create_html_template(self, content):
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <p>{content}</p>
                <br>
                <a href="#" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Verify Account
                </a>
            </div>
        </body>
        </html>
        """

if __name__ == "__main__":
    generator = EmailGenerator()
    target = {'name': 'John Doe', 'email': 'john.doe@example.com'}
    email = generator.generate_phishing_email(target, 'banking')
    print(json.dumps(email, indent=2))
