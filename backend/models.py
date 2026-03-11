"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ClaimRequest(BaseModel):
    """Request model for claim verification."""
    claim: str = Field(..., description="Financial claim to verify", min_length=3)
    company_hint: Optional[str] = Field(None, description="Optional company name hint")


class VerificationDetail(BaseModel):
    """Detailed verification information."""
    company: str
    ticker: str
    metric: str
    claimed_value: float
    actual_value: float
    unit: str = ""
    source: str
    timestamp: datetime
    additional_context: Optional[Dict[str, Any]] = None


class VerificationResponse(BaseModel):
    """Response model for verification results."""
    claim: str
    confidence: float = Field(..., ge=0, le=100)
    reason: str
    verification: Optional[VerificationDetail] = None
    error: Optional[str] = None


class CompanyInfo(BaseModel):
    """Company information model."""
    name: str
    ticker: str
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    revenue: Optional[float] = None


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str
    timestamp: datetime
