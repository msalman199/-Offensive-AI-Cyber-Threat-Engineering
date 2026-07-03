#!/usr/bin/env python3
import os
import json
import subprocess

def verify_installation():
    """Verify all tools are installed"""
    tools = ['nmap', 'python3', 'curl', 'docker']
    missing = []
    
    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0:
            missing.append(tool)
    
    if missing:
        print(f"Missing tools: {', '.join(missing)}")
        return False
    
    print("✓ All required tools installed")
    return True

def verify_outputs():
    """Verify expected output files exist"""
    expected_files = [
        'data/scan_127_0_0_1.json',
        'data/vulnerability_kb.json'
    ]
    
    missing = []
    for file in expected_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"Missing output files: {', '.join(missing)}")
        return False
    
    print("✓ All expected output files present")
    return True

def verify_data_quality():
    """Verify data quality in output files"""
    try:
        with open('data/scan_127_0_0_1.json', 'r') as f:
            scan_data = json.load(f)
        
        if 'hosts' not in scan_data or len(scan_data['hosts']) == 0:
            print("✗ Scan data appears incomplete")
            return False
        
        print(f"✓ Scan data contains {len(scan_data['hosts'])} hosts")
        
        # Check for RAG analysis files
        rag_files = [f for f in os.listdir('data/') if f.startswith('rag_analysis_')]
        if rag_files:
            print(f"✓ RAG analysis completed ({len(rag_files)} files)")
        else:
            print("✗ No RAG analysis files found")
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ Error verifying data quality: {e}")
        return False

if __name__ == "__main__":
    print("=== Lab Verification ===")
    
    checks = [
        verify_installation(),
        verify_outputs(),
        verify_data_quality()
    ]
    
    if all(checks):
        print("\n🎉 Lab completed successfully!")
        print("All components are working correctly.")
    else:
        print("\n❌ Lab verification failed.")
        print("Please review the steps and try again.")
