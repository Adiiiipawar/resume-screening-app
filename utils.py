import re

def extract_keywords(text):
    """Extract keywords from text (based on comma, hyphen, or line separation)."""
    lines = text.splitlines()
    keywords = []
    for line in lines:
        # Remove punctuation, lower, and split by space/comma
        line = re.sub(r'[^\w\s,]', '', line.lower())
        keywords.extend([kw.strip() for kw in re.split(r'[,\-]', line) if kw.strip()])
    return list(set(keywords))
