import { useState } from 'react';
import Head from 'next/head';
import { analyzeTransactions } from '../lib/api';

export default function Home() {
  const [userId, setUserId] = useState('user123');
  const [transactionsJson, setTransactionsJson] = useState(
`[
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
]`
  );
  const [notes, setNotes] = useState('Trying to save money but had some unexpected expenses');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Parse transactions JSON
      const transactions = JSON.parse(transactionsJson);
      
      // Call backend API
      const response = await analyzeTransactions({
        user_id: userId,
        transactions,
        notes
      });

      setResult(response);
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const renderResult = () => {
    if (!result) return null;

    // Check if it's an error response
    if (result.error) {
      return (
        <div style={styles.errorBox}>
          <h3>❌ Error</h3>
          <p><strong>Error:</strong> {result.error}</p>
          {result.details && <p><strong>Details:</strong> {result.details}</p>}
          {result.raw_response && (
            <details>
              <summary>Raw Response</summary>
              <pre style={styles.pre}>{result.raw_response}</pre>
            </details>
          )}
        </div>
      );
    }

    // Render successful analysis
    return (
      <div style={styles.resultBox}>
        <h3>✅ Analysis Complete</h3>
        
        <div style={styles.section}>
          <h4>😊 Emotional State: <span style={styles.badge}>{result.emotion}</span></h4>
          <h4>💰 Financial Profile: <span style={styles.badge}>{result.financial_profile}</span></h4>
          <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%</p>
        </div>

        <div style={styles.section}>
          <h4>🔍 Top Insights</h4>
          <ul>
            {result.top_insights?.map((insight, idx) => (
              <li key={idx}>{insight}</li>
            ))}
          </ul>
        </div>

        <div style={styles.section}>
          <h4>📋 Recommendations</h4>
          {result.recommendations?.map((rec, idx) => (
            <div key={idx} style={styles.recommendation}>
              <strong>#{rec.priority}: {rec.title}</strong>
              <p>{rec.desc}</p>
            </div>
          ))}
        </div>

        <div style={styles.section}>
          <h4>💸 30-Day Savings Plan</h4>
          <p><strong>Target Amount:</strong> ₹{result.savings_plan?.target_amount}</p>
          <p><strong>Period:</strong> {result.savings_plan?.period_days} days</p>
          <h5>Steps:</h5>
          <ol>
            {result.savings_plan?.steps?.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ol>
        </div>

        <details style={{ marginTop: '20px' }}>
          <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
            View Raw JSON
          </summary>
          <pre style={styles.pre}>{JSON.stringify(result, null, 2)}</pre>
        </details>
      </div>
    );
  };

  return (
    <>
      <Head>
        <title>FinoSpark MVP - Transaction Analysis</title>
        <meta name="description" content="AI-powered transaction analysis with emotional and financial insights" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div style={styles.container}>
        <header style={styles.header}>
          <h1>✨ FinoSpark MVP</h1>
          <p>AI-Powered Transaction Analysis with Emotional & Financial Insights</p>
        </header>

        <main style={styles.main}>
          <form onSubmit={handleSubmit} style={styles.form}>
            <div style={styles.formGroup}>
              <label htmlFor="userId" style={styles.label}>User ID</label>
              <input
                type="text"
                id="userId"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                style={styles.input}
                required
              />
            </div>

            <div style={styles.formGroup}>
              <label htmlFor="transactions" style={styles.label}>
                Transactions (JSON Array)
              </label>
              <textarea
                id="transactions"
                value={transactionsJson}
                onChange={(e) => setTransactionsJson(e.target.value)}
                style={styles.textarea}
                rows={15}
                required
                placeholder='[{"date": "2025-10-20", "amount": 1500.00, ...}]'
              />
            </div>

            <div style={styles.formGroup}>
              <label htmlFor="notes" style={styles.label}>
                Additional Notes (Optional)
              </label>
              <textarea
                id="notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                style={styles.textarea}
                rows={3}
                placeholder="Any additional context about your spending..."
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              style={{
                ...styles.button,
                ...(loading ? styles.buttonDisabled : {})
              }}
            >
              {loading ? '⏳ Analyzing...' : '🚀 Analyze Transactions'}
            </button>
          </form>

          {error && (
            <div style={styles.errorBox}>
              <strong>Error:</strong> {error}
            </div>
          )}

          {renderResult()}
        </main>

        <footer style={styles.footer}>
          <p>FinoSpark MVP v1.0.0 | Powered by OpenRouter AI</p>
        </footer>
      </div>
    </>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    padding: '20px',
    backgroundColor: '#f5f5f5',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
    color: '#333',
  },
  main: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  form: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    marginBottom: '30px',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: 'bold',
    color: '#333',
  },
  input: {
    width: '100%',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '14px',
    fontFamily: 'inherit',
  },
  textarea: {
    width: '100%',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '14px',
    fontFamily: 'monospace',
    resize: 'vertical',
  },
  button: {
    width: '100%',
    padding: '15px',
    backgroundColor: '#0070f3',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
    cursor: 'not-allowed',
  },
  resultBox: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  errorBox: {
    backgroundColor: '#fff3f3',
    border: '1px solid #ffcccc',
    padding: '20px',
    borderRadius: '8px',
    color: '#d00',
    marginTop: '20px',
  },
  section: {
    marginBottom: '25px',
    paddingBottom: '20px',
    borderBottom: '1px solid #eee',
  },
  badge: {
    backgroundColor: '#0070f3',
    color: 'white',
    padding: '4px 12px',
    borderRadius: '12px',
    fontSize: '14px',
  },
  recommendation: {
    backgroundColor: '#f9f9f9',
    padding: '15px',
    borderRadius: '4px',
    marginBottom: '10px',
  },
  pre: {
    backgroundColor: '#f4f4f4',
    padding: '15px',
    borderRadius: '4px',
    overflow: 'auto',
    fontSize: '12px',
  },
  footer: {
    textAlign: 'center',
    marginTop: '40px',
    color: '#666',
    fontSize: '14px',
  },
};
