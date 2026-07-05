#!/usr/bin/env python3
import json
import os
from datetime import datetime
from llm_analyzer import LLMAnalyzer

def generate_executive_summary():
    llm = LLMAnalyzer()
    
    # Read previous analysis results
    analysis_files = ['analysis_report.md']
    combined_analysis = ""
    
    for file in analysis_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                combined_analysis += f.read() + "\n\n"
    
    # Generate executive summary
    summary_prompt = f"""
    Based on the following patch analysis results, create an executive summary that includes:
    1. Key vulnerabilities found
    2. Security improvements made
    3. Risk assessment
    4. Recommendations
    
    Analysis Data:
    {combined_analysis}
    """
    
    executive_summary = llm.analyze_patch_diff(summary_prompt, "Executive Summary Generation")
    
    # Create final report
    final_report = f"""
# AI-Driven Patch Analysis - Final Report
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
{executive_summary}

## Technical Analysis Details
{combined_analysis}

## Methodology
This analysis was performed using:
- DeepBinDiff for binary comparison
- Local LLM (CodeLlama) for vulnerability explanation
- Custom Python scripts for integration
- Radare2 for binary analysis

## Tools Used
- **DeepBinDiff**: AI-powered binary diffing
- **Ollama + CodeLlama**: Local LLM for explanations
- **Radare2**: Binary analysis framework
- **Custom Scripts**: Integration and automation
"""
    
    with open('final_patch_analysis_report.md', 'w') as f:
        f.write(final_report)
    
    print("Final report generated: final_patch_analysis_report.md")
    print("\nExecutive Summary:")
    print(executive_summary)

if __name__ == "__main__":
    generate_executive_summary()
