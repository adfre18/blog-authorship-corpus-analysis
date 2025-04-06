import re

"""
This file contains constants used in the project.
"""

dollar_pattern = re.compile(
    r"\$(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?|\d+)([MBK]|\s*[-]?\s*(million|billion|thousand|bill|bn))?",
    re.IGNORECASE)