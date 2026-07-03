#!/usr/bin/env python3
import subprocess
import json
import time
import sys
from datetime import datetime

def run_complete_pipeline(target):
    """Execute complete automated pipeline"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"[{datetime.now()}] Starting automated pipeline for {target}")
    
    # Step 1: Run Nmap scan
    print("Step 1: Running Nmap scan...")
    scan_result = subprocess.run([
        'python3', 'scripts/nmap_scanner.py', target
    ], capture_output=True, text=True)
    
    if scan_result.returncode != 0:
        print(f"Nmap scan failed: {scan_result.stderr}")
        return False
    
    # Step 2: Find the generated JSON file
    target_safe = target.replace('/', '_').replace('.', '_')
    json_file = f"data/scan_{target_safe}.json"
    
    # Step 3: Run RAG analysis
    print("Step 2: Running RAG analysis...")
    rag_result = subprocess.run([
        'python3', 'scripts/rag_analyzer.py', json_file
    ], capture_output=True, text=True)
    
    if rag_result.returncode != 0:
        print(f"RAG analysis failed: {rag_result.stderr}")
        return False
    
    # Step 4: Send to N8N (if running)
    print("Step 3: Sending to N8N workflow...")
    try:
        with open(json_file, 'r') as f:
            scan_data = json.load(f)
        
        n8n_result = subprocess.run([
            'curl', '-X', 'POST', 'http://localhost:5678/webhook/nmap-scan',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(scan_data)
        ], capture_output=True, text=True, timeout=10)
        
        if n8n_result.returncode == 0:
            print("Successfully sent data to N8N")
        else:
            print("N8N webhook not available (this is optional)")
    
    except Exception as e:
        print(f"N8N integration skipped: {e}")
    
    print(f"[{datetime.now()}] Pipeline completed successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 automated_pipeline.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    success = run_complete_pipeline(target)
    sys.exit(0 if success else 1)
