from utils.data_utils import save_results
from pandas import DataFrame


class Task:
    """
    This class is a base class for all tasks in the project. It provides a structure for preprocessing data,
    running the task, and preparing the output format.

    Attributes:
        task_method (callable): The method to be used for processing the data.

    Methods:
        preprocess_data(data: DataFrame) -> DataFrame:
            Preprocess the data for the task. This method should be overridden in subclasses.
        run(data: DataFrame) -> None:
            Run the task method on the preprocessed data. This method should be overridden in subclasses.
    """

    def __init__(self):
        """
        Initialize the Task class.

        Args:
            None

        Returns:
            None
        """
        self.task_method = None

    def preprocess_data(self, data: DataFrame) -> list[str]:
        """
        Preprocess the data for the task. This method should be overridden in subclasses.

        Args:
            data (DataFrame): The input data.

        Returns:
            list[str]: A list of texts.
        """
        pass

    def run(self, data: DataFrame) -> None:
        """
        Run the task method on the preprocessed data. Each task should implement its own run method.

        Args:
            data (DataFrame): The input data.

        Returns:
            str: The result of the task method.
        """
        # Preprocess the data
        preprocessed_data = self.preprocess_data(data)
        # Run the task method
        result = self.task_method(preprocessed_data)

        # Save the result
        save_results(self.__class__.__name__, result)


