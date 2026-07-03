#!/usr/bin/env python3
import requests
import json
import sys

class LLMAnalyzer:
    def __init__(self, model="llama2:7b-chat"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
    
    def analyze_osint_data(self, data, analysis_type="summary"):
        prompts = {
            "summary": f"Analyze this OSINT data and provide a concise security summary: {data}",
            "threats": f"Identify potential security threats from this reconnaissance data: {data}",
            "recommendations": f"Provide security recommendations based on this OSINT information: {data}"
        }
        
        payload = {
            "model": self.model,
            "prompt": prompts.get(analysis_type, prompts["summary"]),
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Connection error: {str(e)}"

if __name__ == "__main__":
    analyzer = LLMAnalyzer()
    if len(sys.argv) > 1:
        result = analyzer.analyze_osint_data(sys.argv[1])
        print(result)
    else:
        print("Usage: python3 llm_analyzer.py 'data_to_analyze'")
