from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import json
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self):
        # Initialize multiple sentiment models
        self.basic_sentiment = pipeline("sentiment-analysis", 
                                      model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.emotion_analyzer = pipeline("text-classification", 
                                       model="j-hartmann/emotion-english-distilroberta-base")
        
    def analyze_sentiment(self, text):
        """Analyze sentiment of given text"""
        basic_result = self.basic_sentiment(text)[0]
        emotion_result = self.emotion_analyzer(text)[0]
        
        return {
            'text': text,
            'sentiment': basic_result['label'],
            'sentiment_score': basic_result['score'],
            'emotion': emotion_result['label'],
            'emotion_score': emotion_result['score'],
            'timestamp': datetime.now().isoformat()
        }
    
    def batch_analyze(self, texts):
        """Analyze multiple texts"""
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Test with sample texts
    test_texts = [
        "I love this new product! It's amazing!",
        "This service is terrible and disappointing.",
        "The weather is okay today, nothing special.",
        "Urgent! Your account will be suspended unless you click here immediately!"
    ]
    
    results = analyzer.batch_analyze(test_texts)
    
    for result in results:
        print(f"Text: {result['text'][:50]}...")
        print(f"Sentiment: {result['sentiment']} ({result['sentiment_score']:.3f})")
        print(f"Emotion: {result['emotion']} ({result['emotion_score']:.3f})")
        print("-" * 60)
