#!/usr/bin/env python3
import os
from voice_cloner import VoiceCloner

class VishingSimulator:
    def __init__(self):
        self.cloner = VoiceCloner()
        self.scenarios = {
            "bank_fraud": "Hello, this is calling from your bank's security department. We've detected suspicious activity on your account. Please verify your account number and PIN to secure your account immediately.",
            "tech_support": "Hi, this is Microsoft technical support. We've detected malware on your computer. Please allow me remote access to fix this critical security issue.",
            "ceo_fraud": "This is urgent. I need you to transfer $50,000 to our new vendor account immediately. I'll send you the details via email. This is confidential.",
            "family_emergency": "Hi, this is your grandson calling from jail. I need you to wire money for bail immediately. Please don't tell my parents about this.",
            "irs_scam": "This is the IRS calling about unpaid taxes. You have a warrant for your arrest. Pay immediately to avoid legal action."
        }
    
    def generate_vishing_audio(self, scenario_name, voice_id, custom_text=None):
        """Generate vishing audio for specified scenario"""
        if custom_text:
            text = custom_text
        elif scenario_name in self.scenarios:
            text = self.scenarios[scenario_name]
        else:
            print(f"Unknown scenario: {scenario_name}")
            return None
        
        output_file = f"vishing_{scenario_name}.mp3"
        result = self.cloner.generate_speech(text, voice_id, output_file)
        
        if result:
            print(f"Vishing audio generated: {output_file}")
            print(f"Scenario: {scenario_name}")
            print(f"Text: {text[:100]}...")
        
        return result
    
    def list_scenarios(self):
        """List available vishing scenarios"""
        print("Available vishing scenarios:")
        for name, description in self.scenarios.items():
            print(f"- {name}: {description[:50]}...")

def main():
    simulator = VishingSimulator()
    
    # Check if voice ID file exists
    voice_id_file = "target_voice_voice_id.txt"
    if not os.path.exists(voice_id_file):
        print("Error: Voice ID file not found. Please run voice cloning first.")
        return
    
    # Read voice ID
    with open(voice_id_file, 'r') as f:
        voice_id = f.read().strip()
    
    print(f"Using voice ID: {voice_id}")
    
    # Generate vishing scenarios
    simulator.list_scenarios()
    
    scenarios_to_generate = ["bank_fraud", "tech_support", "ceo_fraud"]
    
    for scenario in scenarios_to_generate:
        print(f"\nGenerating scenario: {scenario}")
        simulator.generate_vishing_audio(scenario, voice_id)

if __name__ == "__main__":
    main()
