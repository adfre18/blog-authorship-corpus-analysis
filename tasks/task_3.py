from .task import Task
from utils.logging_utils import logger
from utils.consts import dollar_pattern
from utils.finance_utils import parse_dollar_amount

from pandas import DataFrame


class Task3(Task):
    """
    This class implements the third task of the project. It is responsible for processing the text data
    and finding the total sum of dollar amounts across selected texts.

    Attributes:
        task_method (callable): The method to be used for processing the data.

    Methods:
        preprocess_data(data: DataFrame) -> list[str]:
            Preprocess the data for task 3. No filters are applied.

        _task_method(texts: list[str]) -> str:
            Process the texts to find the total sum of dollar amounts.

        prepare_string_output_format(data: int) -> str:
            Prepare the output format for the task.
    """
    def __init__(self):
        """
        Initialize the Task3 class.

        Args:
            None
        Returns:
            None
        """
        super().__init__()
        self.task_method = self._task_method

    def preprocess_data(self, data: DataFrame) -> list[str]:
        """
        Preprocess the data for task 3. No filters are applied.

        Args:
            data (DataFrame): The input data.
        Returns:
            list[str]: A list of texts.
        """
        logger.info("Preprocessing data for task 3 - applying filters")
        selected_data = data['text'].tolist()
        logger.info(f"Selected {len(selected_data)} texts for task 3")
        return selected_data

    def _task_method(self, texts: list[str]) -> DataFrame:
        """
        Process the texts to find the total sum of dollar amounts.

        Args:
            texts (list[str]): A list of texts.
        Returns:
            DataFrame: The formatted output with the total sum of dollar amounts.
        """
        total_sum = 0
        logger.info("Processing texts - extracting dollar amounts")
        for text in texts:
            # Find all dollar amounts in the text
            matches = dollar_pattern.finditer(text)
            for match in matches:
                dollar_value = match.group()
                # if dollar value is found parse it
                dollar_value = parse_dollar_amount(dollar_value)
                if dollar_value:
                    total_sum += dollar_value
        logger.info("Extracting dollar amounts - done")
        return self.prepare_string_output_format(total_sum)

    @staticmethod
    def prepare_string_output_format(data: int) -> DataFrame:
        """
        Prepare the output format for the task.

        Args:
            data (int): The total sum of dollar amounts.

        Returns:
            DataFrame: The formatted output with the total sum of dollar amounts.
        """
        df = DataFrame({'Total Dollar Amount Billion $': [data / 1e9]})
        return df