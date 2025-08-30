# Sentiment Analysis Web App

This project is a full-stack web application for performing sentiment analysis on user-provided text or files. It consists of a Python Flask backend and a React frontend.

## Features
- Upload text or files for sentiment analysis
- Dashboard to view results
- Modern, responsive UI

## Project Structure
```
backend/
  app.py                # Flask API server
  requirements.txt      # Python dependencies
  sentiment_analyzer.py # Sentiment analysis logic
frontend/
  src/                  # React source code
  public/               # Static assets
  package.json          # Frontend dependencies
```

## Getting Started

### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React app:
   ```bash
   npm start
   ```

## Usage
- Access the frontend at `http://localhost:3000`.
- The backend API runs at `http://localhost:5000` by default.

## License
This project is licensed under the MIT License.
