# 🌟 FinoSpark MVP

**AI-Powered Transaction Analysis with Emotional & Financial Insights**

FinoSpark is a minimal but complete MVP that analyzes your financial transactions using AI to provide:
- 😊 Emotional tone detection (calm, stressed, anxious, excited, neutral)
- 💰 Financial profile classification (spender, saver, balanced, investor)
- 🔍 Actionable insights and recommendations
- 📋 Personalized 30-day savings plans

## 🏗️ Architecture

- **Backend**: FastAPI (Python) + OpenRouter API integration
- **Frontend**: Next.js (React) with minimal styling
- **AI Model**: Meta Llama 3.2 3B Instruct (free tier via OpenRouter)

## 📁 Project Structure

```
Test-Beta/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app with /analyze endpoint
│   │   ├── schemas.py           # Pydantic models for validation
│   │   └── openrouter_client.py # OpenRouter API client
│   ├── requirements.txt         # Python dependencies
│   ├── .env.template           # Environment variable template
│   ├── .gitignore
│   └── README.md
├── frontend/
│   ├── pages/
│   │   ├── _app.js
│   │   └── index.js            # Main UI page
│   ├── lib/
│   │   └── api.js              # API client functions
│   ├── styles/
│   │   └── globals.css
│   ├── package.json
│   ├── next.config.js
│   ├── .env.template
│   ├── .gitignore
│   └── README.md
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenRouter API key (get one at https://openrouter.ai/keys)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.template .env
   # Edit .env and add your OpenRouter API key
   ```

5. **Run the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory (in a new terminal):**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.template .env.local
   # Edit if backend is not at localhost:8000
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## 🧪 Testing the API

### Using curl:

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
      },
      {
        "date": "2025-10-21",
        "amount": 3000.00,
        "currency": "INR",
        "merchant": "Electronics Store",
        "category": "Shopping",
        "note": "New headphones"
      },
      {
        "date": "2025-10-22",
        "amount": 500.00,
        "currency": "INR",
        "merchant": "Coffee Shop",
        "category": "Food",
        "note": ""
      }
    ],
    "notes": "Trying to save money but had some unexpected expenses"
  }'
```

### Expected Response:

```json
{
  "emotion": "anxious",
  "financial_profile": "balanced",
  "confidence": 0.85,
  "top_insights": [
    "Recent spike in discretionary spending",
    "Regular food expenses are consistent",
    "Emotional spending pattern detected"
  ],
  "recommendations": [
    {
      "title": "Set a Monthly Budget",
      "desc": "Establish clear spending limits for each category",
      "priority": 1
    },
    {
      "title": "Track Impulse Purchases",
      "desc": "Wait 24 hours before non-essential purchases",
      "priority": 2
    },
    {
      "title": "Build Emergency Fund",
      "desc": "Save 10% of income monthly for unexpected expenses",
      "priority": 3
    }
  ],
  "savings_plan": {
    "target_amount": 5000.0,
    "period_days": 30,
    "steps": [
      "Reduce dining out to 2x per week",
      "Cancel unused subscriptions",
      "Use public transport 3 days per week"
    ]
  }
}
```

## 📊 API Endpoints

### `POST /analyze`

Analyzes transaction data and returns insights.

**Request Body:**
```json
{
  "user_id": "string",
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "amount": 123.45,
      "currency": "INR",
      "merchant": "Merchant Name",
      "category": "Category",
      "note": "Optional note"
    }
  ],
  "notes": "Optional additional context"
}
```

**Response:**
- `200 OK`: Returns analysis result (or error object if analysis fails)
- `400 Bad Request`: Invalid input data
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "openrouter_configured": true,
  "timestamp": 1234567890.0
}
```

## 🔐 Security Features

- ✅ Environment variable for API keys (no hardcoded secrets)
- ✅ CORS middleware configured
- ✅ Rate limiting (10 requests per 60 seconds per user)
- ✅ Input validation using Pydantic models
- ✅ Error handling with detailed logging

## ⚙️ Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENROUTER_API_KEY=sk-or-v1-YOUR-API-KEY-HERE
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🛠️ Development

### Backend

- **Run with auto-reload:**
  ```bash
  uvicorn app.main:app --reload
  ```

- **View API documentation:**
  Visit `http://localhost:8000/docs` for interactive Swagger UI

- **Run linting:**
  ```bash
  pip install flake8
  flake8 app/
  ```

### Frontend

- **Development mode:**
  ```bash
  npm run dev
  ```

- **Build for production:**
  ```bash
  npm run build
  npm start
  ```

- **Linting:**
  ```bash
  npm run lint
  ```

## 📝 Model Information

**Model Used:** `meta-llama/llama-3.2-3b-instruct:free`

**Why this model?**
- Free tier on OpenRouter
- Good balance of speed and quality
- Excellent at following structured output instructions
- Low temperature (0.2) for deterministic responses

## 🚨 Known Limitations

1. **Rate Limiting**: In-memory rate limiting resets on server restart. Use Redis for production.
2. **Model Availability**: Free tier models may have usage limits or availability constraints.
3. **JSON Extraction**: If model doesn't return pure JSON, extraction is attempted but may fail.
4. **No Authentication**: No user authentication implemented. Add JWT/OAuth for production.
5. **No Database**: No persistent storage. Transactions are analyzed in real-time only.

## 🔄 Future Enhancements

- [ ] User authentication and session management
- [ ] Transaction history storage (PostgreSQL/MongoDB)
- [ ] Real-time dashboard with charts
- [ ] Email/SMS notifications for insights
- [ ] Multi-currency support
- [ ] CSV/Excel file upload
- [ ] Scheduled analysis reports
- [ ] Mobile app (React Native)

## 📄 License

MIT License - Feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

This is an MVP project. Feel free to fork and enhance!

## 📞 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the health endpoint at `/health`
3. Check browser console for frontend errors
4. Verify environment variables are set correctly

## 🎯 Project Goals

This MVP demonstrates:
- ✅ FastAPI backend with async operations
- ✅ OpenRouter API integration
- ✅ Pydantic validation and schemas
- ✅ Next.js frontend with API integration
- ✅ AI-powered financial analysis
- ✅ Emotional intelligence detection
- ✅ Clean, maintainable code structure

---

**Built with ❤️ for financial wellness**
