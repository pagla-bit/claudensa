from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict
from news_scraper import fetch_article_content

# Initialize VADER
vader_analyzer = SentimentIntensityAnalyzer()

# Initialize FinBERT (lazy loading)
finbert_tokenizer = None
finbert_model = None


def load_finbert():
    """Lazy load FinBERT model to save memory"""
    global finbert_tokenizer, finbert_model
    
    if finbert_tokenizer is None or finbert_model is None:
        finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        finbert_model.eval()  # Set to evaluation mode


def analyze_vader(text: str) -> Dict:
    """
    Analyze sentiment using VADER
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with sentiment scores and label
    """
    scores = vader_analyzer.polarity_scores(text)
    
    # Determine label based on compound score
    compound = scores['compound']
    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
    
    return {
        'pos': scores['pos'],
        'neg': scores['neg'],
        'neu': scores['neu'],
        'compound': compound,
        'label': label
    }


def analyze_finbert(text: str) -> Dict:
    """
    Analyze sentiment using FinBERT
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with sentiment scores and label
    """
    load_finbert()
    
    # Tokenize and prepare input
    inputs = finbert_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )
    
    # Get prediction
    with torch.no_grad():
        outputs = finbert_model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # FinBERT outputs: [positive, negative, neutral]
    scores = predictions[0].tolist()
    
    # Determine label
    label_idx = scores.index(max(scores))
    labels = ['Positive', 'Negative', 'Neutral']
    label = labels[label_idx]
    
    return {
        'pos': scores[0],
        'neg': scores[1],
        'neu': scores[2],
        'label': label
    }


def analyze_sentiment(article: Dict, use_vader: bool = True, use_finbert: bool = True, 
                     analyze_content: bool = False) -> Dict:
    """
    Analyze sentiment of an article using specified methods
    
    Args:
        article: Article dictionary with headline, link, etc.
        use_vader: Whether to use VADER analysis
        use_finbert: Whether to use FinBERT analysis
        analyze_content: Whether to fetch and analyze full article content
    
    Returns:
        Article dictionary enriched with sentiment analysis results
    """
    result = article.copy()
    
    # Determine what text to analyze
    headline = article.get('headline', '')
    
    if analyze_content:
        content = fetch_article_content(article.get('link', ''))
        # Combine headline and content, or use content if available
        text_to_analyze = f"{headline}. {content}" if content else headline
    else:
        text_to_analyze = headline
    
    # Perform sentiment analysis
    if use_vader:
        try:
            result['vader_sentiment'] = analyze_vader(text_to_analyze)
        except Exception as e:
            print(f"VADER analysis error: {str(e)}")
            result['vader_sentiment'] = None
    
    if use_finbert:
        try:
            result['finbert_sentiment'] = analyze_finbert(text_to_analyze)
        except Exception as e:
            print(f"FinBERT analysis error: {str(e)}")
            result['finbert_sentiment'] = None
    
    return result
