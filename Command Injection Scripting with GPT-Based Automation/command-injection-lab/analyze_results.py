import json
import glob
import sys

def analyze_latest_report():
    report_files = glob.glob("results/automated_report_*.json")
    if not report_files:
        print("No report files found")
        return
    
    latest_report = max(report_files)
    
    with open(latest_report, 'r') as f:
        report = json.load(f)
    
    print("COMMAND INJECTION ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Target: {report['scan_info']['target']}")
    print(f"Scan Time: {report['scan_info']['timestamp']}")
    print(f"Total Tests: {report['scan_info']['total_tests']}")
    print(f"Vulnerable Tests: {report['scan_info']['vulnerable_tests']}")
    print(f"Risk Level: {report['summary']['risk_level']}")
    
    if report['summary']['vulnerability_found']:
        print("\nVULNERABLE PAYLOADS DETECTED:")
        print("-" * 30)
        for result in report['detailed_results']:
            if result.get('analysis', {}).get('vulnerable', False):
                payload = result.get('payload', 'Unknown')
                confidence = result.get('analysis', {}).get('confidence', 0)
                print(f"• {payload[:60]}... (Confidence: {confidence}%)")
    
    print(f"\nFull report: {latest_report}")

if __name__ == "__main__":
    analyze_latest_report()
