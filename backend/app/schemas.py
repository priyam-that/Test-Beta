"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class Transaction(BaseModel):
    """Single transaction entry"""
    date: str = Field(..., description="Transaction date in YYYY-MM-DD format")
    amount: float = Field(..., description="Transaction amount")
    currency: str = Field(default="INR", description="Currency code")
    merchant: str = Field(default="", description="Merchant/vendor name")
    category: str = Field(default="", description="Transaction category")
    note: str = Field(default="", description="Optional note about transaction")


class AnalyzeRequest(BaseModel):
    """Request body for /analyze endpoint"""
    user_id: str = Field(..., description="Unique user identifier")
    transactions: List[Transaction] = Field(..., description="List of transactions to analyze")
    notes: Optional[str] = Field(default="", description="Optional additional context or notes")


class Recommendation(BaseModel):
    """Single recommendation item"""
    title: str
    desc: str
    priority: int


class SavingsPlan(BaseModel):
    """30-day savings micro-plan"""
    target_amount: float
    period_days: int = 30
    steps: List[str]


class AnalysisResponse(BaseModel):
    """Response from the analysis endpoint"""
    emotion: str = Field(..., description="Detected emotional tone: calm, stressed, anxious, excited, neutral")
    financial_profile: str = Field(..., description="Financial profile: spender, saver, balanced, investor")
    confidence: float = Field(..., description="Confidence score 0.0-1.0")
    top_insights: List[str] = Field(..., description="Key insights from transaction analysis")
    recommendations: List[Recommendation] = Field(..., description="Prioritized recommendations")
    savings_plan: SavingsPlan = Field(..., description="30-day savings plan")


class ErrorResponse(BaseModel):
    """Error response with debug details"""
    error: str
    details: Optional[str] = None
    raw_response: Optional[str] = None
