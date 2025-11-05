"""
FinoSpark MVP - FastAPI Backend
Analyzes transaction data using OpenRouter API to provide emotional and financial insights
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from collections import defaultdict
import time
from typing import Dict
from dotenv import load_dotenv

from app.schemas import AnalyzeRequest, AnalysisResponse
from app.openrouter_client import OpenRouterClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="FinoSpark MVP",
    description="Emotional and financial insights from transaction data",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenRouter client
try:
    openrouter_client = OpenRouterClient()
except ValueError as e:
    print(f"WARNING: {e}")
    openrouter_client = None

# Simple in-memory rate limiting (placeholder for production rate limiter)
# In production, use Redis or similar for distributed rate limiting
rate_limit_store: Dict[str, list] = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 10  # max requests per window


def check_rate_limit(user_id: str) -> bool:
    """
    Simple in-memory rate limiting
    Returns True if request is allowed, False if rate limit exceeded
    """
    now = time.time()
    user_requests = rate_limit_store[user_id]
    
    # Remove old requests outside the window
    user_requests[:] = [req_time for req_time in user_requests if now - req_time < RATE_LIMIT_WINDOW]
    
    if len(user_requests) >= RATE_LIMIT_MAX_REQUESTS:
        return False
    
    user_requests.append(now)
    return True


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FinoSpark MVP",
        "version": "1.0.0"
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_transactions(request: AnalyzeRequest):
    """
    Analyze transaction data and return emotional + financial insights
    
    Args:
        request: AnalyzeRequest containing user_id, transactions, and optional notes
    
    Returns:
        AnalysisResponse with emotional tone, financial profile, insights, recommendations, and savings plan
    
    Example curl:
        curl -X POST http://localhost:8000/analyze \\
          -H "Content-Type: application/json" \\
          -d '{
            "user_id": "user123",
            "transactions": [
              {"date": "2025-10-20", "amount": 1500.00, "currency": "INR", "merchant": "Grocery Store", "category": "Food", "note": "Weekly groceries"},
              {"date": "2025-10-21", "amount": 3000.00, "currency": "INR", "merchant": "Electronics Store", "category": "Shopping", "note": "New headphones"},
              {"date": "2025-10-22", "amount": 500.00, "currency": "INR", "merchant": "Coffee Shop", "category": "Food", "note": ""}
            ],
            "notes": "Trying to save money but had some unexpected expenses"
          }'
    """
    # Check if OpenRouter client is initialized
    if not openrouter_client:
        raise HTTPException(
            status_code=500,
            detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable."
        )
    
    # Check rate limit
    if not check_rate_limit(request.user_id):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )
    
    # Validate that we have transactions
    if not request.transactions or len(request.transactions) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one transaction is required for analysis"
        )
    
    # Call OpenRouter API for analysis
    result = await openrouter_client.analyze_transactions(request)
    
    # Check if result is an error
    if "error" in result:
        # Return error response with 200 status but error structure
        # This allows frontend to handle gracefully
        return JSONResponse(
            status_code=200,
            content=result
        )
    
    return result


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "openrouter_configured": openrouter_client is not None,
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
