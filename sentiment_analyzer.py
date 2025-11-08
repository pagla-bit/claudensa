from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict
import numpy as np

# Initialize VADER
vader_analyzer = SentimentIntensityAnalyzer()

# Initialize FinBERT (lazy loading)
finbert_tokenizer = None
finbert_model = None


def load_finbert():
    """
    Lazy load FinBERT model to save startup time
    """
    global finbert_tokenizer, finbert_model
    
    if finbert_tokenizer is None or finbert_model is None:
        finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        finbert_model.eval()


def analyze_vader_sentiment(text: str) -> Dict:
    """
    Analyze sentiment using VADER
    Returns: {'label': 'positive'|'negative'|'neutral', 'compound': score}
    """
    if not text or not text.strip():
        return {'label': 'neutral', 'compound': 0.0}
    
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Classify based on compound score
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    
    return {
        'label': label,
        'compound': compound,
        'pos': scores['pos'],
        'neu': scores['neu'],
        'neg': scores['neg']
    }


def analyze_finbert_sentiment(text: str) -> Dict:
    """
    Analyze sentiment using FinBERT
    Returns: {'label': 'positive'|'negative'|'neutral', 'score': confidence}
    """
    if not text or not text.strip():
        return {'label': 'neutral', 'score': 0.0}
    
    # Load model if not already loaded
    load_finbert()
    
    # Truncate text if too long (FinBERT has 512 token limit)
    max_length = 512
    
    try:
        # Tokenize
        inputs = finbert_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=max_length,
            padding=True
        )
        
        # Get prediction
        with torch.no_grad():
            outputs = finbert_model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # FinBERT labels: 0=positive, 1=negative, 2=neutral
        probs = predictions[0].numpy()
        predicted_class = np.argmax(probs)
        confidence = float(probs[predicted_class])
        
        label_map = {0: 'positive', 1: 'negative', 2: 'neutral'}
        label = label_map[predicted_class]
        
        return {
            'label': label,
            'score': confidence,
            'positive': float(probs[0]),
            'negative': float(probs[1]),
            'neutral': float(probs[2])
        }
        
    except Exception as e:
        print(f"Error in FinBERT analysis: {str(e)}")
        return {'label': 'neutral', 'score': 0.0}


def batch_analyze_vader(texts: list) -> list:
    """
    Batch analyze multiple texts with VADER
    """
    return [analyze_vader_sentiment(text) for text in texts]


def batch_analyze_finbert(texts: list, batch_size: int = 8) -> list:
    """
    Batch analyze multiple texts with FinBERT for efficiency
    """
    results = []
    
    # Load model once
    load_finbert()
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for text in batch:
            results.append(analyze_finbert_sentiment(text))
    
    return results
