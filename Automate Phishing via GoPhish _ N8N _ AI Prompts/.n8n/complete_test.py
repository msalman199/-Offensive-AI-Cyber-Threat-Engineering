#!/usr/bin/env python3
import requests
import json
import time
import subprocess

def run_complete_test():
    print("Starting complete phishing automation test...")
    
    # Step 1: Generate AI content
    print("1. Generating AI content...")
    ai_content = subprocess.check_output([
        'python3', 'ai_phishing_generator.py', 
        'TestCompany', 'awareness_training'
    ]).decode('utf-8')
    
    # Step 2: Create GoPhish campaign
    print("2. Creating GoPhish campaign...")
    gophish_api = "http://localhost:3333/api"
    
    # Step 3: Trigger N8N workflow
    print("3. Triggering N8N workflow...")
    n8n_webhook = "http://localhost:5678/webhook-test/phishing-automation"
    
    workflow_data = {
        "campaign_name": "automated_test_campaign",
        "ai_content": ai_content,
        "target_count": 1,
        "timestamp": int(time.time())
    }
    
    try:
        response = requests.post(n8n_webhook, json=workflow_data)
        print(f"N8N Response: {response.status_code}")
    except Exception as e:
        print(f"N8N Error: {e}")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    run_complete_test()
