import React, { useState } from 'react';
import './UploadForm.css'; // Create this CSS file for specific form styles

function UploadForm({ onAnalysisComplete }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [commentColumn, setCommentColumn] = useState('5'); // Default to column 5
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleColumnChange = (event) => {
    setCommentColumn(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      setError('Please select a CSV file.');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('comment_column', commentColumn);

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Analysis failed.');
      }

      const data = await response.json();
      onAnalysisComplete(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <h2>Upload CSV for Sentiment Analysis</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <div>
          <label htmlFor="csvFile">Select CSV File:</label>
          <input
            type="file"
            id="csvFile"
            accept=".csv"
            onChange={handleFileChange}
          />
        </div>
        <div>
          <label htmlFor="commentColumn">
            Comment Column Name or Index (e.g., 'text' or '5'):
          </label>
          <input
            type="text"
            id="commentColumn"
            value={commentColumn}
            onChange={handleColumnChange}
            placeholder="e.g., 'text' or '5'"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Comments'}
        </button>
      </form>
      {error && <p className="error-message">Error: {error}</p>}
    </div>
  );
}

export default UploadForm;