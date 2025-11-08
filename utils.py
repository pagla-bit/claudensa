import re
from typing import Dict


def validate_ticker(ticker: str) -> bool:
    """
    Validate ticker symbol format
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        True if valid format, False otherwise
    """
    # Basic validation: 1-5 uppercase letters
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, ticker.upper()))


def calculate_sentiment_ratio(row: Dict, use_vader: bool, use_finbert: bool) -> float:
    """
    Calculate sentiment ratio for sorting
    Ratio = (Positive) / (Positive + Negative + 1)
    
    Args:
        row: DataFrame row with sentiment counts
        use_vader: Whether VADER was used
        use_finbert: Whether FinBERT was used
    
    Returns:
        Sentiment ratio score
    """
    total_pos = 0
    total_neg = 0
    
    if use_vader:
        total_pos += row.get('VADER_Positive', 0)
        total_neg += row.get('VADER_Negative', 0)
    
    if use_finbert:
        total_pos += row.get('FinBERT_Positive', 0)
        total_neg += row.get('FinBERT_Negative', 0)
    
    # Calculate ratio (add 1 to denominator to avoid division by zero)
    ratio = total_pos / (total_pos + total_neg + 1)
    
    return round(ratio, 4)


def format_sentiment_scores(sentiment: Dict) -> str:
    """
    Format sentiment scores for display
    
    Args:
        sentiment: Sentiment dictionary with scores
    
    Returns:
        Formatted string
    """
    if not sentiment:
        return "N/A"
    
    label = sentiment.get('label', 'N/A')
    pos = sentiment.get('pos', 0)
    neg = sentiment.get('neg', 0)
    neu = sentiment.get('neu', 0)
    
    return f"{label} (P:{pos:.2f}, N:{neg:.2f}, Neu:{neu:.2f})"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
