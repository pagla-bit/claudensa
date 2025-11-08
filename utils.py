import re
from typing import List

def validate_ticker(ticker: str) -> bool:
    """
    Simple validation if a ticker symbol is valid format
    Returns True if ticker appears valid (basic check)
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Basic validation: 1-5 characters, alphanumeric
    ticker = ticker.strip().upper()
    if len(ticker) < 1 or len(ticker) > 5:
        return False
    
    # Allow letters, numbers, dots, and hyphens
    if not re.match(r'^[A-Z0-9.\-]+$', ticker):
        return False
    
    return True


def clean_ticker(ticker: str) -> str:
    """
    Clean and format ticker symbol
    """
    if not ticker:
        return ""
    
    # Remove special characters except dots and hyphens
    ticker = re.sub(r'[^A-Za-z0-9.\-]', '', ticker)
    return ticker.upper().strip()


def format_results(results: List[dict]) -> dict:
    """
    Format raw results into structured summary
    """
    summary = {}
    
    for item in results:
        ticker = item.get('ticker', 'UNKNOWN')
        
        if ticker not in summary:
            summary[ticker] = {
                'total_news': 0,
                'vader': {'positive': 0, 'negative': 0, 'neutral': 0},
                'finbert': {'positive': 0, 'negative': 0, 'neutral': 0},
                'news_items': []
            }
        
        summary[ticker]['total_news'] += 1
        
        # Count VADER sentiment
        vader_sentiment = item.get('vader_sentiment', 'neutral')
        if vader_sentiment in summary[ticker]['vader']:
            summary[ticker]['vader'][vader_sentiment] += 1
        
        # Count FinBERT sentiment
        finbert_sentiment = item.get('finbert_sentiment', 'neutral')
        if finbert_sentiment in summary[ticker]['finbert']:
            summary[ticker]['finbert'][finbert_sentiment] += 1
        
        summary[ticker]['news_items'].append(item)
    
    return summary


def calculate_sentiment_ratio(positive: int, negative: int) -> float:
    """
    Calculate positive to negative sentiment ratio
    """
    if negative == 0:
        return float('inf') if positive > 0 else 0.0
    return positive / negative


def format_percentage(value: float) -> str:
    """
    Format value as percentage
    """
    return f"{value * 100:.1f}%"
