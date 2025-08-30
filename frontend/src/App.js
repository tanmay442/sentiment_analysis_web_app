import React, { useState, useRef, useEffect } from 'react';
import UploadForm from './components/UploadForm';
import './App.css'; 

function App() {
  const [analysisResults, setAnalysisResults] = useState(null);
  const resultsRef = useRef(null); // Create a ref for the results section

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results);
  };

  // Effect to scroll to results when they are loaded
  useEffect(() => {
    if (analysisResults && resultsRef.current) {
      resultsRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  }, [analysisResults]); // Depend on analysisResults changing

  return (
    <div className="App">
      <header className="App-header">
        <h1>E-consultation Comment Analyzer</h1>
      </header>

      <main className="App-main-content">
        <UploadForm onAnalysisComplete={handleAnalysisComplete} />

        {analysisResults && (
          <section className="results-section" ref={resultsRef}> {/* Attach the ref here */}
            <h2>Analysis Results</h2>

            <div className="results-grid">
              <div className="sentiment-card">
                <h3>Sentiment Distribution:</h3>
                <ul className="sentiment-list">
                  {Object.entries(analysisResults.sentiment_counts).map(([sentiment, count]) => (
                    <li key={sentiment} className={`sentiment-item ${sentiment.toLowerCase()}`}>
                      <span className="sentiment-label">{sentiment}:</span>
                      <span className="sentiment-count">{count}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="summary-card">
                <h3>Summary:</h3>
                <p className="summary-text">
                  {analysisResults.summary}
                </p>
              </div>
            </div>

            <div className="word-cloud-container">
              <h3>Word Cloud:</h3>
              {analysisResults.word_cloud_image && (
                <img
                  src={`data:image/png;base64,${analysisResults.word_cloud_image}`}
                  alt="Word Cloud"
                  className="word-cloud-image"
                />
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
