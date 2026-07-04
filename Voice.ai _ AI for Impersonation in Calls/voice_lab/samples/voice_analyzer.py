import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

class VoiceAnalyzer:
    def __init__(self):
        pass
    
    def analyze_audio(self, audio_file):
        """Analyze audio characteristics"""
        try:
            # Load audio
            y, sr = librosa.load(audio_file)
            
            # Extract features
            features = {
                'duration': len(y) / sr,
                'sample_rate': sr,
                'rms_energy': np.mean(librosa.feature.rms(y=y)),
                'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
                'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y)),
                'tempo': librosa.beat.tempo(y=y, sr=sr)[0]
            }
            
            return features
        except Exception as e:
            print(f"Error analyzing {audio_file}: {e}")
            return None
    
    def compare_voices(self, original, synthetic):
        """Compare original and synthetic voice characteristics"""
        orig_features = self.analyze_audio(original)
        synth_features = self.analyze_audio(synthetic)
        
        if not orig_features or not synth_features:
            return None
        
        print(f"\n=== VOICE COMPARISON ===")
        print(f"{'Metric':<20} {'Original':<15} {'Synthetic':<15} {'Difference':<15}")
        print("-" * 65)
        
        for key in orig_features:
            if isinstance(orig_features[key], (int, float)):
                diff = abs(orig_features[key] - synth_features[key])
                print(f"{key:<20} {orig_features[key]:<15.3f} {synth_features[key]:<15.3f} {diff:<15.3f}")
        
        return orig_features, synth_features
    
    def detect_synthetic_indicators(self, audio_file):
        """Detect potential indicators of synthetic speech"""
        features = self.analyze_audio(audio_file)
        if not features:
            return []
        
        indicators = []
        
        # Check for common synthetic speech characteristics
        if features['rms_energy'] < 0.01:
            indicators.append("Unusually low energy levels")
        
        if features['spectral_centroid'] > 3000:
            indicators.append("High spectral centroid (metallic sound)")
        
        if features['zero_crossing_rate'] > 0.15:
            indicators.append("High zero crossing rate (artificial)")
        
        return indicators

if __name__ == "__main__":
    analyzer = VoiceAnalyzer()
    
    # Analyze available audio files
    audio_files = [f for f in os.listdir('.') if f.endswith('.wav')]
    
    for audio_file in audio_files:
        print(f"\nAnalyzing: {audio_file}")
        features = analyzer.analyze_audio(audio_file)
        if features:
            for key, value in features.items():
                print(f"{key}: {value}")
        
        indicators = analyzer.detect_synthetic_indicators(audio_file)
        if indicators:
            print("Synthetic speech indicators:")
            for indicator in indicators:
                print(f"- {indicator}")
