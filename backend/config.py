"""
Configuration management for FinVerify AI.
Loads environment variables and provides typed configuration.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Keys
    FMP_API_KEY: Optional[str] = os.getenv("FMP_API_KEY")
    ALPHA_VANTAGE_KEY: Optional[str] = os.getenv("ALPHA_VANTAGE_KEY")
    FRED_API_KEY: Optional[str] = os.getenv("FRED_API_KEY")

    # Application Settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    PRIMARY_DATA_SOURCE: str = os.getenv("PRIMARY_DATA_SOURCE", "yfinance")

    # API Configuration
    API_TITLE: str = "FinVerify AI"
    API_DESCRIPTION: str = "Trust Gap Analyzer for Financial Claims"
    API_VERSION: str = "1.0.0"

    # CORS
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        case_sensitive = True


settings = Settings()
