import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict
import re

# User agent to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_finviz(ticker: str, max_articles: int = 5) -> List[Dict]:
    """
    Scrape news from Finviz.com
    """
    news_items = []
    
    try:
        url = f"https://finviz.com/quote.ashx?t={ticker}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_table = soup.find('table', {'id': 'news-table'})
        
        if news_table:
            rows = news_table.find_all('tr')[:max_articles]
            
            for row in rows:
                try:
                    # Get date/time
                    date_cell = row.find('td', {'align': 'right'})
                    date_text = date_cell.text.strip() if date_cell else 'N/A'
                    
                    # Get headline and link
                    link_cell = row.find('a', {'class': 'tab-link-news'})
                    if link_cell:
                        headline = link_cell.text.strip()
                        url = link_cell.get('href', '')
                        
                        # Try to fetch article content if URL is available
                        content = fetch_article_content(url) if url else ''
                        
                        news_items.append({
                            'source': 'Finviz',
                            'headline': headline,
                            'date': date_text,
                            'url': url,
                            'content': content
                        })
                except Exception as e:
                    continue
        
        time.sleep(0.5)  # Be respectful to the server
        
    except Exception as e:
        print(f"Error scraping Finviz for {ticker}: {str(e)}")
    
    return news_items


def scrape_yahoo(ticker: str, max_articles: int = 5) -> List[Dict]:
    """
    Scrape news from Yahoo Finance - Updated for 2024 structure
    """
    news_items = []
    
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Yahoo Finance uses various div structures for news
        # Try multiple selectors to find news items
        news_containers = []
        
        # Look for news sections
        selectors = [
            'div[data-test="news-stream"]',
            'div.stream-items',
            'div.Mb\\(20px\\)',
            'li.js-stream-content'
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                news_containers.extend(containers[:max_articles * 2])  # Get extra in case some fail
                break
        
        # If no specific news containers, look for article/h3 tags
        if not news_containers:
            # Find all h3 tags that might contain news
            h3_tags = soup.find_all('h3')
            for h3 in h3_tags[:max_articles * 2]:
                link = h3.find('a')
                if link and link.get('href'):
                    headline = link.text.strip()
                    article_url = link.get('href', '')
                    
                    # Make URL absolute if relative
                    if article_url.startswith('/'):
                        article_url = f"https://finance.yahoo.com{article_url}"
                    elif not article_url.startswith('http'):
                        continue
                    
                    # Skip if not a valid URL
                    if not article_url or article_url == '#':
                        continue
                    
                    # Try to get date from nearby elements
                    date_text = 'Recent'
                    parent = h3.find_parent()
                    if parent:
                        time_elem = parent.find('time')
                        if time_elem:
                            date_text = time_elem.text.strip()
                    
                    # Try to fetch content
                    content = ''
                    if article_url.startswith('http'):
                        content = fetch_article_content(article_url)
                    
                    news_items.append({
                        'source': 'Yahoo Finance',
                        'headline': headline,
                        'date': date_text,
                        'url': article_url,
                        'content': content
                    })
                    
                    if len(news_items) >= max_articles:
                        break
        else:
            # Process news containers
            for container in news_containers:
                if len(news_items) >= max_articles:
                    break
                
                try:
                    # Find headline and link
                    link = container.find('a')
                    if not link:
                        continue
                    
                    headline = link.text.strip()
                    article_url = link.get('href', '')
                    
                    # Skip empty headlines
                    if not headline or len(headline) < 10:
                        continue
                    
                    # Make URL absolute if relative
                    if article_url.startswith('/'):
                        article_url = f"https://finance.yahoo.com{article_url}"
                    elif not article_url.startswith('http'):
                        continue
                    
                    # Try to get date
                    date_text = 'Recent'
                    time_elem = container.find('time')
                    if time_elem:
                        date_text = time_elem.text.strip()
                    
                    # Try to fetch content
                    content = ''
                    if article_url.startswith('http'):
                        content = fetch_article_content(article_url)
                    
                    news_items.append({
                        'source': 'Yahoo Finance',
                        'headline': headline,
                        'date': date_text,
                        'url': article_url,
                        'content': content
                    })
                except Exception as e:
                    continue
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error scraping Yahoo Finance for {ticker}: {str(e)}")
    
    return news_items[:max_articles]


def scrape_google_news(ticker: str, max_articles: int = 5) -> List[Dict]:
    """
    Scrape news from Google News
    Note: Google News URLs may redirect through Google's servers
    """
    news_items = []
    
    try:
        # Search Google News for ticker
        search_query = f"{ticker} stock news"
        url = f"https://news.google.com/search?q={search_query}&hl=en-US&gl=US&ceid=US:en"
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Google News articles
        articles = soup.find_all('article', limit=max_articles * 2)
        
        for article in articles:
            if len(news_items) >= max_articles:
                break
            
            try:
                # Get headline and link
                headline_tag = article.find('a')
                if not headline_tag:
                    continue
                
                headline = headline_tag.text.strip()
                article_url = headline_tag.get('href', '')
                
                # Skip if headline too short
                if len(headline) < 10:
                    continue
                
                # Handle Google News URLs
                final_url = ''
                if article_url.startswith('./articles/'):
                    # Google News article - convert to full URL
                    final_url = f"https://news.google.com{article_url[1:]}"
                elif article_url.startswith('./'):
                    final_url = f"https://news.google.com{article_url[1:]}"
                elif article_url.startswith('http'):
                    final_url = article_url
                
                # Get date/time
                time_tag = article.find('time')
                date_text = time_tag.text.strip() if time_tag else 'Recent'
                
                # Add article with or without URL
                news_items.append({
                    'source': 'Google News',
                    'headline': headline,
                    'date': date_text,
                    'url': final_url if final_url.startswith('http') else '',  # Only include valid URLs
                    'content': ''
                })
            except Exception as e:
                continue
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error scraping Google News for {ticker}: {str(e)}")
    
    return news_items


def fetch_article_content(url: str, max_length: int = 1000) -> str:
    """
    Attempt to fetch article content from URL
    Limited to first max_length characters to avoid overload
    """
    if not url or url.startswith('#') or not url.startswith('http'):
        return ''
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'header', 'footer']):
            script.decompose()
        
        # Try common article containers
        article_content = None
        for selector in ['article', 'div[class*="article"]', 'div[class*="content"]', 'main']:
            article_content = soup.find(selector)
            if article_content:
                break
        
        if article_content:
            # Get text and clean it
            text = article_content.get_text(separator=' ', strip=True)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:max_length]
        
        return ''
        
    except Exception as e:
        return ''
