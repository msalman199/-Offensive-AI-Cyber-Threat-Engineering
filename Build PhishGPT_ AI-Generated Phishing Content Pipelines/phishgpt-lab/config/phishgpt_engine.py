#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
from config.phishgpt_config import *

class PhishGPTEngine:
    def __init__(self):
        self.setup_logging()
        self.load_model()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'{LOG_DIR}/phishgpt.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def load_model(self):
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.model = GPT2LMHeadModel.from_pretrained('gpt2')
            self.generator = pipeline('text-generation', 
                                    model=self.model, 
                                    tokenizer=self.tokenizer)
            self.logger.info("Model loaded successfully")
        except Exception as e:
            self.logger.error(f"Model loading failed: {e}")
            
    def generate_content(self, content_type, target_info, scenario):
        prompts = self.create_prompts(content_type, target_info, scenario)
        generated_content = []
        
        for prompt in prompts:
            try:
                result = self.generator(
                    prompt,
                    max_length=CONTENT_TYPES[content_type]['max_length'],
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                generated_content.append(result[0]['generated_text'])
                self.logger.info(f"Generated {content_type} content")
            except Exception as e:
                self.logger.error(f"Content generation failed: {e}")
                
        return generated_content
        
    def create_prompts(self, content_type, target_info, scenario):
        base_prompts = {
            'email': [
                f"Write a professional email from {scenario['sender']} to {target_info['name']} about {scenario['topic']}:",
                f"Create an urgent email notification for {target_info['name']} regarding {scenario['topic']}:"
            ],
            'sms': [
                f"Write a short SMS message to {target_info['name']} about {scenario['topic']}:",
                f"Create an urgent text message for {target_info['name']} regarding {scenario['topic']}:"
            ],
            'form': [
                f"Create form text for {scenario['topic']} targeting {target_info['name']}:",
                f"Write form content about {scenario['topic']} for user verification:"
            ]
        }
        return base_prompts.get(content_type, [])

if __name__ == "__main__":
    engine = PhishGPTEngine()
    print("PhishGPT Engine initialized successfully")
