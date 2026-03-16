# FinVerify AI - Trust Gap Analyzer for Financial Claims

## The Problem

77% of CFOs cite security and trust as critical risks in AI adoption. Financial AI systems operate as "black boxes," making decisions without explainability. **FinVerify AI** bridges this trust gap by providing source-verified validation of financial claims.

## Why This Project

This project directly aligns with 2025 technology initiatives:

- **Fact Verification Patent** - JPMorgan filed a patent for blockchain + ML fact verification in 2024
- **"Ask David" Multi-Agent System** - Their investment research tool acknowledges the "last mile accuracy" challenge
- **Agentic AI Focus** - Building AI agents that require trust and verification layers
- **High-Touch Advisory** - New advisory unit for clients on AI and cybersecurity

## Features

- **Claim Verification** - Validate financial claims against real-time market data
- **Confidence Scoring** - Algorithmic scoring with clear reasoning
- **Source Traceability** - Every verified claim links to its data source
- **Multi-Source Fallback** - yfinance primary, FMP/Alpha Vantage as backup
- **Historical Context** - View 30-day price trends for verified companies
- **Beautiful UI** - Modern, responsive design with confidence visualizations

## Tech Stack

### Backend
- **FastAPI** - High-performance Python API framework
- **yfinance** - Yahoo Finance data (no API key required)
- **Pydantic** - Data validation and settings management
- **CacheTools** - In-memory caching for rate limiting

### Frontend
- **HTML5 + Tailwind CSS** - Modern, responsive UI
- **Chart.js** - Interactive data visualizations
- **Vanilla JavaScript** - No framework bloat

### DevOps
- **Render** - Cloud deployment
- **GitHub Actions** - CI/CD pipeline
- **Docker** - Containerization

## Installation

### Prerequisites
- Python 3.11+
- Git

### Local Setup

```bash
# Clone repository
git clone https://github.com/yourusername/FinVerifyAI.git
cd FinVerifyAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys (optional)

# Run the application
uvicorn backend.main:app --reload

# Open browser to http://localhost:8000
```

## Usage Examples

Try these sample claims:

```
"Apple revenue is $394.8 billion"
"Microsoft P/E ratio is 35"
"Tesla stock price is $250"
"Amazon market cap is $1.7 trillion"
"JPMorgan profit margin is 35%"
"Nvidia grew 200% this year"
```

## API Keys (Optional)

The app works without API keys using yfinance. For additional data sources:

| Service | API Key Required | Free Tier |
|---------|-----------------|-----------|
| Yahoo Finance | No | Unlimited |
| Financial Modeling Prep | Yes | 250 req/day |
| Alpha Vantage | Yes | 5 calls/min |

Get keys at:
- [Financial Modeling Prep](https://financialmodelingprep.com/register)
- [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────>│   FastAPI    │────>│  Data Layer │
│  (HTML/JS)  │<────│   Backend    │<────│  (yfinance) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────v──────┐
                    │  Cache      │
                    │  (TTLCache) │
                    └─────────────┘
```

## Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=backend tests/ --cov-report=html
```

## Deployment

### Deploy to Render (Free)

1. Push code to GitHub
2. Connect repository to Render
3. Use `render.yaml` for configuration
4. Add environment variables

### Deploy with Docker

```bash
# Build image
docker build -t finverify-ai .

# Run container
docker run -p 8000:8000 finverify-ai
```

## API Documentation

Once running, visit `/docs` for interactive API documentation.

### Verify Claim Endpoint

```http
POST /api/verify
Content-Type: application/json

{
    "claim": "Apple revenue is $394 billion"
}
```

Response:
```json
{
    "claim": "Apple revenue is $394 billion",
    "confidence": 87,
    "reason": "Slightly off",
    "verification": {
        "company": "Apple",
        "ticker": "AAPL",
        "metric": "revenue",
        "claimed_value": 394000000000,
        "actual_value": 383285000000,
        "source": "Yahoo Finance",
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

## Future Enhancements

- [ ] SEC EDGAR integration for filing data
- [ ] FRED API for economic indicators
- [ ] NLP improvements with transformer models
- [ ] Blockchain verification trail
- [ ] Mobile app with push notifications
