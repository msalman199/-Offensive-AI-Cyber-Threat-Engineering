import json
from datetime import datetime

class DefenseAnalyzer:
    def __init__(self):
        self.vulnerabilities = []
        self.recommendations = []
    
    def analyze_attack_results(self, results_file='attack_report.json'):
        """Analyze attack results and generate defense recommendations"""
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
        except FileNotFoundError:
            print("No attack results found")
            return
        
        print("=== Defense Analysis Report ===")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Analyze each attack type
        for attack in results['attacks']:
            self.analyze_attack_type(attack)
        
        # Generate comprehensive recommendations
        self.generate_defense_recommendations()
        
        # Save defense report
        defense_report = {
            'analysis_date': datetime.now().isoformat(),
            'vulnerabilities': self.vulnerabilities,
            'recommendations': self.recommendations
        }
        
        with open('defense_recommendations.json', 'w') as f:
            json.dump(defense_report, f, indent=2)
        
        print("Defense analysis saved to: defense_recommendations.json")
    
    def analyze_attack_type(self, attack):
        """Analyze specific attack type"""
        attack_type = attack['type']
        
        if attack_type == 'password_analysis':
            self.vulnerabilities.append({
                'type': 'Weak Password Patterns',
                'severity': 'High',
                'description': 'AI can identify and exploit common password patterns'
            })
        
        elif attack_type == 'brute_force':
            self.vulnerabilities.append({
                'type': 'Brute Force Susceptibility',
                'severity': 'High',
                'description': 'System vulnerable to intelligent brute force attacks'
            })
        
        elif attack_type == 'credential_stuffing':
            self.vulnerabilities.append({
                'type': 'Credential Reuse',
                'severity': 'Critical',
                'description': 'Users likely reusing passwords across multiple services'
            })
    
    def generate_defense_recommendations(self):
        """Generate comprehensive defense recommendations"""
        self.recommendations = [
            {
                'category': 'Authentication Security',
                'measures': [
                    'Implement multi-factor authentication (MFA)',
                    'Use account lockout policies after failed attempts',
                    'Implement CAPTCHA after multiple failed logins',
                    'Use rate limiting on login endpoints'
                ]
            },
            {
                'category': 'Password Policy',
                'measures': [
                    'Enforce strong password complexity requirements',
                    'Implement password history to prevent reuse',
                    'Regular password expiration policies',
                    'Use password strength meters during creation'
                ]
            },
            {
                'category': 'Monitoring and Detection',
                'measures': [
                    'Implement real-time login attempt monitoring',
                    'Set up alerts for suspicious login patterns',
                    'Log and analyze authentication events',
                    'Use behavioral analysis to detect anomalies'
                ]
            },
            {
                'category': 'Network Security',
                'measures': [
                    'Implement IP-based blocking for repeated failures',
                    'Use geolocation filtering for unusual locations',
                    'Deploy Web Application Firewalls (WAF)',
                    'Implement DDoS protection'
                ]
            }
        ]
        
        print("Defense Recommendations:")
        print("=" * 30)
        
        for rec in self.recommendations:
            print(f"\n{rec['category']}:")
            for measure in rec['measures']:
                print(f"  • {measure}")

if __name__ == "__main__":
    analyzer = DefenseAnalyzer()
    analyzer.analyze_attack_results()
