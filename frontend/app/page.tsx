'use client';

import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<{
    trade_analysis: string;
    risk_analysis: string;
    final_decision: string;
  } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:8000/analyze-trade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ trade_details: query }),
      });
      
      if (!response.ok) throw new Error('Failed to analyze trade');
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Trade Analysis Platform
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Get expert insights on your trading decisions
          </p>
        </header>
        
        {/* Input Section */}
        <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="query" className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-200">
                Describe your trade
              </label>
              <textarea
                id="query"
                rows={4}
                className="w-full px-4 py-3 text-gray-700 dark:text-gray-200 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                placeholder="For example: Buy 100 shares of AAPL at $200, stop-loss $190, target $220"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              ></textarea>
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className={`px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition duration-200 flex items-center ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : (
                'Analyze Trade'
              )}
            </button>
          </form>
        </section>
        
        {/* Error Message */}
        {error && (
          <div className="mb-8 p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300">
            <p className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zm-1 9a1 1 0 01-1-1v-4a1 1 0 112 0v4a1 1 0 01-1 1z" clipRule="evenodd"></path>
              </svg>
              {error}
            </p>
          </div>
        )}
        
        {/* Results Section */}
        {result && (
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
            {/* Trading Analysis */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-100 dark:border-gray-700 transition duration-200 hover:shadow-xl">
              <div className="bg-blue-500 p-4">
                <h3 className="text-xl font-semibold text-white">Trading Analysis</h3>
              </div>
              <div className="p-6">
                <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line">{result.trade_analysis}</p>
              </div>
            </div>
            
            {/* Risk Analysis */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-100 dark:border-gray-700 transition duration-200 hover:shadow-xl">
              <div className="bg-amber-500 p-4">
                <h3 className="text-xl font-semibold text-white">Risk Analysis</h3>
              </div>
              <div className="p-6">
                <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line">{result.risk_analysis}</p>
              </div>
            </div>
            
            {/* Final Decision */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-100 dark:border-gray-700 transition duration-200 hover:shadow-xl">
              <div className="bg-green-500 p-4">
                <h3 className="text-xl font-semibold text-white">Final Decision</h3>
              </div>
              <div className="p-6">
                <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line">{result.final_decision}</p>
              </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}