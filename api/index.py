"""
FastAPI app entrypoint for Vercel deployment.
This file exports the FastAPI app instance for Vercel to discover.
"""
import sys
import os
import traceback

# Add the parent directory to the path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Create base app
app = FastAPI(title="FinVerify AI")

# Try to import and setup the main app
try:
    from backend.main import app as main_app
    # Use the main app if import successful
    app = main_app
except ImportError as e:
    # Log the error but keep a working app
    error_msg = f"Failed to import backend.main: {str(e)}\n{traceback.format_exc()}"
    
    @app.get("/")
    async def root():
        return {"status": "error", "message": "Failed to load main app", "error": error_msg}
    
    @app.get("/health")
    async def health():
        return {"status": "error", "message": "App initialization failed", "error": error_msg}
        
except Exception as e:
    # Handle any other exceptions during import
    error_msg = f"Unexpected error loading app: {str(e)}\n{traceback.format_exc()}"
    
    @app.get("/")
    async def root():
        return {"status": "error", "message": "App initialization failed", "error": error_msg}
    
    @app.get("/health")
    async def health():
        return {"status": "error", "message": "App initialization failed", "error": error_msg}

__all__ = ["app"]
