from .task import Task
from utils.logging_utils import logger
from utils.text_processing import get_cleaned_words_from_text

from tqdm import tqdm
from pandas import DataFrame
from collections import Counter


class Task1(Task):
    """
    This class implements the first task of the project. It is responsible for processing the text data
    and finding the most common words across selected texts.

    Attributes:
        task_method (callable): The method to be used for processing the data.

    Methods:
        preprocess_data(data: DataFrame) -> list[str]:
            Preprocess the data for task 1. Applying filters for gender and age.
        _task_method(texts: list[str]) -> str:
            Process the texts to find the most common words across selected texts.
        prepare_string_output_format(data: list[tuple]) -> str:
            Prepare the output format for the task.
    """
    def __init__(self):
        """
        Initialize the Task1 class.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.task_method = self._task_method

    def preprocess_data(self, data: DataFrame) -> list[str]:
        """
        Preprocess the data for task 1. Applying filters for gender and age.

        Args:
            data (DataFrame): The input data.

        Returns:
            list[str]: A list of texts.
        """
        logger.info("Preprocessing data for task 1 - applying filters")
        # applying these specific filters
        selected_data = data[(data['gender'] == 'female') & (data['age'] >= 20) & (data['age'] <= 30)]
        selected_data = selected_data['text'].tolist()
        logger.info(f"Selected {len(selected_data)} texts for task 1")
        return selected_data

    def _task_method(self, texts: list[str]) -> DataFrame:
        """
        Process the texts to find the most common words across selected texts.

        Args:
            texts (list[str]): The input texts.

        Returns:
            DataFrame: A DataFrame with the most common words and their counts.
        """
        all_words = []
        logger.info("Processing texts - extracting keywords")

        for text in tqdm(texts, desc="Processing texts - extracting keywords"):
            # Clean the text
            cleaned_words = get_cleaned_words_from_text(text)
            # save just those words with at least 5 chars and with no vowels at the end or at the beginning
            cleaned_words = [word
                             for word in cleaned_words
                             if (len(word) >= 5 and word[-1] not in 'aeiou' and word[0] not in 'aeiou')]
            all_words.extend(cleaned_words)

        logger.info("Counting occurrences of words")

        # Count the occurrences of each word
        word_counts = Counter(all_words)

        # get 10 most common words
        most_common_words = word_counts.most_common(10)
        return self.prepare_dataframe_output_format(most_common_words)

    @staticmethod
    def prepare_dataframe_output_format(data: list[tuple]) -> DataFrame:
        """
        Prepare the output format for the task.

        Args:
            data (list[tuple]): The most common words and their counts.

        Returns:
           DataFrame: A DataFrame with the most common words and their counts.
        """
        df = DataFrame(data, columns=['word', 'count'])

        return df