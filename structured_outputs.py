from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field


class EventExtraction(BaseModel):
    """First LLM call: Extract basic event information"""

    description: str = Field(description="Raw description of the event")
    is_calendar_event: bool = Field(
        description="Whether this text describes a calendar event"
    )
    confidence_score: float = Field(
        description="Confidence score between 0 and 1")


class EventDetails(BaseModel):
    """Second LLM call: Parse event details"""
    name: str = Field(description="name of the event")
    start_time: str = Field(
        description="start date and time of the event. Use ISO 8601 to format this value.")
    end_time: str = Field(
        description="end date and time of the event. Use ISO 8601 to format this value.")
    duration: str = Field(description="Duration of the event")
    participants: list[str] = Field(description="List of participants")


class EventConfirmation(BaseModel):
    """Third LLM call: Generate confirmation message"""
    confirmation_message: str = Field(
        description="confirmation message in natural language")
    calendar_link: Optional[str] = Field(
        description="generated calendar link if applicable")
