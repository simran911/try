import os

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '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')
    MODEL_NAME = "llama-3.3-70b-versatile"
    TEMPERATURE = 0.3
    MAX_TOKENS = 500