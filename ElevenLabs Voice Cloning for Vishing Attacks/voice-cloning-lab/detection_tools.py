#!/usr/bin/env python3
import os
import subprocess
from pydub import AudioSegment
import json

class VoiceAnalyzer:
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_audio_properties(self, audio_file):
        """Analyze basic audio properties"""
        try:
            audio = AudioSegment.from_file(audio_file)
            
            properties = {
                "duration_seconds": len(audio) / 1000.0,
                "frame_rate": audio.frame_rate,
                "channels": audio.channels,
                "sample_width": audio.sample_width,
                "max_amplitude": audio.max,
                "rms": audio.rms
            }
            
            print(f"Audio Properties for {audio_file}:")
            for key, value in properties.items():
                print(f"  {key}: {value}")
            
            return properties
        except Exception as e:
            print(f"Error analyzing {audio_file}: {e}")
            return None
    
    def compare_audio_files(self, original_file, cloned_file):
        """Compare original and cloned audio properties"""
        print(f"\nComparing {original_file} vs {cloned_file}")
        
        original_props = self.analyze_audio_properties(original_file)
        cloned_props = self.analyze_audio_properties(cloned_file)
        
        if original_props and cloned_props:
            print("\nComparison Results:")
            for key in original_props:
                if key in cloned_props:
                    diff = abs(original_props[key] - cloned_props[key])
                    print(f"  {key} difference: {diff}")
    
    def generate_detection_report(self, audio_files):
        """Generate detection report for multiple audio files"""
        report = {
            "analysis_timestamp": "2024-01-01",
            "files_analyzed": len(audio_files),
            "suspicious_indicators": [],
            "recommendations": []
        }
        
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                props = self.analyze_audio_properties(audio_file)
                if props:
                    # Simple heuristics for detection
                    if props["duration_seconds"] < 10:
                        report["suspicious_indicators"].append(f"{audio_file}: Very short duration")
                    
                    if props["frame_rate"] != 22050:  # Common AI voice rate
                        report["suspicious_indicators"].append(f"{audio_file}: Unusual sample rate")
        
        report["recommendations"] = [
            "Verify caller identity through alternative channels",
            "Be suspicious of urgent requests for money or information",
            "Listen for unnatural speech patterns or artifacts",
            "Implement voice authentication systems"
        ]
        
        # Save report
        with open("detection_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\nDetection Report Generated:")
        print(json.dumps(report, indent=2))

def main():
    analyzer = VoiceAnalyzer()
    
    # Find generated vishing audio files
    audio_files = [f for f in os.listdir('.') if f.startswith('vishing_') and f.endswith('.mp3')]
    
    if audio_files:
        print(f"Found {len(audio_files)} vishing audio files for analysis")
        analyzer.generate_detection_report(audio_files)
    else:
        print("No vishing audio files found. Please generate scenarios first.")

if __name__ == "__main__":
    main()
