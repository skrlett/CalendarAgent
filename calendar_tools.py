from datetime import datetime
from typing import Optional
from structured_outputs import EventExtraction, EventDetails, EventConfirmation
from client import client
from config import setup_logging

# Set up logging
logger = setup_logging()


def create_event(from_time: datetime, to_time: datetime, message: str, email: str) -> bool:
    pass


def get_events(from_time: datetime, to_time: datetime, message: str, email: str):
    pass


def is_available(from_time: datetime, to_time: datetime) -> bool:
    pass


def update_event(event_id: str, from_time: datetime, to_time: datetime, message: str) -> bool:
    pass


def extract_event_info(user_input: str) -> EventExtraction:
    """First LLM call to extract event info"""
    logger.info("starting event info, extraction process")
    logger.debug(f"user_input: {user_input}")

    today = datetime.now()
    date_content = f"Today is {today.strftime("%A, %B %d, %Y")}"
    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "system", "content": f"{date_content} is the event a calendar event?"},
                  {"role": "user", "content": user_input}],
        response_format=EventExtraction
    )

    result = chat_completion.choices[0].message.parsed

    logger.info(
        f"Extraction complete - Is calendar event: {result.is_calendar_event}, Confidence: {result.confidence_score:.2f}"
    )

    return result


def parse_event_details(description: str) -> EventDetails:
    """Second LLM Call: Extract event details"""
    logger.info("Second LLM call: parsing event details")
    logger.debug(f"description: {description}")

    today = datetime.now()
    date_context = f"today is {today.strftime("%A, %B %d, %Y")}"
    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "system", "content": f"{date_context} Extract event data relative to todays date"},
                  {"role": "user", "content": description}],
        response_format=EventDetails
    )

    result = chat_completion.choices[0].message.parsed

    logger.info(
        f"parsed event details: {result}"
    )

    return result


def generate_confirmation(eventDetails: EventDetails) -> str:
    """Generate event confirmation message using the event details"""

    logger.info("generating event confirmation")
    logger.debug(f"eventDetails: {eventDetails}")

    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Generate natural language event confirmation message"},
                  {"role": "user", "content": str(eventDetails.model_dump())}],
        response_format=EventConfirmation
    )
    result = chat_completion.choices[0].message.parsed

    logger.info(f"results: {result}")

    return result

def process_calendar_request(user_input: str) -> Optional[EventConfirmation]:
    """Main function to run all the LLM calls"""
    logger.info("processing calendar request")
    logger.debug(f"user_input: {user_input}")

    init_data_extraction = extract_event_info(user_input=user_input)

    # Gate check if the event is a calendar event
    if not init_data_extraction.is_calendar_event or init_data_extraction.confidence_score < 0.6:
        logger.warning(f"Gate Check failed, {user_input} is not a calendar event")
        return None
    
    logger.info("Gate check passed, proceeding with event processing")
    event_details_extraction = parse_event_details(init_data_extraction.description)
    logger.info("completed event data extraction, proceeding to genrate confirmation")

    event_confirmation = generate_confirmation(event_details_extraction)
    logger.info(f"succesfully compiled the event genration message{event_confirmation.confirmation_message}")

    return event_confirmation

