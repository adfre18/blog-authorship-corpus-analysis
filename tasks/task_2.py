from .task import Task
from utils.logging_utils import logger
from utils.text_processing import get_cleaned_words_from_text

from tqdm import tqdm
from pandas import DataFrame
import numpy as np
from gensim.models import FastText
from sklearn.neighbors import NearestNeighbors

class Task2(Task):
    """
    This class implements the second task of the project. It is responsible for processing the text data
    and finding the most similar words using FastText and NearestNeighbors.

    Attributes:
        task_method (callable): The method to be used for processing the data.

    Methods:
        preprocess_data(data: DataFrame) -> list[str]:
            Preprocess the data for task 2. No filters are applied.

        _task_method(texts: list[str]) -> str:
            Process the texts to find the most similar words using FastText and NearestNeighbors.

        prepare_string_output_format(data: list[tuple]) -> str:
            Prepare the output format for the task.
    """
    def __init__(self):
        """
        Initialize the Task2 class.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.task_method = self._task_method

    def preprocess_data(self, data: DataFrame) -> list[str]:
        """
        Preprocess the data for task 2. No filters are applied.

        Args:
            data (DataFrame): The input data.

        Returns:
            list[str]: A list of texts.
        """
        logger.info("Preprocessing data for task 2 - applying filters")
        selected_data = data['text'].tolist()
        logger.info(f"Selected {len(selected_data)} texts for task 2")
        return selected_data

    def _task_method(self, texts: list[str]) -> DataFrame:
        """
        Process the texts to find the most similar words using FastText and NearestNeighbors.

        Args:
            texts (list[str]): The input texts.

        Returns:
            DataFrame: A DataFrame with the most similar words and their distances.
        """
        all_words = []
        logger.info("Processing texts - extracting keywords")

        for text in tqdm(texts, desc="Processing texts - extracting keywords"):
            # Clean the text
            cleaned_words = get_cleaned_words_from_text(text)
            # save just those words with at least 6 chars and at most 45 chars
            # (45 is number of letters for the longest word in English)
            # + using just words with letters
            cleaned_words = [word
                             for word in cleaned_words
                             if (6 <= len(word) <= 45)]
            all_words.extend(cleaned_words)
        logger.info('Extracting unique words')
        # get list of unique words to simplify the process
        unique_words = list(set(all_words))

        logger.info('Vectorizing words using FastText')
        # using FastText model to get word embeddings
        model = FastText(sentences=[[w] for w in unique_words], vector_size=50, min_count=1)
        # Get embeddings
        embeddings = np.array([model.wv[w] for w in unique_words])

        logger.info('Finding most similar words using NearestNeighbors')
        # setting n_neighbors to 2 to get the most similar pairs of words (first index is the word itself)
        nn = NearestNeighbors(n_neighbors=2, metric='cosine').fit(embeddings)
        distances, indices = nn.kneighbors(embeddings)

        logger.info('Sorting distances and indices')
        # sorting the distances + pairs of words
        sorted_distances = sorted(zip(distances, indices), key=lambda x: x[0][1])
        # get 50 most similar pairs of words
        most_similar_pairs = [
            (unique_words[i], unique_words[j], d[0][1]) for d, (i, j) in zip(sorted_distances[:50], indices[:50])
        ]
        return self.prepare_string_output_format(most_similar_pairs)

    @staticmethod
    def prepare_string_output_format(data: list[tuple]) -> DataFrame:
        """
        Prepare the output format for the task.

        Args:
            data (list[tuple]): The input data.

        Returns:
            DataFrame: A DataFrame with the most similar words and their distances.
        """

        df = DataFrame(data, columns=['word1', 'word2', 'distance'])

        return df


