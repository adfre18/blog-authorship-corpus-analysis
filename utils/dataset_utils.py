import kagglehub
import pandas as pd
import os


def download_dataset(dataset_name: str) -> str:
    """
    Downloads the specified dataset from Kaggle and returns the path to the downloaded files.

    Args:
        dataset_name (str): The name of the dataset to download.

    Returns:
        str: The path to the downloaded dataset files.
    """
    # download dataset
    path = kagglehub.dataset_download(dataset_name)

    return path

def load_dataset_to_dataframe(path_to_dataset: str) -> pd.DataFrame:
    """
    Loads the dataset from the specified path into a pandas DataFrame.

    Args:
        path_to_dataset (str): The path to the dataset files.

    Returns:
        pd.DataFrame: The loaded dataset as a pandas DataFrame.
    """
    df = None
    for file in os.listdir(path_to_dataset):
        path_to_dataset = os.path.join(path_to_dataset, file)
        if file.endswith(".csv"):
            # load dataset
            df = pd.read_csv(path_to_dataset)
            break
        elif file.endswith('.xlsx'):
            # load dataset
            df = pd.read_excel(path_to_dataset)
            break
        else:
            raise ValueError(f"Unsupported file format: {file}. Only .csv and .xlsx files are supported.")
    if df is None:
        raise ValueError("No valid dataset file found in the specified path.")
    if os.path.exists(path_to_dataset):
        # add the dataset path to ENVIRONMENT params to use it streamlit
        os.environ['DATASET_PATH_TIPSPORT'] = path_to_dataset

    return df