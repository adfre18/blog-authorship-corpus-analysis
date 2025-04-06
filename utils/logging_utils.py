from logging import getLogger, StreamHandler, Formatter, INFO

# Set up logger
logger = getLogger('main_logger')
logger.setLevel(INFO)  # Set the logging level to INFO or DEBUG, etc.

# Create a formatter
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create console handler
ch = StreamHandler()

# Set formatter for the handler
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)