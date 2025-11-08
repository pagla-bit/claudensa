# Multi-Ticker News Sentiment Analysis

A Streamlit application that analyzes news sentiment for multiple stock tickers using both VADER and FinBERT sentiment analysis methods.

## Features

- **Multi-ticker analysis**: Analyze up to 30 stock tickers simultaneously
- **Multiple news sources**: Scrape from Finviz, Yahoo Finance, and Google News
- **Dual sentiment analysis**: Compare VADER and FinBERT sentiment scores
- **Flexible analysis scope**: Analyze headlines only, full article content, or both
- **Efficient caching**: Avoid re-scraping news with intelligent caching system
- **Parallel processing**: Fast processing using ThreadPoolExecutor
- **Progress tracking**: Real-time progress indicators during analysis
- **Export functionality**: Download results as CSV
- **Detailed view**: Explore individual news articles and their sentiment scores

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and branch
5. Set main file path to `app.py`
6. Click "Deploy"

## Usage

1. **Enter tickers**: Input stock ticker symbols (comma-separated, max 30)
2. **Select news sources**: Choose which news sources to scrape
3. **Choose analysis method**: Select VADER, FinBERT, or both
4. **Set analysis scope**: Choose to analyze headlines only, full content, or both
5. **Configure cache**: Set cache duration to avoid redundant scraping
6. **Click "Analyze Sentiments"**: Wait for the analysis to complete
7. **View results**: 
   - Summary table sorted by sentiment ratio
   - Detailed news articles with individual sentiment scores
   - Export results as CSV

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── news_scraper.py         # News scraping from multiple sources
├── sentiment_analyzer.py   # VADER and FinBERT sentiment analysis
├── cache_manager.py        # Caching system for efficiency
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Key Components

### News Scraper (`news_scraper.py`)
- Scrapes news from Finviz, Yahoo Finance, and Google News
- Fetches full article content when needed
- Handles errors gracefully
- Returns structured article data

### Sentiment Analyzer (`sentiment_analyzer.py`)
- VADER: Rule-based sentiment analysis
- FinBERT: Transformer-based financial sentiment analysis
- Analyzes headlines and/or full content
- Returns standardized sentiment scores and labels

### Cache Manager (`cache_manager.py`)
- Stores scraped news data with timestamps
- Configurable cache expiration
- Reduces redundant API calls and scraping
- Improves overall performance

## Performance Optimization

- **Parallel processing**: Uses ThreadPoolExecutor for concurrent ticker processing
- **Smart caching**: Avoids re-scraping recently fetched news
- **Lazy loading**: FinBERT model loads only when needed
- **Progress indicators**: Real-time feedback during processing
- **Error handling**: Graceful handling of scraping and analysis errors

## Configuration Options

- **Cache duration**: 5-120 minutes
- **Max tickers**: Up to 30 per analysis
- **Articles per source**: 5 articles per ticker per source
- **Analysis methods**: VADER, FinBERT, or both
- **Content scope**: Headlines, full content, or both

## Sentiment Calculation

### VADER
- Compound score > 0.05: Positive
- Compound score < -0.05: Negative
- Otherwise: Neutral

### FinBERT
- Uses softmax probabilities
- Label with highest probability is selected
- Classes: Positive, Negative, Neutral

### Sentiment Ratio
- Formula: `Positive / (Positive + Negative + 1)`
- Used for sorting tickers
- Higher ratio = more positive sentiment

## Troubleshooting

### Common Issues

1. **Slow performance**: 
   - Reduce number of tickers
   - Use cache effectively
   - Analyze headlines only instead of full content

2. **Scraping errors**:
   - Some websites may block automated requests
   - Try different news sources
   - Check internet connection

3. **Memory issues**:
   - FinBERT model requires significant memory
   - Consider using VADER only for large batches
   - Process fewer tickers at once

4. **Model download issues**:
   - Ensure internet connection
   - FinBERT downloads automatically on first use
   - May take time on first run

## Future Enhancements

- Add more news sources (Bloomberg, Reuters, etc.)
- Implement sentiment trend analysis over time
- Add data visualization (charts, graphs)
- Support for additional languages
- Comparison with historical sentiment data
- Alert system for significant sentiment changes

## Dependencies

- `streamlit`: Web application framework
- `pandas`: Data manipulation
- `requests`: HTTP requests
- `beautifulsoup4`: Web scraping
- `vaderSentiment`: VADER sentiment analysis
- `transformers`: FinBERT model
- `torch`: PyTorch for FinBERT
- `lxml`: HTML parsing

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.
