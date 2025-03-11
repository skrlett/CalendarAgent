from datetime import datetime
from typing import Optional
from structured_outputs import EventConfirmation, CalendarRequestType, ModifyEventDetails, NewEventDetails
from client import client
from config import setup_logging

# Set up logging
logger = setup_logging()


def route_calendar_request(user_input: str) -> CalendarRequestType:
    """LLM call to determine the type of calendar request being made"""
    logger.info("Routing Calendar Request")

    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": "Determine if this request is to create new calendar event or modify an existing one."
        }, {"role": "user", "content": user_input}],

        response_format=CalendarRequestType
    )

    result = chat_completion.choices[0].message.parsed

    logger.info(f"Routing Result: {result}")

    return result


def handle_new_event(user_input: str) -> NewEventDetails:
    """LLM call to process create new event"""
    logger.info("creating a new event")

    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": "Extract the details of the new event."
        }, {"role": "user", "content": user_input}],
        response_format=NewEventDetails
    )

    result = chat_completion.choices[0].message.parsed

    logger.info(f"New Evevnt Creation Information {result}")

    """Here, you can process the event details and then create a event
    with your calendar api"""

    return result


def handle_modity_event(user_input: str) -> ModifyEventDetails:
    """LLM call to process modift event"""
    logger.info(f"Modifying the event {user_input}")

    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": "Extract details for modifying an existing calendar event."
        }, {
            "role": "user",
            "content": user_input}],
        response_format=ModifyEventDetails,
    )

    result = chat_completion.choices[0].message.parsed

    logger.info(f"modified event details {result}")

    return result


def process_calendar_request(user_input: str) -> str:
    """Main function for LLM Calls"""
    logger.info("Processing Calendar Request")

    # route the request
    route_result = route_calendar_request(user_input=user_input)

    if route_result.confidence < 0.7:
        logger.warning(f"Low confidence score {route_result.confidence}")
        return None
    
    # Route to appropriate handler
    if route_result.request_type == "modify_event":
        return handle_modity_event(user_input=user_input)
    elif route_result.request_type == "new_event":
        return handle_new_event(user_input=user_input)
    else:
        logger.warning("Request type not supported")
        return None


