import dotenv
import os
import logging

dotenv.load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    return logger
