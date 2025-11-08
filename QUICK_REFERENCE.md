# Quick Reference Guide

## 🚀 Quick Start (3 Steps)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run stock_sentiment_app.py
   ```

3. **Use the app:**
   - Enter tickers (e.g., `AAPL, MSFT, GOOGL`)
   - Select news sources
   - Click "Analyze Sentiment"

## 📁 Project Files

| File | Purpose |
|------|---------|
| `stock_sentiment_app.py` | Main Streamlit application |
| `news_scrapers.py` | Web scraping functions |
| `sentiment_analyzer.py` | VADER & FinBERT models |
| `utils.py` | Helper functions |
| `requirements.txt` | Python dependencies |
| `test_app.py` | Test script |
| `setup.sh` | Automated setup |

## ⚙️ Configuration Options

### Input Settings
- **Max Tickers:** 30
- **News per Source:** 5 articles
- **Total Sources:** 3 (Finviz, Yahoo, Google)

### Analysis Modes
1. **Headlines Only** - Fast (10-30 sec)
2. **Full Content** - Thorough (1-3 min)
3. **Both Averaged** - Balanced

### Cache Settings
- **Duration:** 5-60 minutes (default: 15)
- **Purpose:** Avoid redundant scraping
- **Clear:** Button in sidebar

## 📊 Understanding Output

### Summary Table Columns
- `Ticker` - Stock symbol
- `Total News` - Articles analyzed
- `VADER Positive/Negative/Neutral` - Counts
- `VADER Ratio (P/N)` - Positive/Negative ratio
- `FinBERT Positive/Negative/Neutral` - Counts
- `FinBERT Ratio (P/N)` - Positive/Negative ratio

### Detailed Results Columns
- `Ticker`, `Source`, `Headline`, `Date`
- `VADER Sentiment` - Label (positive/negative/neutral)
- `VADER Score` - Compound score (-1 to +1)
- `FinBERT Sentiment` - Label
- `FinBERT Score` - Confidence (0 to 1)
- `URL` - Article link

## 🎯 Sentiment Interpretation

| Ratio | Interpretation |
|-------|---------------|
| > 2.0 | Strongly Positive |
| 1.0 - 2.0 | Moderately Positive |
| 0.5 - 1.0 | Moderately Negative |
| < 0.5 | Strongly Negative |
| ∞ | All positive (no negative) |

## ⚡ Performance Tips

### For Speed (10-30 seconds)
- Use 5-10 tickers max
- Select Finviz only
- Choose "Headlines Only"
- Set cache to 30 min

### For Accuracy (1-3 minutes)
- Use 3-5 tickers max
- Select all sources
- Choose "Both Averaged"
- Set cache to 15 min

## 🔧 Common Commands

### Setup
```bash
# Using setup script
chmod +x setup.sh
./setup.sh

# Manual setup
pip install -r requirements.txt
python test_app.py
```

### Running
```bash
# Normal run
streamlit run stock_sentiment_app.py

# Custom port
streamlit run stock_sentiment_app.py --server.port=8080

# Network access
streamlit run stock_sentiment_app.py --server.address=0.0.0.0
```

### Testing
```bash
# Run all tests
python test_app.py

# Test specific component
python -c "from sentiment_analyzer import analyze_vader_sentiment; print(analyze_vader_sentiment('Good news!'))"
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No news found | Verify ticker symbol |
| Slow performance | Reduce tickers or use "Headlines Only" |
| FinBERT loading slow | Normal on first use (downloads model) |
| Scraping blocked | Clear cache and retry |
| Memory error | Reduce batch size in sentiment_analyzer.py |

## 📦 Dependencies

**Core:**
- streamlit (UI framework)
- pandas (Data manipulation)
- requests + beautifulsoup4 (Web scraping)

**Sentiment:**
- vaderSentiment (VADER model)
- transformers (FinBERT)
- torch (PyTorch backend)

**Optional:**
- yfinance (Ticker validation)

## 🌐 Deployment URLs

- **Streamlit Cloud:** [share.streamlit.io](https://share.streamlit.io)
- **Documentation:** [docs.streamlit.io](https://docs.streamlit.io)
- **FinBERT Model:** [huggingface.co/ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert)

## 📝 Example Usage

### Basic Analysis
```
Input: AAPL, MSFT
Sources: Finviz ✓, Yahoo ✓
Mode: Headlines Only
Result: ~10 articles, 15 seconds
```

### Deep Analysis
```
Input: TSLA
Sources: All ✓
Mode: Both Averaged
Result: ~15 articles, 45 seconds
```

### Portfolio Monitoring
```
Input: AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA, AMD, INTC, NFLX
Sources: Finviz ✓
Mode: Headlines Only
Cache: 30 min
Result: ~50 articles, 30 seconds
```

## 🔑 Key Features

✓ Multi-source scraping
✓ Dual sentiment models
✓ Parallel processing
✓ Smart caching
✓ Progress tracking
✓ CSV export
✓ Session history
✓ Ticker filtering
✓ Error handling

## 📞 Support

- GitHub: Create an issue
- Docs: See README.md, DEPLOYMENT.md, EXAMPLES.md
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)

---

**Version:** 1.0  
**Last Updated:** November 2025
