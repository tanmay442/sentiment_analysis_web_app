import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard'; // Import the Dashboard component

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
      {/* Render the Dashboard component and pass necessary props */}
      <Dashboard
        analysisResults={analysisResults}
        setAnalysisResults={setAnalysisResults}
        resultsRef={resultsRef}
        onAnalysisComplete={handleAnalysisComplete}
      />
    </div>
  );
}

export default App;
