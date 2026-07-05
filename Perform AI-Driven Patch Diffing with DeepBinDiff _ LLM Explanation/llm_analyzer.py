#!/usr/bin/env python3
import requests
import json
import sys

class LLMAnalyzer:
    def __init__(self, model="codellama:7b"):
        self.model = model
        self.base_url = "http://localhost:11434/api/generate"
    
    def analyze_patch_diff(self, diff_content, context=""):
        prompt = f"""
        Analyze the following binary patch difference and explain:
        1. What changes were made
        2. Potential security implications
        3. Vulnerability assessment
        4. Risk level (Low/Medium/High)
        
        Context: {context}
        
        Patch Diff:
        {diff_content}
        
        Provide a concise technical analysis:
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                return json.loads(response.text)["response"]
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"LLM Analysis Error: {str(e)}"
    
    def explain_vulnerability(self, vuln_data):
        prompt = f"""
        Explain this vulnerability finding in simple terms:
        
        {vuln_data}
        
        Include:
        - What the vulnerability is
        - How it could be exploited
        - Recommended mitigation
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                return json.loads(response.text)["response"]
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Explanation Error: {str(e)}"

if __name__ == "__main__":
    analyzer = LLMAnalyzer()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
        result = analyzer.analyze_patch_diff(content)
        print(result)
