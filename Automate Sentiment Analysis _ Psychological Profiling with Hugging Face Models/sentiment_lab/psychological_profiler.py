from transformers import pipeline
import re
import pandas as pd
from collections import Counter
import numpy as np

class PsychologicalProfiler:
    def __init__(self):
        # Initialize personality analysis model
        self.personality_analyzer = pipeline("text-classification", 
                                           model="martin-ha/toxic-comment-model")
        
    def analyze_linguistic_patterns(self, text):
        """Analyze linguistic patterns for psychological insights"""
        patterns = {
            'urgency_words': len(re.findall(r'\b(urgent|immediate|now|quickly|asap|hurry)\b', text.lower())),
            'authority_words': len(re.findall(r'\b(must|required|mandatory|official|government)\b', text.lower())),
            'fear_words': len(re.findall(r'\b(danger|risk|threat|warning|alert|suspended)\b', text.lower())),
            'reward_words': len(re.findall(r'\b(free|win|prize|bonus|reward|gift)\b', text.lower())),
            'personal_pronouns': len(re.findall(r'\b(you|your|yours)\b', text.lower())),
            'exclamation_marks': text.count('!'),
            'question_marks': text.count('?'),
            'capital_letters': sum(1 for c in text if c.isupper()),
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text))
        }
        
        return patterns
    
    def calculate_manipulation_score(self, patterns):
        """Calculate manipulation score based on linguistic patterns"""
        score = 0
        
        # Weight different factors
        score += patterns['urgency_words'] * 2
        score += patterns['authority_words'] * 1.5
        score += patterns['fear_words'] * 2.5
        score += patterns['reward_words'] * 1.5
        score += min(patterns['exclamation_marks'], 5) * 0.5
        score += min(patterns['capital_letters'] / max(patterns['word_count'], 1), 0.3) * 10
        
        # Normalize score (0-100)
        normalized_score = min(score * 5, 100)
        return normalized_score
    
    def generate_psychological_profile(self, text):
        """Generate comprehensive psychological profile"""
        patterns = self.analyze_linguistic_patterns(text)
        manipulation_score = self.calculate_manipulation_score(patterns)
        
        # Determine profile characteristics
        profile = {
            'manipulation_score': manipulation_score,
            'urgency_level': 'High' if patterns['urgency_words'] > 2 else 'Medium' if patterns['urgency_words'] > 0 else 'Low',
            'authority_appeal': 'High' if patterns['authority_words'] > 1 else 'Medium' if patterns['authority_words'] > 0 else 'Low',
            'fear_tactics': 'High' if patterns['fear_words'] > 2 else 'Medium' if patterns['fear_words'] > 0 else 'Low',
            'reward_motivation': 'High' if patterns['reward_words'] > 1 else 'Medium' if patterns['reward_words'] > 0 else 'Low',
            'personalization': 'High' if patterns['personal_pronouns'] > 3 else 'Medium' if patterns['personal_pronouns'] > 0 else 'Low',
            'emotional_intensity': 'High' if patterns['exclamation_marks'] > 3 else 'Medium' if patterns['exclamation_marks'] > 0 else 'Low',
            'linguistic_patterns': patterns
        }
        
        return profile

if __name__ == "__main__":
    profiler = PsychologicalProfiler()
    
    # Test with phishing-like text
    test_text = """
    URGENT! Your PayPal account will be suspended immediately unless you verify your information NOW!
    Click here to avoid account closure. This is an official notice from PayPal Security Team.
    You must act quickly to prevent losing access to your funds!
    """
    
    profile = profiler.generate_psychological_profile(test_text)
    
    print("Psychological Profile Analysis:")
    print(f"Manipulation Score: {profile['manipulation_score']:.1f}/100")
    print(f"Urgency Level: {profile['urgency_level']}")
    print(f"Authority Appeal: {profile['authority_appeal']}")
    print(f"Fear Tactics: {profile['fear_tactics']}")
    print(f"Reward Motivation: {profile['reward_motivation']}")
    print(f"Personalization: {profile['personalization']}")
    print(f"Emotional Intensity: {profile['emotional_intensity']}")
