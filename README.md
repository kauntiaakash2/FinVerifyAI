# FinVerify AI - Trust Gap Analyzer for Financial Claims

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/kauntiaakash2/FinVerifyAI)

## The Problem

77% of CFOs cite security and trust as critical risks in AI adoption. Financial AI systems operate as "black boxes," making decisions without explainability. **FinVerify AI** bridges this trust gap by providing source-verified validation of financial claims.

## Why This Project

This project directly aligns with 2025 technology initiatives:

- **Fact Verification Patent** - JPMorgan filed a patent for blockchain + ML fact verification in 2024
- **"Ask David" Multi-Agent System** - Their investment research tool acknowledges the "last mile accuracy" challenge
- **Agentic AI Focus** - Building AI agents that require trust and verification layers
- **High-Touch Advisory** - New advisory unit for clients on AI and cybersecurity

## Features

140+ Company Support: Verify claims about major global companies across all sectors
Real-Time Verification: Validate financial claims against live market data
Multiple Metrics: Revenue, P/E ratio, market cap, stock price, growth %, profit margin, dividend yield
Confidence Scoring: Algorithmic scoring with clear reasoning
Source Traceability: Every verified claim links to its data source
Multi-Source Fallback: yfinance primary, FMP/Alpha Vantage as backup
Historical Context: View 30-day price trends for verified companies
Beautiful UI: Modern, responsive design with confidence visualizations
Production-Ready: Deployed and scalable on Vercel

## Supported Companies

Over 140 companies across all major sectors:

**Technology:** Apple, Microsoft, Google, Amazon, Tesla, Nvidia, Intel, AMD, Qualcomm, Oracle, Adobe, Salesforce

**Finance:** JPMorgan Chase, Goldman Sachs, Bank of America, Wells Fargo, Morgan Stanley, Citigroup, Charles Schwab

**Healthcare:** Pfizer, Moderna, Johnson & Johnson, Eli Lilly, Merck, AstraZeneca

**Consumer:** Coca-Cola, Walmart, Starbucks, McDonald's, Target, Costco

**Automotive:** General Motors, Ford, Toyota, Volkswagen, BMW

**Energy:** Exxon Mobil, Chevron, Shell, BP

**Fintech:** PayPal, Coinbase, Square, Affirm, Robinhood

**E-commerce:** Alibaba, Shopify, eBay, Sea Limited

**And 50+ more across all industries!**

## Tech Stack

### Backend
- **FastAPI** - Modern, high-performance Python web framework
- **yfinance** - Real-time financial data (no API key required)
- **Pydantic** - Data validation and type checking
- **CacheTools** - Intelligent caching for performance
- **Loguru** - Structured logging
- **Python 3.11** - Latest stable Python

### Frontend
- **HTML5 + CSS3** - Modern markup and styling
- **Vanilla JavaScript** - No framework overhead
- **Responsive Design** - Mobile-friendly interface

### DevOps & Deployment
- **Vercel** - Serverless deployment (main platform)
- **GitHub** - Version control and CI/CD
- **Docker** - Container support

## Installation

### Prerequisites
- Python 3.11+
- Git
- pip

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/kauntiaakash2/FinVerifyAI.git
cd FinVerifyAI
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API keys (optional but recommended):**
```bash
cp .env.example .env
# Edit .env with your API keys:
# - FMP_API_KEY (from https://financialmodelingprep.com)
# - ALPHA_VANTAGE_KEY (from https://www.alphavantage.co)
# - FRED_API_KEY (from https://fred.stlouisfed.org)
```

5. **Run the application:**
```bash
python -m backend.main
```

6. **Access the application:**
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## API Documentation

### Live Demo
Production URL: https://fin-verify-ai.vercel.app
API Docs: https://fin-verify-ai.vercel.app/docs

### Key Endpoints

#### POST `/api/verify`
Verify a financial claim.

**Request:**
```json
{
  "claim": "Apple's revenue is $394 billion"
}
```

**Response:**
```json
{
  "claim": "Apple's revenue is $394 billion",
  "confidence": 70,
  "reason": "Moderately off",
  "verification": {
    "company": "Apple",
    "ticker": "AAPL",
    "metric": "revenue",
    "claimed_value": 394000000000,
    "actual_value": 435617005568,
    "unit": "B",
    "source": "Yahoo Finance",
    "timestamp": "2026-04-02T01:28:16.915435"
  },
  "error": null
}
```

#### GET `/api/health`
Check service health.

#### GET `/api/examples`
Get example claims for testing.

#### GET `/api/companies`
List all supported companies.

#### GET `/api/metrics/{ticker}`
Get detailed metrics for a company.

#### GET `/api/historical/{ticker}?days=30`
Get historical price data.

## Deployment

### Deploy to Vercel (Recommended)

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

**Quick Deploy:**
1. Go to https://vercel.com/import
2. Select your GitHub repository
3. Add environment variables (API keys)
4. Deploy

**Via CLI:**
```bash
npm i -g vercel
vercel login
vercel --prod
```

## Security and Configuration

### Environment Variables

Required for full functionality:
```
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
CACHE_TTL=300
RATE_LIMIT_PER_MINUTE=10
PRIMARY_DATA_SOURCE=yfinance

# Optional (fallback data sources)
FMP_API_KEY=your_key_here
ALPHA_VANTAGE_KEY=your_key_here
FRED_API_KEY=your_key_here
```

### Features
Rate limiting (10 requests/minute per IP)
Secure environment variable management
CORS enabled for cross-origin requests
Input validation on all endpoints
Comprehensive error handling

## Metrics Supported

- **Revenue** - Total company revenue
- **P/E Ratio** - Price-to-earnings ratio  
- **Market Cap** - Total market capitalization
- **Stock Price** - Current stock price
- **Growth %** - Year-over-year growth
- **Profit Margin** - Profitability percentage
- **Dividend Yield** - Dividend yield percentage
- **EPS** - Earnings per share

## Testing

Run tests locally:
```bash
pytest tests/
pytest tests/test_api.py
pytest tests/test_verifier.py
```

## Project Structure

```
FinVerifyAI/
├── api/
│   └── index.py                 # Vercel entrypoint
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Configuration
│   ├── models.py                # Pydantic models
│   ├── verifier.py              # Verification logic
│   ├── data_fetcher.py          # Data fetching
│   └── utils.py                 # Utilities
├── frontend/
│   ├── index.html               # Web UI
│   └── script.js                # Frontend logic
├── tests/
│   ├── test_api.py
│   └── test_verifier.py
├── requirements.txt             # All dependencies
├── requirements-prod.txt        # Production dependencies
├── vercel.json                  # Vercel config
├── .vercelignore                # Vercel build ignore
├── DEPLOYMENT.md                # Deployment guide
└── README.md                    # This file
```

## How It Works

1. **Claim Extraction** - Parse user input to extract company name and financial metric
2. **Company Identification** - Map company name to ticker symbol
3. **Data Fetching** - Retrieve real-time data from multiple sources
4. **Comparison** - Compare claimed value with actual data
5. **Confidence Scoring** - Calculate confidence based on accuracy
6. **Response** - Return detailed verification result with source attribution

## Use Cases

Validate financial claims in news articles
Verify investor presentations
Check earnings call claims
Fact-check social media financial posts
Education tool for finance students
Internal compliance verification

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- **JPMorgan Chase** - Inspiration from their AI and verification initiatives
- **Yahoo Finance** - Real-time financial data
- **Financial Modeling Prep** - Additional financial data source
- **FastAPI Community** - Excellent framework and documentation
- **Vercel** - Easy deployment platform

## Support

For questions, issues, or suggestions:
1. Check existing [issues](https://github.com/kauntiaakash2/FinVerifyAI/issues)
2. See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment help
3. Review [API Documentation](https://fin-verify-ai.vercel.app/docs)

## Roadmap

Machine learning confidence scoring
Real-time news integration
Batch claim verification
Advanced analytics dashboard
Mobile app
Browser extension
Blockchain verification records
Multi-language support

## Show Your Support

If you find this project helpful, please give it a star on GitHub.

Made for the fintech community

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
