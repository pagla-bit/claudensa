# Usage Examples

This document provides practical examples of using the Stock Sentiment Analyzer.

## Basic Usage

### Example 1: Single Ticker Analysis
**Input:**
- Ticker: `AAPL`
- Sources: Finviz, Yahoo Finance
- Mode: Headlines Only

**Expected Output:**
- Summary table showing sentiment counts
- Detailed view of 10-15 news headlines
- VADER and FinBERT sentiment for each article

### Example 2: Multiple Tech Stocks
**Input:**
```
AAPL, MSFT, GOOGL, AMZN, META
```
- Sources: All three (Finviz, Yahoo, Google News)
- Mode: Both (Averaged)

**Expected Output:**
- Comprehensive analysis across 5 tickers
- ~25-75 total articles analyzed
- Sorted by sentiment ratio

### Example 3: Sector Analysis
**Input:**
```
JPM, BAC, WFC, C, GS, MS
```
**Use Case:** Analyze sentiment across banking sector

### Example 4: Portfolio Monitoring
**Input:**
```
AAPL, TSLA, NVDA, AMD, INTC, MSFT, GOOGL, META, AMZN, NFLX
```
**Use Case:** Daily sentiment check for your portfolio holdings

## Advanced Usage

### Optimizing for Speed

**Fast Analysis (Headlines Only):**
- Use 5-10 tickers maximum
- Select only Finviz (fastest source)
- Choose "Headlines Only" mode
- Set cache to 30 minutes

**Expected Time:** 10-30 seconds for 10 tickers

### Optimizing for Depth

**Deep Analysis (Full Content):**
- Use 3-5 tickers maximum
- Select all news sources
- Choose "Both (Averaged)" mode
- Set cache to 15 minutes

**Expected Time:** 1-3 minutes for 5 tickers

## Interpreting Results

### Understanding Sentiment Ratios

**Ratio > 2.0**: Strongly positive sentiment
- Example: 10 positive, 3 negative = ratio of 3.33

**Ratio 1.0 - 2.0**: Moderately positive
- Example: 6 positive, 4 negative = ratio of 1.50

**Ratio 0.5 - 1.0**: Moderately negative
- Example: 3 positive, 5 negative = ratio of 0.60

**Ratio < 0.5**: Strongly negative
- Example: 2 positive, 8 negative = ratio of 0.25

### Comparing VADER vs FinBERT

**When They Agree:**
Both models show similar sentiment → High confidence in results

**When They Disagree:**
- VADER is rule-based (good for obvious sentiment)
- FinBERT is ML-based (better for nuanced financial language)
- Generally trust FinBERT for financial news

**Example Disagreement:**
- Headline: "Company misses earnings but provides optimistic guidance"
- VADER might focus on "misses" → Negative
- FinBERT considers full context → Neutral or Positive

## Sample Scenarios

### Scenario 1: Pre-Earnings Analysis
**Objective:** Gauge market sentiment before earnings announcement

**Steps:**
1. Enter ticker (e.g., `TSLA`)
2. Select all sources
3. Use "Full Content" mode
4. Analyze trends in recent news

**What to Look For:**
- Increasing negative sentiment → Possible earnings miss priced in
- Increasing positive sentiment → High expectations (risk of disappointment)
- Neutral sentiment → Market uncertainty

### Scenario 2: Sector Rotation Strategy
**Objective:** Identify sectors with improving sentiment

**Steps:**
1. Analyze representative stocks from each sector
2. Run analysis weekly
3. Compare sentiment ratios over time
4. Rotate towards improving sectors

**Example Sectors:**
- Tech: `AAPL, MSFT, GOOGL`
- Finance: `JPM, BAC, GS`
- Healthcare: `JNJ, UNH, PFE`
- Energy: `XOM, CVX, COP`

### Scenario 3: Crisis Detection
**Objective:** Early warning of negative news

**Steps:**
1. Add all portfolio holdings
2. Run daily analysis
3. Set up alerts for sentiment ratio < 0.5
4. Investigate causes of negative sentiment

**Red Flags:**
- Sudden drop in sentiment ratio
- Multiple negative articles from different sources
- FinBERT showing strong negative confidence (>0.8)

## Best Practices

### 1. Regular Monitoring
- Run analysis at consistent times (e.g., daily at market open)
- Track changes in sentiment over time
- Compare to price movements

### 2. Context Matters
- Don't rely solely on sentiment scores
- Read actual headlines and articles
- Consider broader market conditions
- Verify with fundamental analysis

### 3. Cache Management
- Use longer cache (30-60 min) for slower-moving stocks
- Use shorter cache (5-15 min) for volatile stocks or breaking news
- Clear cache when major news breaks

### 4. Source Selection
- **Finviz**: Best for quick, reliable headlines
- **Yahoo Finance**: Good for comprehensive coverage
- **Google News**: Broadest source variety

### 5. Analysis Mode Selection
- **Headlines Only**: Quick daily checks, fast execution
- **Full Content**: Deep dives, important decisions
- **Both Averaged**: Balanced approach, recommended default

## Common Issues and Solutions

### Issue: No News Found
**Possible Causes:**
- Ticker symbol incorrect
- Low-volume/small-cap stock with limited coverage
- Temporary scraping issue

**Solutions:**
- Verify ticker symbol
- Try different news sources
- Check again later

### Issue: Slow Performance
**Possible Causes:**
- Too many tickers (>15)
- Full content analysis on many articles
- Slow internet connection

**Solutions:**
- Reduce number of tickers
- Switch to "Headlines Only"
- Enable longer cache duration

### Issue: Unexpected Sentiment
**Possible Causes:**
- Sarcasm or complex language
- Mixed positive/negative in same article
- Domain-specific terminology

**Solutions:**
- Read the actual article
- Trust FinBERT over VADER for finance
- Consider neutral sentiment as "unclear"

## Export and Further Analysis

### CSV Export Options

**Summary Export:**
- Quick overview of all tickers
- Great for Excel pivot tables
- Track historical sentiment trends

**Detailed Export:**
- Full article-level data
- Can be used for custom analysis
- Machine learning training data

### Integration Ideas

1. **Excel Dashboard:**
   - Import CSV to Excel
   - Create charts showing sentiment trends
   - Use conditional formatting for alerts

2. **Google Sheets:**
   - Import for cloud-based tracking
   - Share with team/investment group
   - Set up automatic daily imports

3. **Python Analysis:**
   - Load CSV with pandas
   - Correlate sentiment with price movements
   - Build custom trading signals

## Tips for Different User Types

### Day Traders
- Focus on recent news (last 24 hours)
- Use "Headlines Only" for speed
- Monitor sentiment changes intraday
- Clear cache frequently

### Swing Traders
- Analyze 5-10 day sentiment trends
- Use "Both Averaged" mode
- Check before entering positions
- Look for sentiment divergence from price

### Long-Term Investors
- Focus on persistent negative sentiment
- Use "Full Content" for depth
- Less concerned with daily fluctuations
- Track quarterly trends

### Portfolio Managers
- Monitor entire portfolio daily
- Export to Excel for reporting
- Track sentiment vs performance
- Use for risk management

---

**Remember:** Sentiment analysis is a tool, not a crystal ball. Always combine with other analysis methods!
