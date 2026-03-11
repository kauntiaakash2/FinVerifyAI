import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.verifier import FinancialVerifier
from backend.data_fetcher import DataFetcher


@pytest.mark.asyncio
async def test_entity_extraction():
    v = FinancialVerifier()

    # Test revenue extraction
    result = v.extract_entities("Apple revenue is $394 billion")
    assert result["company"] == "Apple"
    assert result["ticker"] == "AAPL"
    assert result["metric"] == "revenue"
    assert result["value"] > 0

    # Test P/E extraction
    result = v.extract_entities("Microsoft P/E ratio is 35")
    assert result["company"] == "Microsoft"
    assert result["ticker"] == "MSFT"
    assert result["metric"] == "pe_ratio"


@pytest.mark.asyncio
async def test_confidence_scoring():
    v = FinancialVerifier()

    # Test exact match
    conf, reason = await v.calculate_confidence(100, 100, "revenue")
    assert conf >= 95

    # Test close match (5% diff = 'fair' threshold = 70)
    conf, reason = await v.calculate_confidence(105, 100, "revenue")
    assert 70 <= conf <= 95


@pytest.mark.asyncio
async def test_data_fetcher():
    f = DataFetcher()

    # Test company search
    ticker = f.search_company("Apple")
    assert ticker == "AAPL"

    # Test profile fetch
    profile = await f.get_company_profile("AAPL")
    assert profile is not None
    assert "name" in profile
