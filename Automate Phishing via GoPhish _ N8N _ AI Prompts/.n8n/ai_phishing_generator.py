#!/usr/bin/env python3
import requests
import json
import sys

def generate_phishing_content(target_company, campaign_type):
    prompt = f"""
    Create a professional phishing email for security awareness training targeting {target_company}.
    Campaign type: {campaign_type}
    
    Requirements:
    - Professional tone
    - Believable scenario
    - Clear call-to-action
    - Include subject line
    - For educational purposes only
    
    Format as JSON with 'subject' and 'body' fields.
    """
    
    payload = {
        "model": "llama2:7b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        result = response.json()
        return result['response']
    except Exception as e:
        return f"Error generating content: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ai_phishing_generator.py <company> <campaign_type>")
        sys.exit(1)
    
    company = sys.argv[1]
    campaign_type = sys.argv[2]
    
    content = generate_phishing_content(company, campaign_type)
    print(content)
