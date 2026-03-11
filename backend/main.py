"""
Main FastAPI application for FinVerify AI.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import datetime
import time
from typing import Dict

from .config import settings
from .models import ClaimRequest, VerificationResponse, HealthCheck
from .verifier import verifier
from .data_fetcher import fetcher
from .utils import logger

# Rate limiting storage
request_counts: Dict[str, list] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup/shutdown."""
    logger.info(f"Starting FinVerify AI in {settings.ENVIRONMENT} mode")
    yield
    logger.info("Shutting down FinVerify AI")


# Initialize FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="frontend")

# Serve static files from frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple rate limiting by IP."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Clean old requests
    if client_ip in request_counts:
        request_counts[client_ip] = [
            t for t in request_counts[client_ip] if now - t < 60
        ]
    else:
        request_counts[client_ip] = []

    # Check rate limit
    if len(request_counts[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Please try again later."},
        )

    # Add request
    request_counts[client_ip].append(now)

    # Process request
    response = await call_next(request)
    return response


# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML interface."""
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": settings.API_TITLE}
    )


@app.get("/api/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "timestamp": datetime.now(),
    }


@app.post("/api/verify", response_model=VerificationResponse)
async def verify_claim(claim_request: ClaimRequest):
    """Verify a financial claim."""
    logger.info(f"Received verification request: {claim_request.claim}")

    try:
        result = await verifier.verify_claim(claim_request.claim)
        return result
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/companies")
async def list_companies():
    """List supported companies."""
    return {
        "companies": [
            {"name": name.title(), "ticker": ticker}
            for name, ticker in fetcher.company_mapping.items()
        ][:20]
    }


@app.get("/api/examples")
async def get_examples():
    """Get example claims for testing."""
    return {
        "examples": [
            "Apple revenue is $394 billion",
            "Microsoft P/E ratio is 35",
            "Tesla stock price is $250",
            "Amazon market cap is $1.7 trillion",
            "JPMorgan profit margin is 35%",
            "Nvidia grew 200% this year",
        ]
    }


@app.get("/api/metrics/{ticker}")
async def get_company_metrics(ticker: str):
    """Get available metrics for a ticker."""
    try:
        profile = await fetcher.get_company_profile(ticker.upper())
        return profile
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/historical/{ticker}")
async def get_historical(ticker: str, days: int = 30):
    """Get historical prices for a ticker."""
    try:
        prices = await fetcher.get_historical_prices(ticker.upper(), days)
        return prices
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Resource not found"})


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal error: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG
    )
