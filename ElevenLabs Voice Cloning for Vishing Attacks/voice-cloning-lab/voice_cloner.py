#!/usr/bin/env python3
import os
import requests
from elevenlabs import clone, generate, play, set_api_key
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceCloner:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set ELEVENLABS_API_KEY in .env file")
        set_api_key(self.api_key)
    
    def clone_voice(self, name, audio_files, description="Cloned voice for security testing"):
        """Clone a voice from audio samples"""
        try:
            voice = clone(
                name=name,
                files=audio_files,
                description=description
            )
            print(f"Voice cloned successfully: {voice}")
            return voice
        except Exception as e:
            print(f"Error cloning voice: {e}")
            return None
    
    def generate_speech(self, text, voice_id, output_file="output.mp3"):
        """Generate speech using cloned voice"""
        try:
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            with open(output_file, 'wb') as f:
                f.write(audio)
            
            print(f"Audio generated successfully: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None

if __name__ == "__main__":
    cloner = VoiceCloner()
    print("Voice cloning setup complete!")
