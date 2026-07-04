from sentiment_analyzer import SentimentAnalyzer
from psychological_profiler import PsychologicalProfiler
import json
import pandas as pd
from datetime import datetime

class IntegratedAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.psychological_profiler = PsychologicalProfiler()
    
    def comprehensive_analysis(self, text):
        """Perform comprehensive analysis combining sentiment and psychological profiling"""
        sentiment_result = self.sentiment_analyzer.analyze_sentiment(text)
        psychological_profile = self.psychological_profiler.generate_psychological_profile(text)
        
        # Calculate overall threat score
        threat_score = self.calculate_threat_score(sentiment_result, psychological_profile)
        
        return {
            'text': text,
            'sentiment_analysis': sentiment_result,
            'psychological_profile': psychological_profile,
            'threat_score': threat_score,
            'risk_level': self.determine_risk_level(threat_score),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def calculate_threat_score(self, sentiment, psychological):
        """Calculate overall threat score (0-100)"""
        score = 0
        
        # Sentiment factors
        if sentiment['sentiment'] == 'NEGATIVE':
            score += 20
        elif sentiment['sentiment'] == 'POSITIVE' and psychological['reward_motivation'] == 'High':
            score += 15
        
        # Psychological factors
        score += psychological['manipulation_score'] * 0.4
        
        if psychological['urgency_level'] == 'High':
            score += 15
        if psychological['fear_tactics'] == 'High':
            score += 20
        if psychological['authority_appeal'] == 'High':
            score += 10
        
        return min(score, 100)
    
    def determine_risk_level(self, threat_score):
        """Determine risk level based on threat score"""
        if threat_score >= 70:
            return "HIGH RISK"
        elif threat_score >= 40:
            return "MEDIUM RISK"
        else:
            return "LOW RISK"

if __name__ == "__main__":
    analyzer = IntegratedAnalyzer()
    
    # Test with various text samples
    test_samples = [
        "Congratulations! You've won $1000! Click here to claim your prize now!",
        "Your account security has been compromised. Immediate action required to prevent data loss.",
        "Thank you for your recent purchase. Your order will be delivered tomorrow.",
        "URGENT: IRS Notice - Pay your taxes immediately or face legal consequences!"
    ]
    
    print("Comprehensive Analysis Results:")
    print("=" * 80)
    
    for i, text in enumerate(test_samples, 1):
        result = analyzer.comprehensive_analysis(text)
        
        print(f"\nSample {i}:")
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment_analysis']['sentiment']} "
              f"({result['sentiment_analysis']['sentiment_score']:.3f})")
        print(f"Emotion: {result['sentiment_analysis']['emotion']} "
              f"({result['sentiment_analysis']['emotion_score']:.3f})")
        print(f"Manipulation Score: {result['psychological_profile']['manipulation_score']:.1f}/100")
        print(f"Threat Score: {result['threat_score']:.1f}/100")
        print(f"Risk Level: {result['risk_level']}")
        print("-" * 60)
