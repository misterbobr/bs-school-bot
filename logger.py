import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level to ERROR
logger.setLevel(logging.ERROR)

# Create a file handler
file_handler = logging.FileHandler('errors.log')

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)