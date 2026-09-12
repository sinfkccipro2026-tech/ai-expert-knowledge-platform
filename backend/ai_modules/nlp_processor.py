"""NLP Text Processing Module"""
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

class NLPProcessor:
    """Process natural language text"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def extract_keywords(self, text, num_keywords=10):
        """Extract top keywords from text"""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        from collections import Counter
        freq = Counter(words)
        return [word for word, _ in freq.most_common(num_keywords)]
    
    def extract_sentences(self, text, num_sentences=5):
        """Extract key sentences"""
        sentences = sent_tokenize(text)
        return sentences[:num_sentences]
    
    def clean_text(self, text):
        """Clean and normalize text"""
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
        text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        return text.strip()
