import torch
from TTS.api import TTS
import soundfile as sf
import sys
import os

class VoiceCloner:
    def __init__(self):
        # Initialize TTS model for voice cloning
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", 
                      progress_bar=False, gpu=False)
    
    def clone_voice(self, text, reference_audio, output_file):
        """Clone voice using reference audio"""
        try:
            # Generate speech with cloned voice
            self.tts.tts_to_file(
                text=text,
                speaker_wav=reference_audio,
                file_path=output_file,
                language="en"
            )
            print(f"Voice cloned successfully: {output_file}")
            return True
        except Exception as e:
            print(f"Error cloning voice: {e}")
            return False
    
    def synthesize_text(self, text, output_file):
        """Synthesize text with default voice"""
        try:
            self.tts.tts_to_file(text=text, file_path=output_file)
            print(f"Text synthesized: {output_file}")
            return True
        except Exception as e:
            print(f"Error synthesizing: {e}")
            return False

if __name__ == "__main__":
    cloner = VoiceCloner()
    
    # Example usage
    text = "Hello, this is a test of voice cloning technology."
    reference = "target_voice.wav"
    output = "cloned_output.wav"
    
    if os.path.exists(reference):
        cloner.clone_voice(text, reference, output)
    else:
        print("Reference audio not found, using default voice")
        cloner.synthesize_text(text, output)
