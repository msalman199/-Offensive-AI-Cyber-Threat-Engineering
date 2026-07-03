#!/usr/bin/env python3
import sys
import time
from recon_pipeline import ReconPipeline

def batch_reconnaissance(targets_file):
    pipeline = ReconPipeline()
    
    with open(targets_file, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]
    
    for target in targets:
        print(f"\n{'='*50}")
        print(f"Processing target: {target}")
        print(f"{'='*50}")
        
        if pipeline.run_spiderfoot_scan(target):
            analysis = pipeline.analyze_results()
            if analysis:
                pipeline.generate_report(target, analysis)
            time.sleep(10)  # Delay between scans
        else:
            print(f"Failed to scan {target}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 batch_recon.py targets.txt")
        sys.exit(1)
    
    batch_reconnaissance(sys.argv[1])
