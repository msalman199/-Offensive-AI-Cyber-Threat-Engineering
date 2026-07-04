import os

# LLM Configuration
MODEL_NAME = "microsoft/DialoGPT-medium"
MAX_LENGTH = 512
TEMPERATURE = 0.8
TOP_P = 0.9

# Content Types
CONTENT_TYPES = {
    'email': {
        'max_length': 300,
        'tone': 'professional'
    },
    'sms': {
        'max_length': 160,
        'tone': 'urgent'
    },
    'form': {
        'max_length': 100,
        'tone': 'trustworthy'
    }
}

# Output Directories
OUTPUT_DIR = "outputs"
TEMPLATE_DIR = "templates"
LOG_DIR = "logs"
