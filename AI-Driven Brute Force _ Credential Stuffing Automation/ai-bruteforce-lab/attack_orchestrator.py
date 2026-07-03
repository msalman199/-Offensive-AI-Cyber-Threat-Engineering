import subprocess
import json
import time
from datetime import datetime

class AttackOrchestrator:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'attacks': []
        }
    
    def run_password_analysis(self):
        """Run AI password analysis"""
        print("=== Running Password Analysis ===")
        try:
            result = subprocess.run(['python3', 'ai_password_analyzer.py'], 
                                  capture_output=True, text=True)
            
            attack_result = {
                'type': 'password_analysis',
                'success': result.returncode == 0,
                'output': result.stdout,
                'errors': result.stderr
            }
            
            self.results['attacks'].append(attack_result)
            print("Password analysis completed")
            return attack_result['success']
            
        except Exception as e:
            print(f"Password analysis failed: {e}")
            return False
    
    def run_brute_force_demo(self):
        """Run brute force demonstration"""
        print("=== Running Brute Force Demo ===")
        try:
            result = subprocess.run(['python3', 'intelligent_bruteforce.py'], 
                                  capture_output=True, text=True)
            
            attack_result = {
                'type': 'brute_force',
                'success': result.returncode == 0,
                'output': result.stdout,
                'errors': result.stderr
            }
            
            self.results['attacks'].append(attack_result)
            print("Brute force demo completed")
            return attack_result['success']
            
        except Exception as e:
            print(f"Brute force demo failed: {e}")
            return False
    
    def run_credential_stuffing_demo(self):
        """Run credential stuffing demonstration"""
        print("=== Running Credential Stuffing Demo ===")
        try:
            result = subprocess.run(['python3', 'credential_stuffer.py'], 
                                  capture_output=True, text=True)
            
            attack_result = {
                'type': 'credential_stuffing',
                'success': result.returncode == 0,
                'output': result.stdout,
                'errors': result.stderr
            }
            
            self.results['attacks'].append(attack_result)
            print("Credential stuffing demo completed")
            return attack_result['success']
            
        except Exception as e:
            print(f"Credential stuffing demo failed: {e}")
            return False
    
    def generate_report(self):
        """Generate attack report"""
        print("\n=== Attack Summary Report ===")
        
        successful_attacks = sum(1 for attack in self.results['attacks'] if attack['success'])
        total_attacks = len(self.results['attacks'])
        
        print(f"Total attacks executed: {total_attacks}")
        print(f"Successful attacks: {successful_attacks}")
        print(f"Success rate: {(successful_attacks/total_attacks)*100:.1f}%")
        
        print("\nDetailed Results:")
        for i, attack in enumerate(self.results['attacks'], 1):
            status = "SUCCESS" if attack['success'] else "FAILED"
            print(f"{i}. {attack['type']}: {status}")
            if attack['output']:
                print(f"   Output: {attack['output'][:100]}...")
        
        # Save detailed report
        with open('attack_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nDetailed report saved to: attack_report.json")
    
    def run_full_demonstration(self):
        """Execute complete attack demonstration"""
        print("Starting AI-Driven Attack Demonstration")
        print("=" * 50)
        
        # Run all attack components
        self.run_password_analysis()
        time.sleep(2)
        
        self.run_brute_force_demo()
        time.sleep(2)
        
        self.run_credential_stuffing_demo()
        time.sleep(2)
        
        # Generate final report
        self.generate_report()

if __name__ == "__main__":
    orchestrator = AttackOrchestrator()
    orchestrator.run_full_demonstration()
