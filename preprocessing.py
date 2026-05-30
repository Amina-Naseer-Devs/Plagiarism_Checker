import re

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def word_count(text):
    if not text or not text.strip():
        return 0
    return len(text.strip().split())

def is_valid_text(text):
    cleaned = re.sub(r'[\d\s\W]', '', text)
    return len(cleaned) > 0