"""
Multi-source financial data fetcher with automatic fallback.
Primary: yfinance (no API key required)
Secondary: Financial Modeling Prep (requires API key)
Tertiary: Alpha Vantage (requires API key)
"""
import yfinance as yf
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from .config import settings
from .utils import cache, log_function_call, logger


class DataFetcher:
    """Fetch financial data from multiple sources with fallback."""

    def __init__(self):
        self.sources = ["yfinance", "fmp", "alphavantage"]
        self.company_mapping = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "amazon": "AMZN",
            "tesla": "TSLA",
            "meta": "META",
            "facebook": "META",
            "netflix": "NFLX",
            "nvidia": "NVDA",
            "jpmorgan": "JPM",
            "jpmorgan chase": "JPM",
            "goldman sachs": "GS",
            "bank of america": "BAC",
            "berkshire": "BRK-A",
            "berkshire hathaway": "BRK-A",
        }

    def search_company(self, query: str) -> Optional[str]:
        """Search for company ticker by name."""
        query_lower = query.lower().strip()

        # Direct mapping
        if query_lower in self.company_mapping:
            return self.company_mapping[query_lower]

        # Partial matching
        for name, ticker in self.company_mapping.items():
            if name in query_lower or query_lower in name:
                return ticker

        # Try yfinance search as fallback
        try:
            tickers = yf.Tickers(query)
            if tickers.tickers:
                return list(tickers.tickers.keys())[0]
        except Exception:
            pass

        return None

    @log_function_call
    async def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """Get company profile from primary source with fallback."""
        cache_key_str = f"profile_{ticker}"

        if cache_key_str in cache:
            logger.info(f"Cache hit for {ticker} profile")
            return cache[cache_key_str]

        # Try primary source (yfinance)
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            profile = {
                "name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "forward_pe": info.get("forwardPE", 0),
                "revenue": info.get("totalRevenue", 0),
                "revenue_growth": info.get("revenueGrowth", 0),
                "profit_margins": info.get("profitMargins", 0),
                "website": info.get("website", ""),
                "source": "yfinance",
            }
            cache[cache_key_str] = profile
            return profile
        except Exception as e:
            logger.warning(f"yfinance failed for {ticker}: {e}")

        # Fallback to FMP if API key available
        if settings.FMP_API_KEY and settings.FMP_API_KEY != "your_fmp_api_key_here":
            try:
                url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}"
                response = requests.get(
                    url, params={"apikey": settings.FMP_API_KEY}, timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        profile = {
                            "name": data[0].get("companyName", ""),
                            "sector": data[0].get("sector", ""),
                            "industry": data[0].get("industry", ""),
                            "market_cap": data[0].get("mktCap", 0),
                            "pe_ratio": data[0].get("pe", 0),
                            "revenue": None,
                            "website": data[0].get("website", ""),
                            "source": "fmp",
                        }
                        cache[cache_key_str] = profile
                        return profile
            except Exception as e:
                logger.warning(f"FMP failed for {ticker}: {e}")

        return {"error": "No data available", "ticker": ticker}

    async def get_stock_price(self, ticker: str) -> float:
        """Get current stock price."""
        try:
            stock = yf.Ticker(ticker)
            return stock.info.get(
                "currentPrice", stock.info.get("regularMarketPrice", 0)
            )
        except Exception:
            return 0

    async def get_historical_prices(
        self, ticker: str, days: int = 30
    ) -> List[Dict]:
        """Get historical stock prices."""
        try:
            stock = yf.Ticker(ticker)
            end = datetime.now()
            start = end - timedelta(days=days)
            hist = stock.history(start=start, end=end)

            if hist.empty:
                return []

            prices = []
            for date, row in hist.iterrows():
                prices.append(
                    {
                        "date": str(date),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"]),
                    }
                )
            return prices
        except Exception as e:
            logger.error(f"Error fetching historical prices: {e}")
            return []

    async def get_financial_metric(self, ticker: str, metric: str) -> float:
        """Get specific financial metric."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            metric_map = {
                "revenue": "totalRevenue",
                "pe_ratio": "trailingPE",
                "market_cap": "marketCap",
                "eps": "trailingEps",
                "dividend_yield": "dividendYield",
                "profit_margin": "profitMargins",
                "stock_price": "currentPrice",
            }

            yf_metric = metric_map.get(metric)
            if yf_metric and yf_metric in info:
                return info[yf_metric]

            # Try secondary key for stock_price
            if metric == "stock_price":
                return info.get("regularMarketPrice", 0)

            # Fallback to FMP if available
            if (
                settings.FMP_API_KEY
                and settings.FMP_API_KEY != "your_fmp_api_key_here"
                and metric in ["revenue", "pe"]
            ):
                url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}"
                response = requests.get(
                    url, params={"apikey": settings.FMP_API_KEY}, timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    if data and metric == "revenue":
                        return data[0].get("revenuePerShare", 0) * info.get(
                            "sharesOutstanding", 1
                        )
                    elif data and metric == "pe":
                        return data[0].get("priceEarningsRatio", 0)

            return 0
        except Exception as e:
            logger.error(f"Error fetching metric {metric}: {e}")
            return 0


# Create global instance
fetcher = DataFetcher()
