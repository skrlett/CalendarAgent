from openai import OpenAI
from config import OPEN_AI_API_KEY, setup_logging

# Set up logging
logger = setup_logging()

# Initialize the OpenAI client
try:
    logger.info("Initializing OpenAI Client with API Key.")
    client = OpenAI(api_key=OPEN_AI_API_KEY)
    logger.info("OpenAI Client Initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize openai client: %s", e, exc_info=True)
