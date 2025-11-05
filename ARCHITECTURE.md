# 🏗️ FinoSpark Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    http://localhost:3000                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP POST /analyze
                             │ (JSON: user_id, transactions, notes)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NEXT.JS FRONTEND                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  pages/index.js                                           │  │
│  │  - Form UI (user_id, transactions JSON, notes)           │  │
│  │  - Submit handler                                         │  │
│  │  - Result display                                         │  │
│  │  - Error handling                                         │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │  lib/api.js                                               │  │
│  │  - analyzeTransactions(data)                              │  │
│  │  - fetch() wrapper                                        │  │
│  └──────────────────┬───────────────────────────────────────┘  │
└─────────────────────┼────────────────────────────────────────────┘
                      │
                      │ HTTP POST
                      │ http://localhost:8000/analyze
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│                  http://localhost:8000                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app/main.py                                              │  │
│  │  POST /analyze endpoint                                   │  │
│  │  1. Validate request (Pydantic)                           │  │
│  │  2. Check rate limit                                      │  │
│  │  3. Call OpenRouter client                                │  │
│  │  4. Return analysis result                                │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │  app/schemas.py                                           │  │
│  │  - AnalyzeRequest (validation)                            │  │
│  │  - AnalysisResponse (output)                              │  │
│  │  - Transaction, Recommendation, etc.                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app/openrouter_client.py                                 │  │
│  │  1. Build system prompt (instructions)                    │  │
│  │  2. Build user prompt (transaction data)                  │  │
│  │  3. Call OpenRouter API                                   │  │
│  │  4. Extract JSON from response                            │  │
│  │  5. Validate against schema                               │  │
│  └──────────────────┬───────────────────────────────────────┘  │
└─────────────────────┼────────────────────────────────────────────┘
                      │
                      │ HTTPS POST
                      │ https://openrouter.ai/api/v1/chat/completions
                      │ Authorization: Bearer OPENROUTER_API_KEY
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OPENROUTER API                              │
│                  https://openrouter.ai                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Model: meta-llama/llama-3.2-3b-instruct:free            │  │
│  │  Temperature: 0.2 (deterministic)                         │  │
│  │  Max Tokens: 1500                                         │  │
│  │                                                            │  │
│  │  Input:                                                    │  │
│  │  - System prompt (analysis instructions)                  │  │
│  │  - User prompt (transaction data)                         │  │
│  │                                                            │  │
│  │  Output:                                                   │  │
│  │  - JSON with emotion, profile, insights, etc.            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Input (Frontend)
```javascript
{
  user_id: "user123",
  transactions: [
    {date: "2025-10-20", amount: 1500, merchant: "Store", ...}
  ],
  notes: "Trying to save money"
}
```

### 2. API Request (Frontend → Backend)
```http
POST http://localhost:8000/analyze
Content-Type: application/json

{
  "user_id": "user123",
  "transactions": [...],
  "notes": "..."
}
```

### 3. Validation & Processing (Backend)
```python
# 1. Pydantic validates request
request = AnalyzeRequest(**data)

# 2. Check rate limit
if not check_rate_limit(request.user_id):
    raise HTTPException(429)

# 3. Call OpenRouter
result = await openrouter_client.analyze_transactions(request)
```

### 4. OpenRouter API Call (Backend → OpenRouter)
```python
# Build prompts
system_prompt = """You are FinoSpark AI..."""
user_prompt = """Analyze these transactions:
- 2025-10-20: INR 1500 at Store
...
"""

# Call API
response = await httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }
)
```

### 5. AI Response (OpenRouter → Backend)
```json
{
  "choices": [{
    "message": {
      "content": "{\"emotion\":\"anxious\",\"financial_profile\":\"balanced\",...}"
    }
  }]
}
```

### 6. JSON Extraction & Validation (Backend)
```python
# Extract JSON from response
json_data = extract_json(content)

# Validate against schema
validated = AnalysisResponse(**json_data)

# Return to frontend
return validated.dict()
```

### 7. Display Results (Frontend)
```javascript
setResult(response);
// Display:
// - Emotion badge
// - Financial profile
// - Insights list
// - Recommendations cards
// - Savings plan steps
```

## Component Interaction

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Browser   │────▶│  Next.js UI  │────▶│  API Client │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                  │
                                                  │ HTTP
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ OpenRouter  │◀────│  API Client  │◀────│   FastAPI   │
│     AI      │     │   (httpx)    │     │  Endpoint   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                  │
                                                  ▼
                                          ┌─────────────┐
                                          │  Pydantic   │
                                          │ Validation  │
                                          └─────────────┘
```

## Error Handling Flow

```
User Input
    │
    ▼
Frontend Validation
    │
    ├─ Invalid JSON? → Show error message
    │
    ▼
API Call (try-catch)
    │
    ├─ Network error? → Show connection error
    │
    ▼
Backend Validation
    │
    ├─ Invalid data? → 400 Bad Request
    ├─ Rate limit? → 429 Too Many Requests
    │
    ▼
OpenRouter API Call
    │
    ├─ HTTP error? → Return ErrorResponse
    ├─ Invalid JSON? → Return ErrorResponse with raw data
    │
    ▼
Success Response
    │
    ▼
Display Results
```

## Security Layers

```
1. Environment Variables
   └─ API keys never in code

2. CORS Middleware
   └─ Only allowed origins

3. Rate Limiting
   └─ 10 requests / 60s per user

4. Input Validation
   └─ Pydantic strict validation

5. Error Sanitization
   └─ No sensitive data in errors
```

## Deployment Architecture (Production)

```
┌─────────────┐
│   Vercel    │  (Frontend)
│  Next.js    │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────┐
│   Railway   │  (Backend)
│   FastAPI   │
│   + Redis   │  (Rate limiting)
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────┐
│ OpenRouter  │
│     API     │
└─────────────┘
```

## File Responsibilities

### Backend
- **main.py**: Route handling, middleware, rate limiting
- **schemas.py**: Data models and validation
- **openrouter_client.py**: AI API integration and prompt engineering

### Frontend
- **index.js**: UI components and state management
- **api.js**: HTTP client and error handling
- **globals.css**: Minimal global styles

---

**This architecture ensures:**
- ✅ Clean separation of concerns
- ✅ Type safety (Pydantic)
- ✅ Error resilience
- ✅ Scalable structure
- ✅ Easy to test and debug
