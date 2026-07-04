import time
import random
import os
from voice_clone import VoiceCloner

class CallSimulator:
    def __init__(self):
        self.cloner = VoiceCloner()
        self.call_scripts = {
            "tech_support": [
                "Hello, this is Microsoft technical support.",
                "We've detected suspicious activity on your computer.",
                "Please provide your login credentials to verify your identity."
            ],
            "bank_fraud": [
                "This is your bank's fraud department.",
                "We've detected unauthorized transactions on your account.",
                "Please confirm your account number and PIN for verification."
            ],
            "family_emergency": [
                "Hi, it's me. I'm in trouble and need help.",
                "I've been in an accident and need money for bail.",
                "Please don't tell anyone, just send the money quickly."
            ]
        }
    
    def generate_call_audio(self, scenario, reference_voice=None):
        """Generate audio for vishing call scenario"""
        if scenario not in self.call_scripts:
            print(f"Unknown scenario: {scenario}")
            return False
        
        script = self.call_scripts[scenario]
        output_files = []
        
        for i, line in enumerate(script):
            output_file = f"{scenario}_line_{i+1}.wav"
            
            if reference_voice and os.path.exists(reference_voice):
                success = self.cloner.clone_voice(line, reference_voice, output_file)
            else:
                success = self.cloner.synthesize_text(line, output_file)
            
            if success:
                output_files.append(output_file)
                print(f"Generated: {output_file}")
            
            time.sleep(1)  # Brief pause between generations
        
        return output_files
    
    def simulate_call(self, scenario, reference_voice=None):
        """Simulate a complete vishing call"""
        print(f"\n=== SIMULATING {scenario.upper()} CALL ===")
        print("WARNING: This is a simulation for educational purposes only!")
        print("-" * 50)
        
        audio_files = self.generate_call_audio(scenario, reference_voice)
        
        if audio_files:
            print(f"\nCall simulation complete. Generated {len(audio_files)} audio segments.")
            print("Audio files:", audio_files)
            
            # Simulate call timing
            print("\nSimulating call progression:")
            for i, audio_file in enumerate(audio_files, 1):
                print(f"Playing segment {i}: {audio_file}")
                time.sleep(2)  # Simulate speaking time
                print("Waiting for response...")
                time.sleep(1)  # Simulate response time
        
        return audio_files

if __name__ == "__main__":
    simulator = CallSimulator()
    
    # List available scenarios
    print("Available scenarios:")
    for scenario in simulator.call_scripts.keys():
        print(f"- {scenario}")
    
    # Run simulation
    scenario = input("\nEnter scenario name: ").strip()
    reference = "target_voice.wav" if os.path.exists("target_voice.wav") else None
    
    simulator.simulate_call(scenario, reference)
