import json
import time
import subprocess
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        self.state = {}
        self.learning_data = []
    
    @abstractmethod
    def analyze(self, data):
        pass
    
    @abstractmethod
    def decide(self, analysis_result):
        pass
    
    def log_action(self, action, result):
        log_entry = {
            'timestamp': time.time(),
            'agent': self.name,
            'action': action,
            'result': result
        }
        self.learning_data.append(log_entry)
        
    def save_state(self, filepath):
        with open(filepath, 'w') as f:
            json.dump({
                'state': self.state,
                'learning_data': self.learning_data
            }, f, indent=2)
