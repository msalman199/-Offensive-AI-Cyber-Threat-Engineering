import os
import json
from voice_analyzer import VoiceAnalyzer
from datetime import datetime

def generate_detection_report():
    analyzer = VoiceAnalyzer()
    report = {
        'timestamp': datetime.now().isoformat(),
        'analysis_results': {},
        'detection_summary': {}
    }
    
    # Analyze all WAV files
    audio_files = [f for f in os.listdir('.') if f.endswith('.wav')]
    
    for audio_file in audio_files:
        features = analyzer.analyze_audio(audio_file)
        indicators = analyzer.detect_synthetic_indicators(audio_file)
        
        report['analysis_results'][audio_file] = {
            'features': features,
            'synthetic_indicators': indicators,
            'risk_level': 'HIGH' if len(indicators) > 2 else 'MEDIUM' if indicators else 'LOW'
        }
    
    # Generate summary
    total_files = len(audio_files)
    high_risk = sum(1 for r in report['analysis_results'].values() if r['risk_level'] == 'HIGH')
    
    report['detection_summary'] = {
        'total_files_analyzed': total_files,
        'high_risk_files': high_risk,
        'detection_rate': f"{(high_risk/total_files)*100:.1f}%" if total_files > 0 else "0%"
    }
    
    # Save report
    with open('detection_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("=== VOICE IMPERSONATION DETECTION REPORT ===")
    print(f"Analysis completed at: {report['timestamp']}")
    print(f"Files analyzed: {total_files}")
    print(f"High-risk detections: {high_risk}")
    print(f"Detection rate: {report['detection_summary']['detection_rate']}")
    print("\nDetailed results saved to: detection_report.json")

if __name__ == "__main__":
    generate_detection_report()
