from pandas import DataFrame
from utils.logging_utils import logger
import os


def save_results(task_name: str, results: DataFrame) -> None:
    """
    Save the results to a file.

    Args:
        task_name (str): The ID of the task.
        results (str): The results to be saved.

    Returns:
        None
    """
    os.makedirs("results", exist_ok=True)
    # Define the output file path
    output_file_path = f"results/{task_name}_results.csv"

    # Save the results to a CSV file
    results.to_csv(output_file_path, index=False)

    logger.info(f"Results saved to {output_file_path}")
