import nltk
from nltk.corpus import words
import re

# Download the words corpus if not already downloaded
nltk.download('words', quiet=True)

english_words_list = set(words.words())

def get_cleaned_words_from_text(text: str):
    """
    Cleans the input text by removing unwanted characters and splitting it into words.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        list: A list of cleaned words.
    """
    # Remove unwanted characters
    cleaned_text = re.sub(r'[^\w\s]', '', text)

    # Split the cleaned text into words
    words = [word.lower() for word in cleaned_text.split() if word.lower() in english_words_list]

    return words