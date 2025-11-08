import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import List, Dict, Tuple
import concurrent.futures
from functools import lru_cache

# Import custom modules
from news_scrapers import scrape_finviz, scrape_google_news
from sentiment_analyzer import analyze_vader_sentiment, analyze_finbert_sentiment
from utils import validate_ticker, format_results

# Page configuration
st.set_page_config(
    page_title="Stock News Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'results_history' not in st.session_state:
    st.session_state.results_history = []
if 'cache' not in st.session_state:
    st.session_state.cache = {}

# Helper function for sentiment indicators
def get_sentiment_indicator(sentiment: str) -> str:
    """Return colored ball emoji for sentiment"""
    if sentiment == 'positive':
        return '🟢'
    elif sentiment == 'negative':
        return '🔴'
    else:
        return '🟡'

# Helper function to create clickable links
def make_clickable(url, text):
    """Create HTML for clickable link"""
    if url and url.startswith('http'):
        return f'<a href="{url}" target="_blank">{text}</a>'
    return text

# Title and description
st.title("📈 Stock News Sentiment Analyzer")
st.markdown("Analyze news sentiment for multiple stocks using VADER and FinBERT")

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    
    # Ticker input
    ticker_input = st.text_area(
        "Enter stock tickers (comma or space separated, max 30):",
        placeholder="AAPL, MSFT, GOOGL",
        height=100
    )
    
    # News sources selection
    st.subheader("News Sources")
    use_finviz = st.checkbox("Finviz.com", value=True)
    use_google = st.checkbox("Google News", value=True)
    
    # News count selection
    st.subheader("News Count")
    news_per_source = st.slider(
        "Articles per ticker per source:",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of latest news articles to fetch from each source"
    )
    
    # Sentiment analysis options
    st.subheader("Analysis Options")
    analysis_mode = st.radio(
        "Analyze sentiment on:",
        ["Headlines Only", "Full Content", "Both (Averaged)"]
    )
    
    # Cache settings
    st.subheader("Cache Settings")
    cache_duration = st.slider("Cache duration (minutes)", 5, 60, 15)
    clear_cache = st.button("Clear Cache")
    
    if clear_cache:
        st.session_state.cache = {}
        st.success("Cache cleared!")
    
    # Run analysis button
    analyze_button = st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True)

# Main content area
if analyze_button:
    # Parse tickers
    if not ticker_input.strip():
        st.error("Please enter at least one ticker symbol")
    else:
        # Parse and validate tickers
        tickers = [t.strip().upper() for t in ticker_input.replace(',', ' ').split() if t.strip()]
        tickers = list(dict.fromkeys(tickers))[:30]  # Remove duplicates and limit to 30
        
        if not any([use_finviz, use_google]):
            st.error("Please select at least one news source")
        else:
            st.info(f"Analyzing {len(tickers)} ticker(s) from {sum([use_finviz, use_google])} source(s)... ({news_per_source} articles per source)")
            
            # Create progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Collect news sources
            sources = []
            if use_finviz:
                sources.append(('Finviz', scrape_finviz))
            if use_google:
                sources.append(('Google News', scrape_google_news))
            
            # Process tickers
            all_results = []
            total_tasks = len(tickers)
            
            start_time = time.time()
            
            for idx, ticker in enumerate(tickers):
                status_text.text(f"Processing {ticker} ({idx + 1}/{total_tasks})...")
                
                ticker_news = []
                
                # Scrape news from each source
                for source_name, scraper_func in sources:
                    cache_key = f"{ticker}_{source_name}_{news_per_source}_{datetime.now().strftime('%Y%m%d%H%M')[:11]}"  # Cache per 10 min
                    
                    # Check cache
                    if cache_key in st.session_state.cache:
                        news_items = st.session_state.cache[cache_key]
                    else:
                        try:
                            news_items = scraper_func(ticker, max_articles=news_per_source)
                            st.session_state.cache[cache_key] = news_items
                        except Exception as e:
                            st.warning(f"Error scraping {source_name} for {ticker}: {str(e)}")
                            news_items = []
                    
                    ticker_news.extend(news_items)
                
                # Analyze sentiment for each news item
                if ticker_news:
                    for news in ticker_news:
                        # Determine what to analyze
                        if analysis_mode == "Headlines Only":
                            text_to_analyze = news['headline']
                        elif analysis_mode == "Full Content":
                            text_to_analyze = news.get('content', news['headline'])
                        else:  # Both (Averaged)
                            text_to_analyze = news['headline'] + " " + news.get('content', '')
                        
                        # VADER sentiment
                        vader_result = analyze_vader_sentiment(text_to_analyze)
                        news['vader_sentiment'] = vader_result['label']
                        news['vader_score'] = vader_result['compound']
                        
                        # FinBERT sentiment
                        finbert_result = analyze_finbert_sentiment(text_to_analyze)
                        news['finbert_sentiment'] = finbert_result['label']
                        news['finbert_score'] = finbert_result['score']
                        
                        news['ticker'] = ticker
                    
                    all_results.extend(ticker_news)
                
                # Update progress
                progress_bar.progress((idx + 1) / total_tasks)
            
            elapsed_time = time.time() - start_time
            status_text.text(f"✅ Analysis complete in {elapsed_time:.2f} seconds!")
            
            # Process results
            if all_results:
                # Create summary DataFrame
                summary_data = []
                
                for ticker in tickers:
                    ticker_results = [r for r in all_results if r['ticker'] == ticker]
                    
                    if ticker_results:
                        vader_pos = sum(1 for r in ticker_results if r['vader_sentiment'] == 'positive')
                        vader_neg = sum(1 for r in ticker_results if r['vader_sentiment'] == 'negative')
                        vader_neu = sum(1 for r in ticker_results if r['vader_sentiment'] == 'neutral')
                        
                        finbert_pos = sum(1 for r in ticker_results if r['finbert_sentiment'] == 'positive')
                        finbert_neg = sum(1 for r in ticker_results if r['finbert_sentiment'] == 'negative')
                        finbert_neu = sum(1 for r in ticker_results if r['finbert_sentiment'] == 'neutral')
                        
                        # Calculate sentiment ratios (positive to negative)
                        vader_ratio = vader_pos / vader_neg if vader_neg > 0 else (float('inf') if vader_pos > 0 else 0)
                        finbert_ratio = finbert_pos / finbert_neg if finbert_neg > 0 else (float('inf') if finbert_pos > 0 else 0)
                        
                        summary_data.append({
                            'Ticker': ticker,
                            'Total News': len(ticker_results),
                            'VADER Positive': vader_pos,
                            'VADER Negative': vader_neg,
                            'VADER Neutral': vader_neu,
                            'VADER Ratio (P/N)': f"{vader_ratio:.2f}" if vader_ratio != float('inf') else "∞",
                            'FinBERT Positive': finbert_pos,
                            'FinBERT Negative': finbert_neg,
                            'FinBERT Neutral': finbert_neu,
                            'FinBERT Ratio (P/N)': f"{finbert_ratio:.2f}" if finbert_ratio != float('inf') else "∞"
                        })
                
                summary_df = pd.DataFrame(summary_data)
                
                # Sort by sentiment ratio (using FinBERT as primary)
                summary_df['_finbert_ratio_numeric'] = summary_df['FinBERT Ratio (P/N)'].apply(
                    lambda x: float('inf') if x == "∞" else float(x)
                )
                summary_df = summary_df.sort_values('_finbert_ratio_numeric', ascending=False)
                summary_df = summary_df.drop('_finbert_ratio_numeric', axis=1)
                
                # Display summary
                st.header("📊 Summary Results")
                st.dataframe(summary_df, use_container_width=True)
                
                # Download summary
                csv_summary = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Summary as CSV",
                    data=csv_summary,
                    file_name=f"sentiment_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Detailed results
                st.header("📰 Detailed News Analysis")
                
                # Ticker filter for detailed view
                selected_ticker = st.selectbox(
                    "Filter by ticker:",
                    ['All'] + tickers
                )
                
                # Filter results
                if selected_ticker != 'All':
                    filtered_results = [r for r in all_results if r['ticker'] == selected_ticker]
                else:
                    filtered_results = all_results
                
                # Create detailed display with HTML for clickable links and sentiment indicators
                for item in filtered_results:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            # Clickable headline
                            if item.get('url'):
                                st.markdown(f"**[{item['headline']}]({item['url']})**")
                            else:
                                st.markdown(f"**{item['headline']}**")
                            st.caption(f"{item['ticker']} | {item['source']} | {item.get('date', 'N/A')}")
                        
                        with col2:
                            st.markdown("**VADER**")
                            vader_indicator = get_sentiment_indicator(item['vader_sentiment'])
                            st.markdown(f"{vader_indicator} {item['vader_score']:.3f}")
                        
                        with col3:
                            st.markdown("**FinBERT**")
                            finbert_indicator = get_sentiment_indicator(item['finbert_sentiment'])
                            st.markdown(f"{finbert_indicator} {item['finbert_score']:.3f}")
                        
                        st.divider()
                
                # Also provide downloadable detailed CSV
                detailed_data = []
                for item in filtered_results:
                    detailed_data.append({
                        'Ticker': item['ticker'],
                        'Source': item['source'],
                        'Headline': item['headline'],
                        'Date': item.get('date', 'N/A'),
                        'VADER Sentiment': item['vader_sentiment'],
                        'VADER Score': f"{item['vader_score']:.3f}",
                        'FinBERT Sentiment': item['finbert_sentiment'],
                        'FinBERT Score': f"{item['finbert_score']:.3f}",
                        'URL': item.get('url', '')
                    })
                
                detailed_df = pd.DataFrame(detailed_data)
                
                # Download detailed results
                csv_detailed = detailed_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Detailed Results as CSV",
                    data=csv_detailed,
                    file_name=f"sentiment_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Store in session state
                st.session_state.results_history.append({
                    'timestamp': datetime.now(),
                    'tickers': tickers,
                    'summary': summary_df,
                    'detailed': detailed_df
                })
            else:
                st.warning("No news articles found for the specified tickers.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Data sources: Finviz, Google News")
