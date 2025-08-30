from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import nltk
import tempfile
import base64
from io import BytesIO
import pandas as pd # Import pandas here as it's used for pd.Series
import traceback # Import traceback module

# Import sentiment analysis functions
from sentiment_analyzer import read_comments_from_csv, analyze_sentiment, generate_summary, generate_word_cloud_image

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# Download NLTK data (only needs to be done once when the app starts)
def download_nltk_data():
    try:
        nltk.data.find('corpora/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
    print("NLTK data downloaded/checked.")

# Call the download function when the app starts
download_nltk_data()

@app.route('/analyze', methods=['POST'])
def analyze_comments():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    comment_column_identifier = request.form.get('comment_column', '5') # Default to column 5

    if file:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            file.save(tmp_file.name)
            temp_file_path = tmp_file.name

        try:
            comments = read_comments_from_csv(temp_file_path, comment_column_identifier)

            if not comments:
                return jsonify({'error': 'No comments found or unable to read CSV.'}), 400

            sentiments = analyze_sentiment(comments)
            sentiment_counts = pd.Series(sentiments).value_counts().to_dict()
            
            # Generate a summary of all comments
            # Join the list of comments into a single string for summarization
            all_comments_text = " ".join(comments)
            summary = generate_summary(all_comments_text)
            
            word_cloud_base64 = generate_word_cloud_image(comments)

            return jsonify({
                'sentiment_counts': sentiment_counts,
                'summary': summary,
                'word_cloud_image': word_cloud_base64
            })
        except Exception as e:
            # Print the full traceback to the console for debugging
            print("An error occurred during analysis:")
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
