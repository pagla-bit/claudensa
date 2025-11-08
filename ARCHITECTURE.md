# System Architecture

## Application Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│                   (Streamlit App)                            │
│                                                              │
│  [Ticker Input] [Source Selection] [Analysis Mode] [Cache]  │
│                                                              │
│              [🚀 Analyze Sentiment Button]                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   MAIN APPLICATION                           │
│              (stock_sentiment_app.py)                        │
│                                                              │
│  • Parse & validate tickers                                  │
│  • Check cache for existing data                             │
│  • Manage progress tracking                                  │
│  • Coordinate parallel processing                            │
│  • Aggregate results                                         │
│  • Update session state                                      │
└────────────┬─────────────────────────┬──────────────────────┘
             │                         │
             ▼                         ▼
┌────────────────────────┐   ┌────────────────────────────────┐
│   NEWS SCRAPING        │   │   SENTIMENT ANALYSIS           │
│  (news_scrapers.py)    │   │  (sentiment_analyzer.py)       │
│                        │   │                                │
│ ┌────────────────────┐ │   │ ┌────────────────────────────┐ │
│ │  scrape_finviz()   │ │   │ │  analyze_vader_sentiment() │ │
│ │  • Parse HTML      │ │   │ │  • Rule-based analysis     │ │
│ │  • Extract news    │ │   │ │  • Compound score          │ │
│ │  • Get headlines   │ │   │ │  • Fast execution          │ │
│ └────────────────────┘ │   │ └────────────────────────────┘ │
│                        │   │                                │
│ ┌────────────────────┐ │   │ ┌────────────────────────────┐ │
│ │  scrape_yahoo()    │ │   │ │ analyze_finbert_sentiment()│ │
│ │  • Parse HTML      │ │   │ │  • ML-based analysis       │ │
│ │  • Extract news    │ │   │ │  • Confidence scores       │ │
│ │  • Get content     │ │   │ │  • Financial context       │ │
│ └────────────────────┘ │   │ └────────────────────────────┘ │
│                        │   │                                │
│ ┌────────────────────┐ │   │ ┌────────────────────────────┐ │
│ │ scrape_google_news()│ │   │ │  load_finbert()           │ │
│ │  • Parse HTML      │ │   │ │  • Lazy model loading      │ │
│ │  • Extract news    │ │   │ │  • Tokenization            │ │
│ │  • Get headlines   │ │   │ │  • Batch processing        │ │
│ └────────────────────┘ │   │ └────────────────────────────┘ │
│                        │   │                                │
│ ┌────────────────────┐ │   └────────────────────────────────┘
│ │fetch_article_      │ │
│ │content()           │ │
│ │  • HTTP requests   │ │
│ │  • Content extract │ │
│ │  • Text cleaning   │ │
│ └────────────────────┘ │
└────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   UTILITY FUNCTIONS                          │
│                     (utils.py)                               │
│                                                              │
│  • validate_ticker() - Check ticker validity                 │
│  • clean_ticker() - Format ticker symbols                    │
│  • format_results() - Structure output data                  │
│  • calculate_sentiment_ratio() - P/N ratio                   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Input Tickers (e.g., "AAPL, MSFT, GOOGL")
    │
    ▼
Parse & Validate
    │
    ├─→ AAPL ──┬─→ Check Cache ──┬─→ [HIT] → Use cached data
    │          │                 │
    │          └─→ [MISS] ──┬────┴─→ scrape_finviz()
    │                        ├──────→ scrape_yahoo()
    │                        └──────→ scrape_google_news()
    │                                     │
    │                                     ▼
    │                           Collect News Articles
    │                           (Headlines + Content)
    │                                     │
    │                                     ▼
    ├──────────────────────────> For Each Article:
    │                                     │
    │                                     ├─→ analyze_vader_sentiment()
    │                                     │   • Get label (pos/neg/neu)
    │                                     │   • Get compound score
    │                                     │
    │                                     └─→ analyze_finbert_sentiment()
    │                                         • Get label (pos/neg/neu)
    │                                         • Get confidence score
    │                                                 │
    │                                                 ▼
    │                                      Store Results with:
    │                                      • Ticker
    │                                      • Source
    │                                      • Headline
    │                                      • Date
    │                                      • VADER sentiment & score
    │                                      • FinBERT sentiment & score
    │                                      • URL
    │
    ├─→ MSFT (same process)
    │
    └─→ GOOGL (same process)
            │
            ▼
    Aggregate All Results
            │
            ├─→ Create Summary Table:
            │   • Count positive/negative/neutral per ticker
            │   • Calculate sentiment ratios
            │   • Sort by ratio
            │
            └─→ Create Detailed Table:
                • All articles with full sentiment data
                • Filterable by ticker
                │
                ▼
    Display Results + Export Options
```

## Component Interaction

```
┌──────────────────┐
│  Streamlit App   │
│  (Frontend)      │
└────────┬─────────┘
         │
         │ User input, configuration
         │
         ▼
┌──────────────────┐
│  Main Controller │◄──────┐
│  (Orchestration) │       │
└────────┬─────────┘       │
         │                 │
         │ Parallel        │ Cache
         │ Processing      │ Read/Write
         │                 │
         ├─────────────────┤
         │                 │
    ┌────▼────┐      ┌────▼────┐
    │ Scraper │      │  Cache  │
    │ Module  │      │ Storage │
    └────┬────┘      └─────────┘
         │
         │ Raw news data
         │
         ▼
    ┌────────────┐
    │ Sentiment  │
    │ Analyzer   │
    └────┬───────┘
         │
         │ Analyzed data
         │
         ▼
    ┌────────────┐
    │  Results   │
    │ Aggregator │
    └────┬───────┘
         │
         │ Formatted results
         │
         ▼
┌──────────────────┐
│  Display Layer   │
│  (Tables, CSV)   │
└──────────────────┘
```

## Caching Strategy

```
Request for Ticker "AAPL" at 10:00 AM
    │
    ▼
Generate Cache Key: "AAPL_Finviz_202511081000"
    │
    ├─→ Check st.session_state.cache
    │
    ├─→ [KEY EXISTS & FRESH]
    │   │
    │   └─→ Return cached data (instant)
    │
    └─→ [KEY MISSING OR EXPIRED]
        │
        └─→ Scrape fresh data
            │
            └─→ Store in cache with timestamp
                │
                └─→ Return fresh data
```

## Error Handling Flow

```
Operation Attempt
    │
    ├─→ [SUCCESS] → Continue
    │
    └─→ [ERROR]
        │
        ├─→ Network Error
        │   └─→ Log warning
        │       └─→ Continue with other sources
        │
        ├─→ Parsing Error
        │   └─→ Skip article
        │       └─→ Continue with next article
        │
        ├─→ Invalid Ticker
        │   └─→ Skip ticker
        │       └─→ Continue with next ticker
        │
        └─→ Model Error
            └─→ Fallback to default sentiment
                └─→ Continue processing
```

## Performance Optimization

### Parallel Processing
```
Sequential (slow):
AAPL → wait → MSFT → wait → GOOGL → wait (90 seconds)

Parallel (fast):
┌─→ AAPL ─┐
├─→ MSFT ─┤→ All complete (30 seconds)
└─→ GOOGL ─┘
```

### Lazy Loading
```
App Start → Load UI (instant)
    │
    └─→ First FinBERT request → Load model (2 min)
        │
        └─→ Subsequent requests → Use cached model (instant)
```

### Caching Benefits
```
Without Cache:
Request 1 → Scrape (5s) → Analyze (3s) = 8s
Request 2 → Scrape (5s) → Analyze (3s) = 8s
Total: 16s

With Cache:
Request 1 → Scrape (5s) → Analyze (3s) → Cache = 8s
Request 2 → Cache hit (0.1s) → Analyze (3s) = 3.1s
Total: 11.1s (31% faster)
```

## Technology Stack

```
┌─────────────────────────────────────┐
│         Frontend Layer              │
│  • Streamlit (UI framework)         │
│  • HTML/CSS (via Streamlit)         │
└─────────────────────────────────────┘
                │
┌─────────────────────────────────────┐
│       Application Layer             │
│  • Python 3.8+                      │
│  • Pandas (data manipulation)       │
│  • Session state management         │
└─────────────────────────────────────┘
                │
┌─────────────────────────────────────┐
│         Data Layer                  │
│  • Requests (HTTP)                  │
│  • BeautifulSoup4 (parsing)         │
│  • In-memory caching                │
└─────────────────────────────────────┘
                │
┌─────────────────────────────────────┐
│          AI/ML Layer                │
│  • VADER (rule-based NLP)           │
│  • FinBERT (transformer model)      │
│  • PyTorch (deep learning)          │
└─────────────────────────────────────┘
```

## Scalability Considerations

### Current Limits
- **Tickers:** 30 per request
- **Articles:** 5 per ticker per source
- **Max Articles:** 450 total (30 × 5 × 3)
- **Processing Time:** 2-5 minutes for max load

### Scaling Options

1. **Horizontal Scaling**
   - Deploy multiple instances
   - Load balance requests
   - Shared cache layer (Redis)

2. **Vertical Scaling**
   - Increase FinBERT batch size
   - Add more CPU cores
   - Increase memory for larger models

3. **Optimization**
   - Implement database caching
   - Pre-compute popular tickers
   - Add CDN for static assets
   - Use async scraping

---

This architecture provides a solid foundation for efficient, scalable sentiment analysis while maintaining code modularity and maintainability.
