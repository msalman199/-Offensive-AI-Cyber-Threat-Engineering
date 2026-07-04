#!/usr/bin/env python3
import os
import sys
from voice_cloner import VoiceCloner

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 clone_automation.py <voice_name> <audio_file1> <audio_file2> [audio_file3...]")
        sys.exit(1)
    
    voice_name = sys.argv[1]
    audio_files = sys.argv[2:]
    
    # Verify audio files exist
    for file in audio_files:
        if not os.path.exists(file):
            print(f"Error: Audio file {file} not found")
            sys.exit(1)
    
    cloner = VoiceCloner()
    
    print(f"Cloning voice: {voice_name}")
    print(f"Using audio files: {', '.join(audio_files)}")
    
    # Clone the voice
    voice = cloner.clone_voice(voice_name, audio_files)
    
    if voice:
        print(f"Voice cloning successful!")
        print(f"Voice ID: {voice}")
        
        # Save voice ID for later use
        with open(f"{voice_name}_voice_id.txt", 'w') as f:
            f.write(str(voice))
        
        return voice
    else:
        print("Voice cloning failed!")
        return None

if __name__ == "__main__":
    main()
