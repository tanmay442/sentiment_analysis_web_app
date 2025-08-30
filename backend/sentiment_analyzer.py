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
    """Reads comments from a specified column (by name or index) in a CSV file."""
    try:
        # Try common encodings
        encodings_to_try = ['utf-8', 'latin1', 'cp1252']
        df = None
        for encoding in encodings_to_try:
            try:
                # Explicitly set separator and quote character
                df = pd.read_csv(file_path, header=None, encoding=encoding, sep=',', quotechar='"')
                break # If successful, break the loop
            except UnicodeDecodeError:
                continue # Try next encoding
            except pd.errors.ParserError as pe: # Catch pandas parsing errors
                print(f"ParserError with encoding {encoding}: {pe}")
                continue
        
        if df is None:
            raise ValueError("Could not decode or parse the CSV file with common encodings (utf-8, latin1, cp1252).")

        try:
            # If identifier is an integer, treat it as a column index
            col_index = int(comment_column_identifier)
            if col_index < 0 or col_index >= df.shape[1]:
                raise IndexError(f"Column index {col_index} is out of bounds for a CSV with {df.shape[1]} columns (0 to {df.shape[1]-1}).")
            return df.iloc[:, col_index].dropna().tolist()
        except ValueError:
            # If identifier is not an integer, treat it as a column name
            # Re-read with header=0 and the successful encoding to check for column name
            # Use the same parsing parameters
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
            return df_with_header[comment_column_identifier].dropna().tolist()

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return []

def analyze_sentiment(comments):
    """Performs sentiment analysis on a list of comments."""
    sentiments = []
    for comment in comments:
        analysis = TextBlob(comment)
        # Classify sentiment as positive, negative, or neutral
        if analysis.sentiment.polarity > 0:
            sentiments.append('Positive')
        elif analysis.sentiment.polarity < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    return sentiments

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
