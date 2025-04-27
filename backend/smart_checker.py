# smart_checker.py

# Smart keyword checking
suspicious_keywords = [
    "free", "lottery", "tanks rolled out", "world war", "us supports india",
    "deepfake menace", "unbelievable", "miracle", "breaking news", "explosive expose"
]

def is_text_suspicious(text):
    text_lower = text.lower()
    for keyword in suspicious_keywords:
        if keyword in text_lower:
            return True
    return False
