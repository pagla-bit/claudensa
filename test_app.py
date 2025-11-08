"""
Test script to verify all components work correctly
Run this before deploying to catch any issues
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✓ Streamlit")
    except ImportError as e:
        print(f"✗ Streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✓ Pandas")
    except ImportError as e:
        print(f"✗ Pandas: {e}")
        return False
    
    try:
        import requests
        print("✓ Requests")
    except ImportError as e:
        print(f"✗ Requests: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup4")
    except ImportError as e:
        print(f"✗ BeautifulSoup4: {e}")
        return False
    
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        print("✓ VADER Sentiment")
    except ImportError as e:
        print(f"✗ VADER Sentiment: {e}")
        return False
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        print("✓ Transformers (Hugging Face)")
    except ImportError as e:
        print(f"✗ Transformers: {e}")
        return False
    
    try:
        import torch
        print("✓ PyTorch")
    except ImportError as e:
        print(f"✗ PyTorch: {e}")
        return False
    
    return True


def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from news_scrapers import scrape_finviz, scrape_yahoo, scrape_google_news
        print("✓ news_scrapers.py")
    except ImportError as e:
        print(f"✗ news_scrapers.py: {e}")
        return False
    
    try:
        from sentiment_analyzer import analyze_vader_sentiment, analyze_finbert_sentiment
        print("✓ sentiment_analyzer.py")
    except ImportError as e:
        print(f"✗ sentiment_analyzer.py: {e}")
        return False
    
    try:
        from utils import validate_ticker, clean_ticker
        print("✓ utils.py")
    except ImportError as e:
        print(f"✗ utils.py: {e}")
        return False
    
    return True


def test_sentiment_analysis():
    """Test sentiment analysis functions"""
    print("\nTesting sentiment analysis...")
    
    try:
        from sentiment_analyzer import analyze_vader_sentiment, analyze_finbert_sentiment
        
        test_text = "Apple Inc. reported strong quarterly earnings, exceeding analyst expectations."
        
        # Test VADER
        vader_result = analyze_vader_sentiment(test_text)
        print(f"✓ VADER analysis: {vader_result['label']} (score: {vader_result['compound']:.3f})")
        
        # Test FinBERT
        print("  Loading FinBERT model (this may take a moment)...")
        finbert_result = analyze_finbert_sentiment(test_text)
        print(f"✓ FinBERT analysis: {finbert_result['label']} (confidence: {finbert_result['score']:.3f})")
        
        return True
        
    except Exception as e:
        print(f"✗ Sentiment analysis failed: {e}")
        return False


def test_web_scraping():
    """Test web scraping functions (optional, requires internet)"""
    print("\nTesting web scraping (optional)...")
    print("Note: This requires internet connection and may take a moment...")
    
    try:
        from news_scrapers import scrape_finviz
        
        # Test with a popular ticker
        print("  Attempting to scrape AAPL news from Finviz...")
        news_items = scrape_finviz("AAPL", max_articles=2)
        
        if news_items:
            print(f"✓ Successfully scraped {len(news_items)} article(s)")
            print(f"  Sample headline: {news_items[0]['headline'][:60]}...")
        else:
            print("⚠ No articles found (this might be normal)")
        
        return True
        
    except Exception as e:
        print(f"⚠ Web scraping test failed (not critical): {e}")
        return True  # Non-critical failure


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Stock Sentiment Analyzer - Component Tests")
    print("="*60)
    
    results = []
    
    # Critical tests
    results.append(("Imports", test_imports()))
    results.append(("Modules", test_modules()))
    results.append(("Sentiment Analysis", test_sentiment_analysis()))
    
    # Optional tests
    results.append(("Web Scraping", test_web_scraping()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary:")
    print("="*60)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    all_passed = all(result for name, result in results[:3])  # Only critical tests
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ All critical tests passed! Ready to deploy.")
        print("\nTo run the app:")
        print("  streamlit run stock_sentiment_app.py")
    else:
        print("✗ Some critical tests failed. Please fix issues before deploying.")
        sys.exit(1)
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
