#!/usr/bin/env python3
import os
import sys
import subprocess
from llm_analyzer import LLMAnalyzer

class DeepPatchAnalyzer:
    def __init__(self):
        self.llm = LLMAnalyzer()
        self.deepbindiff_path = "/home/ubuntu/DeepBinDiff"
    
    def run_deepbindiff(self, binary1, binary2):
        """Run DeepBinDiff analysis"""
        try:
            cmd = [
                'python3', 
                f'{self.deepbindiff_path}/main.py',
                '--binary1', binary1,
                '--binary2', binary2,
                '--output', 'deep_analysis_result.json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  cwd=self.deepbindiff_path)
            return result.stdout, result.stderr
        except Exception as e:
            return "", f"DeepBinDiff error: {str(e)}"
    
    def analyze_with_ai(self, binary1, binary2):
        """Perform AI-driven analysis"""
        print("Starting AI-driven patch analysis...")
        
        # Run basic analysis
        stdout, stderr = self.run_deepbindiff(binary1, binary2)
        
        if stderr and "error" in stderr.lower():
            print(f"DeepBinDiff encountered issues: {stderr}")
            # Fallback to manual analysis
            return self.manual_analysis(binary1, binary2)
        
        # Analyze results with LLM
        analysis_context = f"""
        DeepBinDiff Analysis Results:
        STDOUT: {stdout}
        STDERR: {stderr}
        
        Binaries analyzed:
        - Original: {binary1}
        - Patched: {binary2}
        """
        
        ai_explanation = self.llm.analyze_patch_diff(analysis_context)
        
        return {
            'deepbindiff_output': stdout,
            'deepbindiff_errors': stderr,
            'ai_analysis': ai_explanation
        }
    
    def manual_analysis(self, binary1, binary2):
        """Manual analysis when DeepBinDiff fails"""
        print("Performing manual analysis...")
        
        # Use radare2 for analysis
        try:
            r2_cmd1 = f'r2 -qc "aa; pdf" {binary1}'
            r2_cmd2 = f'r2 -qc "aa; pdf" {binary2}'
            
            result1 = subprocess.run(r2_cmd1, shell=True, capture_output=True, text=True)
            result2 = subprocess.run(r2_cmd2, shell=True, capture_output=True, text=True)
            
            analysis_data = f"""
            Manual Binary Analysis:
            
            Binary 1 Analysis:
            {result1.stdout[:1000]}
            
            Binary 2 Analysis:
            {result2.stdout[:1000]}
            """
            
            ai_explanation = self.llm.analyze_patch_diff(analysis_data)
            
            return {
                'manual_analysis': True,
                'binary1_analysis': result1.stdout,
                'binary2_analysis': result2.stdout,
                'ai_analysis': ai_explanation
            }
            
        except Exception as e:
            return {'error': f'Manual analysis failed: {str(e)}'}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 deep_analysis.py <binary1> <binary2>")
        sys.exit(1)
    
    analyzer = DeepPatchAnalyzer()
    result = analyzer.analyze_with_ai(sys.argv[1], sys.argv[2])
    
    print("\n" + "="*50)
    print("AI-DRIVEN PATCH ANALYSIS RESULTS")
    print("="*50)
    
    if 'ai_analysis' in result:
        print("\nAI Analysis:")
        print(result['ai_analysis'])
    
    if 'deepbindiff_output' in result:
        print(f"\nDeepBinDiff Output:")
        print(result['deepbindiff_output'])
    
    if 'error' in result:
        print(f"\nError: {result['error']}")
