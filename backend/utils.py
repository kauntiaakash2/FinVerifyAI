"""
Utility functions for caching, logging, and helper operations.
"""
import json
import hashlib
from datetime import datetime
from functools import wraps
from cachetools import TTLCache
from loguru import logger
from .config import settings

# Setup caching
cache = TTLCache(maxsize=100, ttl=settings.CACHE_TTL)


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments."""
    key = hashlib.md5(
        json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True).encode()
    ).hexdigest()
    return key


def log_function_call(func):
    """Decorator to log function calls and timing."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__}")
        start = datetime.now()
        try:
            result = await func(*args, **kwargs)
            duration = (datetime.now() - start).total_seconds()
            logger.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {str(e)}")
            raise
    return wrapper


def format_large_number(num: float) -> str:
    """Format large numbers with B/M/K suffixes."""
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"


def parse_value_with_unit(value_str: str) -> tuple:
    """Parse string like '94.9B' or '394billion' into (value, unit)."""
    value_str = value_str.strip().upper()
    multipliers = {
        'B': 1e9, 'M': 1e6, 'K': 1e3, 'T': 1e12,
        'BILLION': 1e9, 'MILLION': 1e6, 'THOUSAND': 1e3, 'TRILLION': 1e12,
    }

    for unit, multiplier in multipliers.items():
        if value_str.endswith(unit):
            try:
                num = float(value_str[:-len(unit)].strip())
                return num * multiplier, unit[0]
            except ValueError:
                pass

    try:
        return float(value_str), ''
    except ValueError:
        return 0.0, ''


# Configure logging
logger.remove()  # Remove default handler
logger.add(
    "logs/finverify.log",
    rotation="500 MB",
    retention="10 days",
    level=settings.LOG_LEVEL,
)
logger.add(
    lambda msg: print(msg, end=""),
    level=settings.LOG_LEVEL,
    format="{time} {level} {message}",
)
