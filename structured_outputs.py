from datetime import datetime

from typing import Literal, Optional
from pydantic import BaseModel, Field


class CalendarRequestType(BaseModel):
    """Route LLM call, define the calendar request type"""

    request_type: Literal["new_event", "modify_event", "other"] = Field(
        description="Type of calendar request beign made")
    
    confidence: float = Field(description="confidence score for the request_type between 0 and 1")
    description: str = Field(description="cleaned up description of the user request")


class NewEventDetails(BaseModel):
    """Parse event details"""
    name: str = Field(description="name of the event")
    start_time: str = Field(
        description="start date and time of the event. Use ISO 8601 to format this value.")
    end_time: str = Field(
        description="end date and time of the event. Use ISO 8601 to format this value.")
    duration: str = Field(description="Duration of the event")
    participants: list[str] = Field(description="List of participants")

class Change(BaseModel):
    """Details for changing the existing event"""
    field: str = Field(description="Field to change")
    new_value: str = Field(description="New value for the field")

class ModifyEventDetails(BaseModel):
    """Details for modifying the existing event"""
    event_identifier: str = Field(description="Description to identify the existing event")
    changes: list[Change] = Field(description="List of changes to make")
    participants_to_add: list[str] = Field(description="participants that needs to be added")
    participants_to_remove: list[str] = Field(description="participants that needs to be removed")
    
class EventConfirmation(BaseModel):
    """Generate confirmation message"""
    confirmation_message: str = Field(
        description="confirmation message in natural language")
    calendar_link: Optional[str] = Field(
        description="generated calendar link if applicable")
