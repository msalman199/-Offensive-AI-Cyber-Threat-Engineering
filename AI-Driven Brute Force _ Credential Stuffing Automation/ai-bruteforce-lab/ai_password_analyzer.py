import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re

class PasswordAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2,4))
        self.kmeans = KMeans(n_clusters=5, random_state=42)
    
    def analyze_patterns(self, passwords):
        # Extract password features
        features = []
        for pwd in passwords:
            feature = {
                'length': len(pwd),
                'has_digits': bool(re.search(r'\d', pwd)),
                'has_upper': bool(re.search(r'[A-Z]', pwd)),
                'has_lower': bool(re.search(r'[a-z]', pwd)),
                'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd)),
                'digit_ratio': len(re.findall(r'\d', pwd)) / len(pwd),
                'common_patterns': self.check_common_patterns(pwd)
            }
            features.append(feature)
        return features
    
    def check_common_patterns(self, password):
        patterns = [
            r'\d{4}',  # 4 digits
            r'[a-zA-Z]+\d+',  # letters followed by numbers
            r'\d+[a-zA-Z]+',  # numbers followed by letters
            r'(.)\1{2,}',  # repeated characters
        ]
        return sum(1 for pattern in patterns if re.search(pattern, password))
    
    def generate_smart_wordlist(self, base_passwords, target_info=None):
        analyzed = self.analyze_patterns(base_passwords)
        smart_list = []
        
        for pwd in base_passwords[:100]:  # Limit for demo
            # Generate variations
            variations = [
                pwd,
                pwd + '123',
                pwd + '!',
                pwd.capitalize(),
                pwd + '2024',
                pwd.replace('a', '@').replace('o', '0')
            ]
            smart_list.extend(variations)
        
        return list(set(smart_list))

if __name__ == "__main__":
    analyzer = PasswordAnalyzer()
    
    # Load sample passwords
    with open('rockyou.txt', 'r', encoding='latin-1', errors='ignore') as f:
        passwords = [line.strip() for line in f.readlines()[:1000]]
    
    # Generate smart wordlist
    smart_passwords = analyzer.generate_smart_wordlist(passwords)
    
    # Save enhanced wordlist
    with open('ai_enhanced_wordlist.txt', 'w') as f:
        for pwd in smart_passwords:
            f.write(pwd + '\n')
    
    print(f"Generated {len(smart_passwords)} AI-enhanced passwords")
