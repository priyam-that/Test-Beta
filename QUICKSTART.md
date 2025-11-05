# 🚀 Quick Start Guide

Get FinoSpark MVP running in 5 minutes!

## Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# The script will:
# - Create Python virtual environment
# - Install all dependencies
# - Create .env files
```

## Option 2: Manual Setup

### Backend (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# .env file already configured with API key
uvicorn app.main:app --reload
```

### Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

## 🎯 Access the App

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Quick Test

### Using the UI (Easy)

1. Go to http://localhost:3000
2. The form is pre-filled with example data
3. Click "🚀 Analyze Transactions"
4. View the results!

### Using curl (Advanced)

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
      }
    ],
    "notes": "Trying to save money"
  }'
```

## 🔑 API Key

The backend `.env` file is already configured with the provided API key:
```
OPENROUTER_API_KEY=sk-or-v1-5278c1d3672dec56a5309b181dd71f0ac
```

## 🐛 Troubleshooting

### Port Already in Use

**Backend (8000):**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000):**
```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9
```

### Module Not Found

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### API Connection Error

1. Ensure backend is running on port 8000
2. Check backend logs for errors
3. Verify `.env` file has API key
4. Test backend health: `curl http://localhost:8000/health`

## 📚 Next Steps

1. ✅ Run the app
2. ✅ Test with sample data
3. ✅ Try your own transactions
4. 📖 Read the full README.md for advanced features
5. 🛠️ Customize and extend!

## 💡 Tips

- **Backend logs**: Watch the terminal where uvicorn is running
- **Frontend logs**: Check browser console (F12)
- **API docs**: Interactive testing at http://localhost:8000/docs
- **Sample data**: Pre-filled in the frontend form

---

**Need help?** Check the main README.md or individual backend/frontend READMEs.
