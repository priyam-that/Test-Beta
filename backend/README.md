# FinoSpark Backend

FastAPI backend for FinoSpark MVP - AI-powered transaction analysis.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.template .env
   # Edit .env and add your OPENROUTER_API_KEY
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📡 API Endpoints

### POST /analyze

Analyzes transaction data and returns insights.

**Example Request:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "transactions": [
      {
        "date": "2025-10-20",
        "amount": 1500.00,
        "currency": "INR",
        "merchant": "Grocery Store",
        "category": "Food",
        "note": "Weekly groceries"
      }
    ],
    "notes": "Optional context"
  }'
```

### GET /health

Health check endpoint.

```bash
curl http://localhost:8000/health
```

### GET /docs

Interactive API documentation (Swagger UI).

Visit: `http://localhost:8000/docs`

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic models
│   └── openrouter_client.py # OpenRouter API client
├── requirements.txt
├── .env.template
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=sk-or-v1-YOUR-API-KEY-HERE
```

Get your API key from: https://openrouter.ai/keys

### Rate Limiting

Default settings:
- 10 requests per user per 60 seconds
- In-memory storage (resets on restart)

For production, implement Redis-based rate limiting.

## 📦 Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **httpx**: Async HTTP client for OpenRouter API
- **pydantic**: Data validation
- **python-dotenv**: Environment variable management

## 🧪 Testing

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

### Test Analysis Endpoint

Use the example curl command above or visit the Swagger UI at `/docs`.

## 🔐 Security Notes

- Never commit `.env` file
- Use environment variables for all secrets
- CORS is configured for development (adjust for production)
- Rate limiting prevents abuse
- Input validation via Pydantic

## 🐛 Debugging

1. **Check if server is running:**
   ```bash
   curl http://localhost:8000/
   ```

2. **Verify API key is set:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **View logs:**
   Server logs appear in the terminal where uvicorn is running.

## 📝 Response Schema

Successful analysis returns:

```json
{
  "emotion": "calm|stressed|anxious|excited|neutral",
  "financial_profile": "spender|saver|balanced|investor",
  "confidence": 0.85,
  "top_insights": ["insight 1", "insight 2"],
  "recommendations": [
    {"title": "...", "desc": "...", "priority": 1}
  ],
  "savings_plan": {
    "target_amount": 5000.0,
    "period_days": 30,
    "steps": ["step 1", "step 2"]
  }
}
```

Error response:

```json
{
  "error": "Error message",
  "details": "Detailed explanation",
  "raw_response": "Raw API response"
}
```

## 🚀 Production Deployment

1. **Use production ASGI server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Set up proper CORS:**
   Update `allow_origins` in `main.py` with your frontend domain.

3. **Add Redis for rate limiting:**
   Replace in-memory rate limiting with Redis.

4. **Set up monitoring:**
   Add logging, error tracking (Sentry), and metrics.

5. **Use HTTPS:**
   Deploy behind a reverse proxy (nginx) with SSL.

## 📄 License

MIT License
