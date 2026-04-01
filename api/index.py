"""
FastAPI app entrypoint for Vercel deployment.
This file exports the FastAPI app instance for Vercel to discover.
"""
from backend.main import app

__all__ = ["app"]
