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
import os
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
    try:
        logger.info(f"Starting FinVerify AI in {settings.ENVIRONMENT} mode")
    except Exception as e:
        print(f"Error logging startup: {e}")
    yield
    try:
        logger.info("Shutting down FinVerify AI")
    except Exception as e:
        print(f"Error logging shutdown: {e}")


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

# Templates - Use absolute path for Vercel compatibility
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
try:
    templates = Jinja2Templates(directory=template_dir)
except Exception as e:
    print(f"Warning: Could not load templates from {template_dir}: {e}")
    templates = None

# Serve static files from frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple rate limiting by IP."""
    try:
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
    except Exception as e:
        logger.error(f"Middleware error: {str(e)}")
        # Still process the request even if middleware fails
        try:
            response = await call_next(request)
            return response
        except Exception as inner_e:
            logger.error(f"Request processing failed: {str(inner_e)}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )


# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML interface."""
    if templates:
        return templates.TemplateResponse(
            "index.html", {"request": request, "title": settings.API_TITLE}
        )
    else:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>FinVerify AI</title>
        </head>
        <body>
            <h1>FinVerify AI - API Server</h1>
            <p>Welcome to FinVerify AI. Use the API endpoints:</p>
            <ul>
                <li><a href="/docs">/docs - API documentation</a></li>
                <li><a href="/api/health">/api/health - Health check</a></li>
                <li><post>/api/verify - Verify financial claims</post></li>
            </ul>
        </body>
        </html>
        """


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    try:
        return {
            "status": "healthy",
            "service": settings.API_TITLE,
            "version": settings.API_VERSION,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "degraded",
            "service": settings.API_TITLE,
            "version": settings.API_VERSION,
            "error": str(e),
        }


@app.post("/api/verify")
async def verify_claim(claim_request: ClaimRequest):
    """Verify a financial claim."""
    try:
        logger.info(f"Received verification request: {claim_request.claim}")
        result = await verifier.verify_claim(claim_request.claim)
        return result
    except Exception as e:
        import traceback
        logger.error(f"Verification failed: {str(e)}\n{traceback.format_exc()}")
        return {
            "claim": claim_request.claim,
            "confidence": 0,
            "reason": "Verification system error",
            "verification": None,
            "error": f"Failed to verify claim: {str(e)}",
        }


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
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Resource not found"})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")
    return JSONResponse(
        status_code=500, 
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG
    )
