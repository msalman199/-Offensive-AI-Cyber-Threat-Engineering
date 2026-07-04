#!/usr/bin/env python3
import openai
import json
import sys
import os
from datetime import datetime

class PhishingContentGenerator:
    def __init__(self):
        # Using a local LLM endpoint or mock for educational purposes
        self.base_prompts = {
            "urgent_security": "Create an urgent security alert email that appears to be from IT department requiring immediate password reset",
            "invoice_scam": "Generate a fake invoice email from a well-known service requesting payment verification",
            "social_media": "Create a social media notification about suspicious account activity",
            "package_delivery": "Generate a package delivery notification requiring address confirmation"
        }
    
    def generate_content(self, prompt_type, target_company="TechCorp", target_name="User"):
        """Generate phishing content based on prompt type"""
        if prompt_type not in self.base_prompts:
            return None
        
        # Simulate AI-generated content (replace with actual LLM API call)
        templates = {
            "urgent_security": f"""
Subject: URGENT: Security Alert for {target_name}

Dear {target_name},

Our security systems have detected unusual activity on your {target_company} account. 
To protect your account, please verify your credentials immediately.

Click here to secure your account: [MALICIOUS_LINK]

This link will expire in 24 hours.

Best regards,
{target_company} Security Team
            """,
            "invoice_scam": f"""
Subject: Invoice #INV-{datetime.now().strftime('%Y%m%d')} - Payment Required

Dear {target_name},

Your recent purchase requires payment verification. Please review the attached invoice.

Amount Due: $299.99
Due Date: {datetime.now().strftime('%Y-%m-%d')}

Verify Payment: [MALICIOUS_LINK]

{target_company} Billing Department
            """,
            "social_media": f"""
Subject: Suspicious Login Detected

Hi {target_name},

We detected a login to your account from an unrecognized device.

Location: Unknown
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

If this wasn't you, secure your account: [MALICIOUS_LINK]

Social Media Security Team
            """,
            "package_delivery": f"""
Subject: Package Delivery Attempt Failed

Dear {target_name},

We attempted to deliver your package but need to confirm your address.

Tracking: PKG{datetime.now().strftime('%Y%m%d')}123
Delivery Company: FastShip Express

Update delivery address: [MALICIOUS_LINK]

FastShip Customer Service
            """
        }
        
        return templates.get(prompt_type, "")
    
    def save_content(self, content, filename):
        """Save generated content to file"""
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Content saved to {filename}")

def main():
    generator = PhishingContentGenerator()
    
    print("AI-Based Phishing Content Generator")
    print("Available prompt types:")
    for key in generator.base_prompts.keys():
        print(f"- {key}")
    
    prompt_type = input("\nEnter prompt type: ").strip()
    target_company = input("Enter target company (default: TechCorp): ").strip() or "TechCorp"
    target_name = input("Enter target name (default: User): ").strip() or "User"
    
    content = generator.generate_content(prompt_type, target_company, target_name)
    
    if content:
        filename = f"phishing_{prompt_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        generator.save_content(content, filename)
        print(f"\nGenerated content:\n{content}")
    else:
        print("Invalid prompt type!")

if __name__ == "__main__":
    main()
