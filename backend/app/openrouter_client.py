"""
OpenRouter API client for LLM analysis
"""
import os
import json
import re
import httpx
from typing import Dict, Any, Optional
from app.schemas import AnalyzeRequest, AnalysisResponse, ErrorResponse


class OpenRouterClient:
    """Client for interacting with OpenRouter API or Google Gemini API"""
    
    def __init__(self):
        # Try Google Gemini API first (more reliable)
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        if self.google_api_key:
            # Use Google Gemini directly (flash model for better availability)
            self.use_google = True
            self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.google_api_key}"
            self.model_id = "gemini-2.5-flash"
        elif self.openrouter_api_key:
            # Fallback to OpenRouter
            self.use_google = False
            self.base_url = "https://openrouter.ai/api/v1/chat/completions"
            self.model_id = "google/gemini-2.0-flash-exp:free"
        else:
            raise ValueError("Neither GOOGLE_API_KEY nor OPENROUTER_API_KEY environment variable is set")
        
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the LLM"""
        return """You are FinoSpark AI, an expert financial and emotional intelligence analyst. 
Your task is to analyze transaction data and provide insights in a specific JSON format.

IMPORTANT: You must ALWAYS respond with ONLY valid JSON, no other text before or after.

Your analysis should include:
1. Emotional tone detection (choose ONE: calm, stressed, anxious, excited, neutral)
2. Financial profile classification (choose ONE: spender, saver, balanced, investor)
3. Confidence score (0.0 to 1.0)
4. Top insights (2-4 key observations)
5. Three prioritized recommendations
6. A 30-day savings micro-plan

The JSON must follow this exact structure:
{
  "emotion": "calm|stressed|anxious|excited|neutral",
  "financial_profile": "spender|saver|balanced|investor",
  "confidence": 0.85,
  "top_insights": ["insight 1", "insight 2", "insight 3"],
  "recommendations": [
    {"title": "Recommendation Title", "desc": "Brief description", "priority": 1},
    {"title": "Second Recommendation", "desc": "Brief description", "priority": 2},
    {"title": "Third Recommendation", "desc": "Brief description", "priority": 3}
  ],
  "savings_plan": {
    "target_amount": 5000.0,
    "period_days": 30,
    "steps": ["Step 1", "Step 2", "Step 3"]
  }
}

Respond ONLY with valid JSON. No markdown, no explanations, just the JSON object."""

    def _build_user_prompt(self, request: AnalyzeRequest) -> str:
        """Build user prompt from transaction data"""
        transactions_text = "\n".join([
            f"- {t.date}: {t.currency} {t.amount:.2f} at {t.merchant or 'Unknown'} "
            f"({t.category or 'Uncategorized'}){' - ' + t.note if t.note else ''}"
            for t in request.transactions
        ])
        
        total_amount = sum(t.amount for t in request.transactions)
        avg_amount = total_amount / len(request.transactions) if request.transactions else 0
        
        user_prompt = f"""Analyze these financial transactions for user {request.user_id}:

TRANSACTIONS ({len(request.transactions)} total):
{transactions_text}

SUMMARY:
- Total spent: {request.transactions[0].currency if request.transactions else 'INR'} {total_amount:.2f}
- Average transaction: {request.transactions[0].currency if request.transactions else 'INR'} {avg_amount:.2f}

ADDITIONAL NOTES:
{request.notes or 'None provided'}

Provide your analysis in the required JSON format."""
        
        return user_prompt

    def _extract_json_from_response(self, text: str) -> Optional[Dict[str, Any]]:
        """Try to extract JSON from response text, including markdown and truncated cases. Returns partial JSON if possible."""
        # Remove markdown code block markers if present
        if text.strip().startswith('```'):
            text = re.sub(r'^```[a-zA-Z]*\s*', '', text.strip())
            text = re.sub(r'```$', '', text.strip())

        # Try to parse directly first
        try:
            return json.loads(text)
        except Exception:
            pass

        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except Exception:
                pass

        # Try to find the largest JSON object in the text
        json_match = re.search(r'(\{[\s\S]*\})', text)
        if json_match:
            json_str = json_match.group(1)
            # Try to fix truncated JSON by removing trailing incomplete structures
            # Find last closing curly brace
            last_brace = json_str.rfind('}')
            if last_brace != -1:
                json_str = json_str[:last_brace+1]
            # Remove trailing commas before closing braces (common truncation issue)
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
            try:
                return json.loads(json_str)
            except Exception:
                # Try to recover partial JSON by iteratively removing last key-value pairs
                while True:
                    # Remove last key-value pair
                    json_str = re.sub(r',\s*"[^"]*"\s*:\s*[^,{}\[\]]*([}\]])', r'\1', json_str)
                    try:
                        return json.loads(json_str)
                    except Exception:
                        # If nothing left to parse, break
                        if json_str.count(':') == 0:
                            break
                pass

        # If still not valid, try to recover by adding missing closing braces
        if 'json_str' in locals():
            open_braces = json_str.count('{')
            close_braces = json_str.count('}')
            if open_braces > close_braces:
                json_str += '}' * (open_braces - close_braces)
                try:
                    return json.loads(json_str)
                except Exception:
                    pass

        return None

    async def analyze_transactions(self, request: AnalyzeRequest) -> Dict[str, Any]:
        """
        Call OpenRouter API or Google Gemini API to analyze transactions
        Returns either AnalysisResponse or ErrorResponse
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request)
        
        if self.use_google:
            return await self._call_google_api(system_prompt, user_prompt)
        else:
            return await self._call_openrouter_api(system_prompt, user_prompt)
    
    async def _call_google_api(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Call Google Gemini API directly"""
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\n{user_prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    json=payload
                )
                response.raise_for_status()
                
                response_data = response.json()
                
                # Extract content from Google's response format
                if "candidates" in response_data and len(response_data["candidates"]) > 0:
                    content = response_data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Try to extract JSON from the response
                    json_data = self._extract_json_from_response(content)
                    
                    if json_data:
                        # Validate against our schema
                        try:
                            validated = AnalysisResponse(**json_data)
                            return validated.dict()
                        except Exception as validation_error:
                            return ErrorResponse(
                                error="Validation failed",
                                details=str(validation_error),
                                raw_response=content
                            ).dict()
                    else:
                        return ErrorResponse(
                            error="Failed to extract JSON from model response",
                            details="The model did not return valid JSON",
                            raw_response=content
                        ).dict()
                else:
                    return ErrorResponse(
                        error="Unexpected API response structure",
                        details="No candidates in response",
                        raw_response=str(response_data)
                    ).dict()
                    
        except httpx.HTTPStatusError as e:
            return ErrorResponse(
                error=f"API request failed with status {e.response.status_code}",
                details=str(e),
                raw_response=e.response.text
            ).dict()
        except Exception as e:
            return ErrorResponse(
                error="Unexpected error during API call",
                details=str(e)
            ).dict()
    
    async def _call_openrouter_api(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Call OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://finospark.app",
            "X-Title": "FinoSpark MVP"
        }
        
        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1500
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                response_data = response.json()
                
                # Extract the assistant's message
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    content = response_data["choices"][0]["message"]["content"]
                    
                    # Try to extract JSON from the response
                    json_data = self._extract_json_from_response(content)
                    
                    if json_data:
                        # Validate against our schema
                        try:
                            validated = AnalysisResponse(**json_data)
                            return validated.dict()
                        except Exception as validation_error:
                            return ErrorResponse(
                                error="Validation failed",
                                details=str(validation_error),
                                raw_response=content
                            ).dict()
                    else:
                        return ErrorResponse(
                            error="Failed to extract JSON from model response",
                            details="The model did not return valid JSON",
                            raw_response=content
                        ).dict()
                else:
                    return ErrorResponse(
                        error="Unexpected API response structure",
                        details="No choices in response",
                        raw_response=str(response_data)
                    ).dict()
                    
        except httpx.HTTPStatusError as e:
            return ErrorResponse(
                error=f"API request failed with status {e.response.status_code}",
                details=str(e),
                raw_response=e.response.text
            ).dict()
        except Exception as e:
            return ErrorResponse(
                error="Unexpected error during API call",
                details=str(e)
            ).dict()
