#!/usr/bin/env python3
import subprocess
import os
import sys
from llm_analyzer import LLMAnalyzer

class PatchAnalyzer:
    def __init__(self):
        self.llm = LLMAnalyzer()
    
    def extract_binary_info(self, binary_path):
        """Extract binary information using objdump"""
        try:
            result = subprocess.run(['objdump', '-d', binary_path], 
                                  capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error extracting binary info: {str(e)}"
    
    def compare_binaries(self, old_binary, new_binary):
        """Compare two binaries and identify differences"""
        old_info = self.extract_binary_info(old_binary)
        new_info = self.extract_binary_info(new_binary)
        
        # Simple diff approach
        old_lines = old_info.split('\n')
        new_lines = new_info.split('\n')
        
        differences = []
        max_lines = max(len(old_lines), len(new_lines))
        
        for i in range(max_lines):
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""
            
            if old_line != new_line:
                differences.append({
                    'line_num': i,
                    'old': old_line,
                    'new': new_line
                })
        
        return differences
    
    def analyze_security_implications(self, differences):
        """Analyze differences for security implications"""
        security_findings = []
        
        for diff in differences:
            old_line = diff['old'].lower()
            new_line = diff['new'].lower()
            
            # Look for security-relevant changes
            if 'strcpy' in old_line and 'strncpy' in new_line:
                security_findings.append({
                    'type': 'Buffer Overflow Fix',
                    'description': 'strcpy replaced with strncpy',
                    'risk_level': 'High',
                    'line': diff['line_num']
                })
            
            if 'malloc' in old_line or 'free' in new_line:
                security_findings.append({
                    'type': 'Memory Management',
                    'description': 'Memory allocation/deallocation change',
                    'risk_level': 'Medium',
                    'line': diff['line_num']
                })
        
        return security_findings
    
    def generate_report(self, old_binary, new_binary, output_file):
        """Generate comprehensive analysis report"""
        print(f"Analyzing patch differences between {old_binary} and {new_binary}")
        
        # Compare binaries
        differences = self.compare_binaries(old_binary, new_binary)
        security_findings = self.analyze_security_implications(differences)
        
        # Prepare diff content for LLM analysis
        diff_summary = f"Found {len(differences)} differences between binaries\n"
        diff_summary += f"Security findings: {len(security_findings)}\n\n"
        
        for finding in security_findings:
            diff_summary += f"- {finding['type']}: {finding['description']} (Risk: {finding['risk_level']})\n"
        
        # Get LLM analysis
        llm_analysis = self.llm.analyze_patch_diff(diff_summary, 
                                                  f"Comparing {old_binary} vs {new_binary}")
        
        # Generate report
        report = f"""
# Patch Analysis Report

## Binary Comparison
- Original: {old_binary}
- Patched: {new_binary}
- Differences Found: {len(differences)}

## Security Findings
"""
        
        for finding in security_findings:
            report += f"""
### {finding['type']}
- **Description**: {finding['description']}
- **Risk Level**: {finding['risk_level']}
- **Line**: {finding['line']}
"""
        
        report += f"""

## AI Analysis
{llm_analysis}

## Detailed Differences
"""
        
        for i, diff in enumerate(differences[:10]):  # Limit to first 10 differences
            report += f"""
### Difference {i+1} (Line {diff['line_num']})
**Before**: {diff['old'][:100]}...
**After**: {diff['new'][:100]}...
"""
        
        # Save report
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"Report saved to {output_file}")
        return report

if __name__ == "__main__":
    analyzer = PatchAnalyzer()
    
    if len(sys.argv) != 4:
        print("Usage: python3 patch_analyzer.py <old_binary> <new_binary> <output_report>")
        sys.exit(1)
    
    old_binary = sys.argv[1]
    new_binary = sys.argv[2]
    output_file = sys.argv[3]
    
    analyzer.generate_report(old_binary, new_binary, output_file)
