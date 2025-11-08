# Deployment Guide

## Deploy to Streamlit Cloud

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Initialize git in your project folder:
```bash
git init
git add .
git commit -m "Initial commit: Stock Sentiment Analyzer"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set main file path: `stock_sentiment_app.py`
6. Click "Deploy"

### Step 3: Configuration
The app will automatically:
- Install dependencies from `requirements.txt`
- Download FinBERT model on first run (may take 1-2 minutes)
- Use the `.streamlit/config.toml` for UI settings

### Important Notes

**First Launch:**
- The first time someone uses FinBERT, the model will download (~400MB)
- This happens once and is cached for future sessions
- Subsequent loads are instant

**Resource Considerations:**
- FinBERT requires ~1GB RAM
- Streamlit Cloud free tier provides sufficient resources
- If you hit memory limits, consider using "Headlines Only" mode by default

**Performance Tips:**
1. Enable caching (already implemented)
2. Use shorter cache durations for frequently updated stocks
3. Limit concurrent ticker analysis to 10-15 for optimal performance
4. Use "Headlines Only" mode for faster results

### Alternative Deployment Options

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run stock_sentiment_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "stock_sentiment_app.py"]
```

#### Local Network
```bash
streamlit run stock_sentiment_app.py --server.address=0.0.0.0
```

## Environment Variables (Optional)

If you want to add API keys or configuration:

1. Create `.streamlit/secrets.toml`:
```toml
# Add any API keys here
news_api_key = "your_key_here"
```

2. Access in code:
```python
import streamlit as st
api_key = st.secrets["news_api_key"]
```

## Troubleshooting

### Model Download Issues
If FinBERT fails to download:
```python
# Add to sentiment_analyzer.py
import os
os.environ['TRANSFORMERS_CACHE'] = './cache'
```

### Memory Errors
Reduce batch size in `sentiment_analyzer.py`:
```python
def batch_analyze_finbert(texts: list, batch_size: int = 4):  # Reduce from 8
```

### Scraping Blocked
Add rotating user agents in `news_scrapers.py`:
```python
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    # Add more user agents
]

HEADERS = {'User-Agent': random.choice(USER_AGENTS)}
```

## Support

For issues or questions:
- Check the [GitHub Issues](https://github.com/yourusername/your-repo/issues)
- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- FinBERT Documentation: [huggingface.co/ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert)
