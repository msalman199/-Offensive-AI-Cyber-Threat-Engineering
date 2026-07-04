import librosa
import numpy as np
from scipy.spatial.distance import cosine

class VoiceAuthenticator:
    def __init__(self):
        self.enrolled_voices = {}
    
    def extract_voice_features(self, audio_file):
        """Extract voice biometric features"""
        try:
            y, sr = librosa.load(audio_file)
            
            # Extract MFCC features (voice fingerprint)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            
            # Extract additional features
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            
            features = np.concatenate([mfcc_mean, [spectral_centroid, spectral_rolloff]])
            return features
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def enroll_voice(self, user_id, audio_file):
        """Enroll a user's voice for authentication"""
        features = self.extract_voice_features(audio_file)
        if features is not None:
            self.enrolled_voices[user_id] = features
            print(f"Voice enrolled for user: {user_id}")
            return True
        return False
    
    def authenticate_voice(self, audio_file, threshold=0.3):
        """Authenticate voice against enrolled voices"""
        features = self.extract_voice_features(audio_file)
        if features is None:
            return None, 0.0
        
        best_match = None
        best_score = float('inf')
        
        for user_id, enrolled_features in self.enrolled_voices.items():
            # Calculate cosine distance
            distance = cosine(features, enrolled_features)
            if distance < best_score:
                best_score = distance
                best_match = user_id
        
        # Convert distance to similarity score
        similarity = 1 - best_score
        authenticated = similarity > (1 - threshold)
        
        return best_match if authenticated else None, similarity

if __name__ == "__main__":
    auth = VoiceAuthenticator()
    
    # Example usage
    if os.path.exists('target_voice.wav'):
        auth.enroll_voice('legitimate_user', 'target_voice.wav')
        
        # Test authentication
        test_files = [f for f in os.listdir('.') if f.endswith('.wav') and f != 'target_voice.wav']
        
        for test_file in test_files[:3]:  # Test first 3 files
            user, score = auth.authenticate_voice(test_file)
            print(f"File: {test_file}")
            print(f"Authenticated as: {user if user else 'REJECTED'}")
            print(f"Confidence: {score:.3f}")
            print("-" * 30)
