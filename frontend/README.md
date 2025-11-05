# FinoSpark Frontend

Next.js frontend for FinoSpark MVP - Simple UI for transaction analysis.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment (optional):**
   ```bash
   cp .env.template .env.local
   # Edit if backend is not at localhost:8000
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   Visit `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── pages/
│   ├── _app.js          # App wrapper
│   └── index.js         # Main page with form and results
├── lib/
│   └── api.js           # API client functions
├── styles/
│   └── globals.css      # Global styles
├── package.json
├── next.config.js
└── README.md
```

## 🎨 Features

- **Simple Form UI**: Paste JSON transactions and notes
- **Real-time Analysis**: Calls backend API and shows results
- **Pretty Results Display**: Formatted insights, recommendations, and savings plan
- **Error Handling**: Graceful error display with debug info
- **Minimal Styling**: Clean, functional design without heavy dependencies

## 📋 Usage

1. **Enter User ID**: Any string identifier
2. **Paste Transaction JSON**: Format as array of transaction objects
3. **Add Notes (optional)**: Additional context for analysis
4. **Click Analyze**: Sends request to backend
5. **View Results**: Insights displayed in formatted cards

### Transaction JSON Format

```json
[
  {
    "date": "2025-10-20",
    "amount": 1500.00,
    "currency": "INR",
    "merchant": "Grocery Store",
    "category": "Food",
    "note": "Weekly groceries"
  }
]
```

## 🔧 Configuration

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Default: `http://localhost:8000`

## 🛠️ Development

### Available Scripts

- **`npm run dev`**: Start development server (port 3000)
- **`npm run build`**: Build for production
- **`npm start`**: Run production build
- **`npm run lint`**: Run ESLint

### Making Changes

1. **Update UI**: Edit `pages/index.js`
2. **Add API calls**: Update `lib/api.js`
3. **Modify styles**: Edit inline styles or `styles/globals.css`

## 📦 Dependencies

### Core
- **next**: React framework
- **react**: UI library
- **react-dom**: React DOM renderer

### Dev
- **eslint**: Code linting
- **eslint-config-next**: Next.js ESLint config

## 🎯 Key Components

### Main Page (`pages/index.js`)

- Form for user input
- API call handling
- Result rendering
- Error display

### API Client (`lib/api.js`)

- `analyzeTransactions()`: POST to /analyze
- `checkHealth()`: GET health status

## 🐛 Troubleshooting

### Backend Connection Error

**Problem**: Cannot connect to backend

**Solution**:
1. Ensure backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Verify CORS is enabled in backend

### JSON Parse Error

**Problem**: Invalid JSON in transactions field

**Solution**:
- Ensure valid JSON array format
- Use the provided example as template
- Check for trailing commas

### No Results Displayed

**Problem**: Analysis runs but shows no results

**Solution**:
1. Check browser console for errors
2. Verify backend returned valid response
3. Check API key is configured in backend

## 🚀 Production Build

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Start production server:**
   ```bash
   npm start
   ```

3. **Deploy:**
   - Vercel: `vercel deploy`
   - Netlify: Connect repo
   - Docker: Use multi-stage build

## 📱 Responsive Design

The UI is mobile-friendly with:
- Flexible layouts
- Responsive text areas
- Touch-friendly buttons
- Readable on small screens

## 🎨 Customization

### Styling

Styles are inline in `pages/index.js` for simplicity.

To customize:
1. Edit `styles` object in `index.js`
2. Add Tailwind CSS for utility classes
3. Use CSS modules for component-specific styles

### Color Scheme

Current colors:
- Primary: `#0070f3` (blue)
- Background: `#f5f5f5` (light gray)
- Error: `#d00` (red)
- Success: `#0a0` (green)

## 🔐 Security

- API key stored in backend (not exposed to frontend)
- Environment variables for configuration
- No sensitive data in client-side code

## 📄 License

MIT License

---

**Happy analyzing! 📊✨**
