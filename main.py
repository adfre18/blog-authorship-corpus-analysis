from utils.dataset_utils import download_dataset, load_dataset_to_dataframe
from utils.logging_utils import logger
from tasks import Task1, Task2, Task3
from config import streamlit_filepath_webapp, streamlit_exe_filepath
import subprocess


def main():
    """
    Main function to run the tasks and start the Streamlit app.
    
    Args:
        None
        
    Returns:
        None
    """
    logger.info('Starting the main function...')
    logger.info('Downloading the dataset...')
    # Download latest version of the dataset
    path = download_dataset("rtatman/blog-authorship-corpus")
    logger.info(f'Dataset downloaded to {path}')
    logger.info('Loading the dataset into a DataFrame...')
    # Load dataset
    df = load_dataset_to_dataframe(path)

    # iterate over all tasks
    for task in [Task1(), Task2(), Task3()]:
        logger.info(f'Starting task: {task.__class__.__name__} ...')
        task.run(df)
        logger.info(f'Finished task: {task.__class__.__name__} ...')

    logger.info('All tasks completed successfully!')

    # Start the streamlit app
    logger.info('Starting streamlit app to visualize results...')
    subprocess.run([streamlit_exe_filepath, "run", streamlit_filepath_webapp, "--server.port", "8501"], check=True)


if __name__ == '__main__':
    main()
