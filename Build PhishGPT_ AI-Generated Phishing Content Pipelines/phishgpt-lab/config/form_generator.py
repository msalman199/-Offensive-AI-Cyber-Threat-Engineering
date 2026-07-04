#!/usr/bin/env python3
import json
from phishgpt_engine import PhishGPTEngine
from datetime import datetime

class FormGenerator:
    def __init__(self):
        self.engine = PhishGPTEngine()
        
    def generate_phishing_form(self, target_data, form_type):
        scenarios = {
            'login': {
                'sender': 'Security Team',
                'topic': 'account verification login form',
                'fields': ['username', 'password', 'email']
            },
            'survey': {
                'sender': 'Research Team',
                'topic': 'customer satisfaction survey',
                'fields': ['name', 'email', 'phone', 'feedback']
            },
            'support': {
                'sender': 'Technical Support',
                'topic': 'technical support request form',
                'fields': ['name', 'email', 'issue', 'account_id']
            }
        }
        
        scenario = scenarios.get(form_type, scenarios['login'])
        
        # Generate form content
        content = self.engine.generate_content('form', target_data, scenario)
        
        # Create form structure
        form_data = {
            'timestamp': datetime.now().isoformat(),
            'target': target_data,
            'form_type': form_type,
            'title': f"{form_type.title()} Verification",
            'description': content[0] if content else "Please complete the form below",
            'fields': scenario['fields'],
            'html_form': self.create_html_form(scenario['fields'], content[0] if content else "")
        }
        
        return form_data
        
    def create_html_form(self, fields, description):
        form_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto;">
            <h2>Account Verification</h2>
            <p>{description}</p>
            <form method="post" action="/submit">
        """
        
        for field in fields:
            field_type = 'password' if field == 'password' else 'text'
            form_html += f"""
                <div style="margin: 15px 0;">
                    <label for="{field}">{field.replace('_', ' ').title()}:</label><br>
                    <input type="{field_type}" id="{field}" name="{field}" 
                           style="width: 100%; padding: 8px; margin: 5px 0;" required>
                </div>
            """
        
        form_html += """
                <button type="submit" style="background-color: #007bff; color: white; 
                        padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                    Submit
                </button>
            </form>
        </body>
        </html>
        """
        
        return form_html

if __name__ == "__main__":
    generator = FormGenerator()
    target = {'name': 'Alice Johnson', 'email': 'alice@example.com'}
    form = generator.generate_phishing_form(target, 'login')
    print(json.dumps(form, indent=2))
