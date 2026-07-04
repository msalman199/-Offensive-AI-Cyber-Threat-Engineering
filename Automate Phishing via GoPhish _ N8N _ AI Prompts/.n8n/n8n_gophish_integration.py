#!/usr/bin/env python3
import requests
import json
import subprocess

class GoPhishN8NIntegration:
    def __init__(self):
        self.gophish_url = "http://localhost:3333"
        self.n8n_url = "http://localhost:5678"
        self.api_key = self.get_gophish_api_key()
    
    def get_gophish_api_key(self):
        # Extract API key from GoPhish logs
        try:
            with open('/opt/gophish/gophish.log', 'r') as f:
                for line in f:
                    if 'Please login with the username admin and the password' in line:
                        return line.split()[-1]
        except:
            return "default_api_key"
    
    def create_campaign(self, name, template_content):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Create email template
        template_data = {
            "name": f"{name}_template",
            "subject": template_content.get('subject', 'Important Update'),
            "text": template_content.get('body', 'Default body'),
            "html": f"<html><body>{template_content.get('body', 'Default body')}</body></html>"
        }
        
        response = requests.post(
            f"{self.gophish_url}/api/templates/",
            headers=headers,
            json=template_data
        )
        
        return response.json()
    
    def trigger_n8n_workflow(self, webhook_url, data):
        return requests.post(webhook_url, json=data)

if __name__ == "__main__":
    integration = GoPhishN8NIntegration()
    
    # Generate AI content
    ai_content = subprocess.check_output([
        'python3', 'ai_phishing_generator.py', 
        'TechCorp', 'credential_harvesting'
    ]).decode('utf-8')
    
    print("AI Generated Content:", ai_content)
    
    # Create campaign
    template_data = {
        'subject': 'Urgent: Account Verification Required',
        'body': ai_content
    }
    
    result = integration.create_campaign("automated_test", template_data)
    print("Campaign created:", result)
