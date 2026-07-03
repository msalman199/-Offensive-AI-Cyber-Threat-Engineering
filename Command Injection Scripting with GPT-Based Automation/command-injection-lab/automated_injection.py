#!/usr/bin/env python3
import argparse
import json
import time
from datetime import datetime
from injection_tester import CommandInjectionTester
from gpt_automation import GPTCommandInjectionFramework

class AutomatedInjectionSuite:
    def __init__(self, target_url, output_dir="results"):
        self.target_url = target_url
        self.output_dir = output_dir
        self.tester = CommandInjectionTester(target_url)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_report(self, results):
        vulnerable_tests = [r for r in results if r.get("analysis", {}).get("vulnerable", False)]
        
        report = {
            "scan_info": {
                "target": self.target_url,
                "timestamp": self.timestamp,
                "total_tests": len(results),
                "vulnerable_tests": len(vulnerable_tests)
            },
            "summary": {
                "vulnerability_found": len(vulnerable_tests) > 0,
                "risk_level": "HIGH" if len(vulnerable_tests) > 3 else "MEDIUM" if len(vulnerable_tests) > 0 else "LOW"
            },
            "detailed_results": results,
            "recommendations": [
                "Implement input validation and sanitization",
                "Use parameterized queries and safe APIs",
                "Apply principle of least privilege",
                "Regular security testing and code review"
            ]
        }
        
        return report
    
    def run_full_automation(self):
        print(f"Starting automated command injection testing on {self.target_url}")
        print("=" * 60)
        
        # Run tests
        results = self.tester.run_automated_test(["basic", "advanced"])
        
        # Generate report
        report = self.generate_report(results)
        
        # Save results
        report_file = f"{self.output_dir}/automated_report_{self.timestamp}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 60)
        print("AUTOMATION COMPLETE")
        print("=" * 60)
        print(f"Target: {self.target_url}")
        print(f"Total Tests: {report['scan_info']['total_tests']}")
        print(f"Vulnerable Tests: {report['scan_info']['vulnerable_tests']}")
        print(f"Risk Level: {report['summary']['risk_level']}")
        print(f"Report saved: {report_file}")
        
        return report

def main():
    parser = argparse.ArgumentParser(description="Automated Command Injection Testing Suite")
    parser.add_argument("--target", default="http://localhost:8080", help="Target URL")
    parser.add_argument("--output", default="results", help="Output directory")
    
    args = parser.parse_args()
    
    suite = AutomatedInjectionSuite(args.target, args.output)
    report = suite.run_full_automation()

if __name__ == "__main__":
    main()
