import re
from utils.logging_utils import logger

def parse_dollar_amount(detected_string: str) -> float:
    """
    Convert a string representing a dollar amount into a float.

    The function handles various formats, including:
    - "$1,000"
    - "$1 million"
    - "$1.5 billion"
    - "$1.5M"

    Args:
        detected_string (str): The string to be converted.

    Returns:
        float: The dollar amount as a float.
    """
    # Remove dollar sign and commas
    detected_string = detected_string.replace('$', '').replace(',', '')
    detected_string = detected_string.strip().lower()

    # Check if the string contains M, B, K
    multiplier = 1
    if 'm' in detected_string or 'million' in detected_string:
        multiplier = 1_000_000
    elif 'b' in detected_string or 'billion' in detected_string:
        multiplier = 1_000_000_000
    elif 'k' in detected_string or 'thousand' in detected_string:
        multiplier = 1_000
    else:
        if any(c.isalpha() for c in detected_string):
            # If the string contains letters, return None
            logger.info(f"Invalid dollar amount: {detected_string}")
            return 0

    # Extract the number and multiply by the corresponding factor
    number_part = re.search(r'\d+(\.\d+)?', detected_string)
    if number_part:
        return float(number_part.group()) * multiplier
    else:
        # If no number is found, return None
        logger.info(f"Invalid dollar amount: {detected_string}")
        return 0