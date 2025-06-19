import os

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    MODEL_NAME = "llama-3.3-70b-versatile"
    TEMPERATURE = 0.3
    MAX_TOKENS = 500
