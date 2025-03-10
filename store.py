import json

from config import setup_logging

# Set up logging
logger = setup_logging()

def email_store():
    """returns the json data of name and emails of people present in the store"""
    try:
        logger.info("Opening Email Store")
        with open("store.json", "r") as f:
            loaded_data = json.load(f)
            logger.info("Opened Email Store Successfully")
            return loaded_data
    except Exception as e:
        logger.error("Failed to read email store %s", e, exc_info=True)

messages = []