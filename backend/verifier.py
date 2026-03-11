"""
Core claim verification engine with entity extraction and confidence scoring.
"""
import re
from typing import Dict, Any, Tuple
from datetime import datetime

from .data_fetcher import fetcher
from .utils import parse_value_with_unit, logger


class FinancialVerifier:
    """Verify financial claims against real-time data."""

    def __init__(self):
        # Enhanced pattern matching
        self.patterns = {
            "revenue": [
                r"revenue.*?\$?(\d+\.?\d*)\s*(billion|trillion|million|[BMKT])\b",
                r"sales.*?\$?(\d+\.?\d*)\s*(billion|trillion|million|[BMKT])\b",
                r"earnings.*?\$?(\d+\.?\d*)\s*(billion|trillion|million|[BMKT])\b",
            ],
            "pe_ratio": [
                r"p/e.*?(\d+\.?\d*)",
                r"price.+?earnings.*?(\d+\.?\d*)",
                r"pe ratio.*?(\d+\.?\d*)",
                r"pe.*?ratio.*?(\d+\.?\d*)",
            ],
            "stock_price": [
                r"stock.*?price.*?\$?(\d+\.?\d*)",
                r"share.*?price.*?\$?(\d+\.?\d*)",
                r"trading at.*?\$?(\d+\.?\d*)",
            ],
            "growth": [
                r"grew.*?(\d+\.?\d*)\s*%",
                r"growth.*?(\d+\.?\d*)\s*%",
                r"increased.*?(\d+\.?\d*)\s*%",
            ],
            "market_cap": [
                r"market.*?cap.*?\$?(\d+\.?\d*)\s*(billion|trillion|million|[BMKT])\b",
                r"valuation.*?\$?(\d+\.?\d*)\s*(billion|trillion|million|[BMKT])\b",
                r"worth.*?\$?(\d+\.?\d*)\s*(billion|trillion|million|[BMKT])\b",
            ],
            "profit_margin": [
                r"profit.*?margin.*?(\d+\.?\d*)\s*%",
                r"margin.*?(\d+\.?\d*)\s*%",
            ],
            "dividend_yield": [
                r"dividend.*?yield.*?(\d+\.?\d*)\s*%",
                r"yield.*?(\d+\.?\d*)\s*%",
            ],
        }

        # Confidence thresholds
        self.confidence_thresholds = {
            "excellent": (95, "Highly accurate"),
            "good": (85, "Slightly off"),
            "fair": (70, "Moderately off"),
            "poor": (40, "Significantly off"),
            "invalid": (0, "Could not verify"),
        }

    def extract_entities(self, claim: str) -> Dict[str, Any]:
        """Extract company, metric, and value from claim."""
        result = {
            "company": None,
            "ticker": None,
            "metric": None,
            "value": 0.0,
            "unit": "",
            "confidence": 0,
        }

        # Extract company
        for name, ticker in fetcher.company_mapping.items():
            if name in claim.lower():
                result["company"] = name.title()
                result["ticker"] = ticker
                break

        if not result["ticker"]:
            # Try fuzzy matching
            words = claim.lower().split()
            for word in words:
                ticker = fetcher.search_company(word)
                if ticker:
                    result["ticker"] = ticker
                    result["company"] = word.title()
                    break

        # Extract metric and value
        claim_lower = claim.lower().replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
        for metric, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, claim_lower)
                if match:
                    result["metric"] = metric
                    value_str = match.group(1)
                    unit = match.group(2) if len(match.groups()) > 1 else ""

                    # Parse value
                    value, parsed_unit = parse_value_with_unit(value_str + unit)
                    result["value"] = value
                    result["unit"] = parsed_unit or unit
                    break
            if result["metric"]:
                break

        return result

    async def calculate_confidence(
        self, claimed_value: float, actual_value: float, metric: str
    ) -> Tuple[float, str]:
        """Calculate confidence score based on accuracy."""
        if actual_value == 0:
            return self.confidence_thresholds["invalid"]

        # Calculate percent difference
        if metric in ["pe_ratio", "dividend_yield", "profit_margin"]:
            percent_diff = abs(claimed_value - actual_value) / actual_value * 100
        else:
            diff = abs(claimed_value - actual_value)
            percent_diff = (diff / actual_value) * 100

        # Determine confidence level
        if percent_diff < 1:
            return self.confidence_thresholds["excellent"]
        elif percent_diff < 5:
            return self.confidence_thresholds["good"]
        elif percent_diff < 15:
            return self.confidence_thresholds["fair"]
        else:
            return self.confidence_thresholds["poor"]

    async def verify_claim(self, claim: str) -> Dict[str, Any]:
        """Main verification function."""
        logger.info(f"Verifying claim: {claim}")

        # Extract entities
        entities = self.extract_entities(claim)

        if not entities["ticker"]:
            return {
                "claim": claim,
                "confidence": 0,
                "reason": "Could not identify company",
                "error": "Company not recognized. Please specify a valid company name.",
                "verification": None,
            }

        if not entities["metric"]:
            return {
                "claim": claim,
                "confidence": 0,
                "reason": "Could not identify financial metric",
                "error": "Metric not recognized. Please specify revenue, P/E ratio, etc.",
                "verification": None,
            }

        # Fetch actual data
        actual_value = await fetcher.get_financial_metric(
            entities["ticker"], entities["metric"]
        )

        if actual_value == 0:
            return {
                "claim": claim,
                "confidence": 0,
                "reason": "Could not fetch verification data",
                "error": f'No data available for {entities["ticker"]} metric: {entities["metric"]}',
                "verification": None,
            }

        # Calculate confidence
        confidence, reason = await self.calculate_confidence(
            entities["value"], actual_value, entities["metric"]
        )

        # Build verification detail
        verification = {
            "company": entities["company"] or entities["ticker"],
            "ticker": entities["ticker"],
            "metric": entities["metric"],
            "claimed_value": entities["value"],
            "actual_value": actual_value,
            "unit": entities["unit"],
            "source": "Yahoo Finance",
            "timestamp": datetime.now().isoformat(),
            "additional_context": {
                "claimed_formatted": self.format_value(
                    entities["value"], entities["metric"]
                ),
                "actual_formatted": self.format_value(actual_value, entities["metric"]),
                "percent_difference": self.calculate_percent_diff(
                    entities["value"], actual_value
                ),
            },
        }

        return {
            "claim": claim,
            "confidence": confidence,
            "reason": reason,
            "verification": verification,
            "error": None,
        }

    def format_value(self, value: float, metric: str) -> str:
        """Format value based on metric type."""
        if metric in ["pe_ratio", "dividend_yield", "profit_margin"]:
            return f"{value:.2f}"
        elif metric in ["revenue", "market_cap"]:
            if value >= 1e12:
                return f"${value/1e12:.2f}T"
            elif value >= 1e9:
                return f"${value/1e9:.2f}B"
            elif value >= 1e6:
                return f"${value/1e6:.2f}M"
            else:
                return f"${value:,.0f}"
        else:
            return f"${value:,.2f}"

    def calculate_percent_diff(self, claimed: float, actual: float) -> str:
        """Calculate percentage difference."""
        if actual == 0:
            return "N/A"
        diff = ((claimed - actual) / actual) * 100
        return f"{diff:+.1f}%"


# Global instance
verifier = FinancialVerifier()
