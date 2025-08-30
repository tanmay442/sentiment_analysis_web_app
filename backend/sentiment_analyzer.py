import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import os
import base64
from io import BytesIO
import csv # Import csv module for quoting options

# NLTK data downloads (will be handled by app.py or a setup script)
# try:
#     nltk.data.find('corpora/punkt')
# except LookupError:
#     nltk.download('punkt')
# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords')
# try:
#     nltk.data.find('tokenizers/punkt_tab')
# except LookupError:
#     nltk.download('punkt_tab')

def read_comments_from_csv(file_path, comment_column_identifier):
    """
    Reads comments from a specified column (by name or index) in a CSV file.
    Returns a tuple: (processed_comments_list, data_quality_metrics_dict)
    """
    data_quality_metrics = {
        'total_comments_read': 0,
        'null_comments_count': 0,
        'non_string_comments_count': 0,
        'processed_comments_count': 0
    }
    
    try:
        encodings_to_try = ['utf-8', 'latin1', 'cp1252']
        df = None
        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(file_path, header=None, encoding=encoding, sep=',', quotechar='"')
                break
            except UnicodeDecodeError:
                continue
            except pd.errors.ParserError as pe:
                print(f"ParserError with encoding {encoding}: {pe}")
                continue
        
        if df is None:
            raise ValueError("Could not decode or parse the CSV file with common encodings (utf-8, latin1, cp1252).")

        comments_series = None
        try:
            col_index = int(comment_column_identifier)
            if col_index < 0 or col_index >= df.shape[1]:
                raise IndexError(f"Column index {col_index} is out of bounds for a CSV with {df.shape[1]} columns (0 to {df.shape[1]-1}).")
            comments_series = df.iloc[:, col_index]
        except ValueError:
            df_with_header = None
            for encoding_retry in encodings_to_try:
                try:
                    df_with_header = pd.read_csv(file_path, header=0, encoding=encoding_retry, sep=',', quotechar='"')
                    break
                except UnicodeDecodeError:
                    continue
                except pd.errors.ParserError as pe_retry:
                    print(f"ParserError (with header) with encoding {encoding_retry}: {pe_retry}")
                    continue
            
            if df_with_header is None:
                raise ValueError("Could not decode or parse the CSV file (with header) with common encodings.")

            if comment_column_identifier not in df_with_header.columns:
                raise ValueError(f"Column '{comment_column_identifier}' not found in the CSV file with or without header.")
            comments_series = df_with_header[comment_column_identifier]

        data_quality_metrics['total_comments_read'] = len(comments_series)
        
        # Count nulls
        initial_comments = comments_series.tolist()
        comments_after_dropna = comments_series.dropna()
        data_quality_metrics['null_comments_count'] = data_quality_metrics['total_comments_read'] - len(comments_after_dropna)

        # Filter out non-string comments and count them
        processed_comments = []
        for comment in comments_after_dropna:
            if isinstance(comment, str):
                processed_comments.append(comment)
            else:
                data_quality_metrics['non_string_comments_count'] += 1
        
        data_quality_metrics['processed_comments_count'] = len(processed_comments)

        return processed_comments, data_quality_metrics

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return [], data_quality_metrics # Return empty list and default metrics
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return [], data_quality_metrics # Return empty list and default metrics

def analyze_sentiment(comments):
    """Performs sentiment analysis on a list of comments, returning categorical and numerical sentiment."""
    results = []
    for comment in comments:
        analysis = TextBlob(comment)
        sentiment_category = ''
        numerical_sentiment = 0 # Default to neutral

        if analysis.sentiment.polarity > 0:
            sentiment_category = 'Positive'
            numerical_sentiment = 1
        elif analysis.sentiment.polarity < 0:
            sentiment_category = 'Negative'
            numerical_sentiment = -1
        else:
            sentiment_category = 'Neutral'
            numerical_sentiment = 0
        
        results.append({
            'comment': comment,
            'sentiment': sentiment_category,
            'numerical_sentiment': numerical_sentiment,
            'polarity': analysis.sentiment.polarity, # Also return polarity for potential future use
            'subjectivity': analysis.sentiment.subjectivity # And subjectivity
        })
    return results

import nltk
import os
import base64
from io import BytesIO
import csv # Import csv module for quoting options

# Ensure NLTK punkt tokenizer is available
# This is handled by app.py's download_nltk_data, but good to ensure here if this file is run standalone
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def generate_summary(text, num_sentences=3):
    """Generates a summary from a given text."""
    # Define a maximum number of sentences to process to prevent memory errors
    MAX_SENTENCES_FOR_SUMMARIZATION = 2000 # Reduced for faster processing of large files

    # Tokenize the text into sentences using NLTK's punkt tokenizer
    sentences = nltk.sent_tokenize(text)

    # If the number of sentences is too high, truncate the list of sentences
    if len(sentences) > MAX_SENTENCES_FOR_SUMMARIZATION:
        sentences = sentences[:MAX_SENTENCES_FOR_SUMMARIZATION]
        # Also, adjust the number of sentences to be summarized if it's greater than the new total
        if num_sentences > MAX_SENTENCES_FOR_SUMMARIZATION:
            num_sentences = MAX_SENTENCES_FOR_SUMMARIZATION

    # Join the (potentially truncated) sentences back into a single string
    truncated_text = " ".join(sentences)

    parser = PlaintextParser.from_string(truncated_text, Tokenizer("english"))
    
    summarizer = LsaSummarizer()
    summarizer.stop_words = nltk.corpus.stopwords.words("english") # Set stopwords for better summarization
    summary_sentences = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary_sentences])

def generate_word_cloud_image(comments):
    """Generates a word cloud image and returns it as a base64 encoded string."""
    text = " ".join(comments)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    # Save image to a bytes buffer
    img_buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    img_buffer.seek(0) # Rewind buffer to the beginning
    plt.close() # Close the plot to free memory

    # Encode image to base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return img_base64

from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_common_keywords(analysis_results, top_n=10):
    """
    Extracts common keywords for each sentiment category.
    analysis_results: List of dictionaries, each containing 'comment' and 'sentiment'.
    """
    positive_comments = " ".join([res['comment'] for res in analysis_results if res['sentiment'] == 'Positive'])
    negative_comments = " ".join([res['comment'] for res in analysis_results if res['sentiment'] == 'Negative'])
    neutral_comments = " ".join([res['comment'] for res in analysis_results if res['sentiment'] == 'Neutral'])

    stop_words = set(stopwords.words('english'))
    
    def get_keywords(text):
        words = word_tokenize(text.lower())
        # Filter out stopwords, non-alphabetic tokens, and single-character tokens
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 1]
        return Counter(filtered_words).most_common(top_n)

    common_keywords = {
        'Positive': get_keywords(positive_comments),
        'Negative': get_keywords(negative_comments),
        'Neutral': get_keywords(neutral_comments)
    }
    return common_keywords
