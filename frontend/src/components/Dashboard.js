import React from 'react';
import './Dashboard.css';
import UploadForm from './UploadForm';
import { Bar } from 'react-chartjs-2'; // Import Bar chart
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'; // Import Chart.js components

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Dashboard({ analysisResults, setAnalysisResults, resultsRef, onAnalysisComplete }) {
  // Prepare data for Sentiment Distribution Chart
  const sentimentChartData = {
    labels: analysisResults ? Object.keys(analysisResults.sentiment_counts) : [],
    datasets: [
      {
        label: 'Number of Comments',
        data: analysisResults ? Object.values(analysisResults.sentiment_counts) : [],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)', // Positive
          'rgba(255, 99, 132, 0.6)',  // Negative
          'rgba(255, 206, 86, 0.6)',  // Neutral
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const sentimentChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#e0e0e0', // Light text for legend
        },
      },
      title: {
        display: true,
        text: 'Sentiment Distribution',
        color: '#e0e0e0', // Light text for title
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y;
            }
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#e0e0e0', // Light text for x-axis labels
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)', // Subtle grid lines
        },
      },
      y: {
        ticks: {
          color: '#e0e0e0', // Light text for y-axis labels
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)', // Subtle grid lines
        },
      },
    },
  };

  return (
    <div className="dashboard-container">
      <header className="App-header">
        <h1>E-consultation Comment Analyzer</h1>
      </header>

      <main className="App-main-content">
        <UploadForm onAnalysisComplete={onAnalysisComplete} />

        {analysisResults && (
          <section className="results-section" ref={resultsRef}>
            <h2>Analysis Results</h2>

            {/* Full-width Summary Card */}
            <div className="full-width-summary-card glass-card">
              <h3>Summary:</h3>
              <p className="summary-text">
                {analysisResults.summary}
              </p>
            </div>

            <div className="results-grid">
              {/* Sentiment Distribution Card with Chart */}
              <div className="sentiment-card glass-card">
                <h3>Sentiment Distribution:</h3>
                <div className="chart-container">
                  <Bar data={sentimentChartData} options={sentimentChartOptions} />
                </div>
                {/* Original list for sentiment counts - can be removed or kept based on preference */}
                <ul className="sentiment-list">
                  {Object.entries(analysisResults.sentiment_counts).map(([sentiment, count]) => (
                    <li key={sentiment} className={`sentiment-item ${sentiment.toLowerCase()}`}>
                      <span className="sentiment-label">{sentiment}:</span>
                      <span className="sentiment-count">{count}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Grouped Statistical and Data Quality Cards */}
              <div className="stats-and-quality-grid">
                {/* New card for Sentiment Statistics (Mean/Median) */}
                <div className="sentiment-stats-card glass-card">
                  <h3>Sentiment Statistics:</h3>
                  <p><strong>Mean Sentiment:</strong> {analysisResults.sentiment_mean.toFixed(2)}</p>
                  <p><strong>Median Sentiment:</strong> {analysisResults.sentiment_median.toFixed(2)}</p>
                </div>

                {/* New card for Common Keywords */}
                <div className="keywords-card glass-card">
                  <h3>Common Keywords:</h3>
                  {Object.entries(analysisResults.common_keywords_by_sentiment).map(([sentiment, keywords]) => (
                    <div key={sentiment}>
                      <h4>{sentiment}:</h4>
                      <ul className="keyword-list">
                        {keywords.map(([keyword, count]) => (
                          <li key={keyword}>{keyword} ({count})</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>

                {/* New card for Data Quality Metrics */}
                <div className="data-quality-card glass-card">
                  <h3>Data Quality:</h3>
                  <p><strong>Total Comments Read:</strong> {analysisResults.data_quality_metrics.total_comments_read}</p>
                  <p><strong>Null Comments:</strong> {analysisResults.data_quality_metrics.null_comments_count}</p>
                  <p><strong>Non-String Comments:</strong> {analysisResults.data_quality_metrics.non_string_comments_count}</p>
                  <p><strong>Processed Comments:</strong> {analysisResults.data_quality_metrics.processed_comments_count}</p>
                </div>
              </div>
            </div>

            <div className="word-cloud-container glass-card">
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

export default Dashboard;