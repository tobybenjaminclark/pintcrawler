import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Preprocessing function: tokenize, remove stop words, and lemmatize
def preprocess_text(text):
    # Convert text to lowercase and tokenize
    tokens = word_tokenize(text.lower())

    # Remove stopwords (you can extend this list if needed)
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize tokens to reduce them to their base form
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Reconstruct the processed tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


# Thematic analysis function: returns "Positive" or "Negative" based on review sentiment
def thematic_analysis(review):
    """
    Performs sentiment analysis on a review and classifies it as Positive or Negative.

    Parameters:
        review (str): The review text.

    Returns:
        str: "Positive" if the sentiment is positive, otherwise "Negative".
    """
    # Preprocess the review text
    processed_review = preprocess_text(review)

    # Initialize the Vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Get the sentiment scores
    scores = analyzer.polarity_scores(processed_review)

    # Vader provides a compound score between -1 (most negative) and +1 (most positive)
    # We use a threshold of 0.05 for positive sentiment, per Vader's recommendation.
    if scores['compound'] >= 0.05:
        return "Positive"
    else:
        return "Negative"


# Example usage:
if __name__ == "__main__":
    sample_reviews = [
        "I absolutely loved this product! It exceeded all my expectations.",
        "This is the worst purchase I have ever made. Completely disappointed.",
        "The product is okay, not great but not terrible either."
    ]

    for review in sample_reviews:
        sentiment = thematic_analysis(review)
        print(f"Review: {review}\nSentiment: {sentiment}\n")
