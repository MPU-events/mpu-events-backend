from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime


class CreateEventDTO(BaseModel):
    title: str
    description: str
    start_time: datetime
    location: str
    max_participants: int | None = None


class UpdateEventDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    location: str | None = None
    max_participants: int | None = None


class EventResponseDTO(BaseModel):
    id: UUID
    title: str
    description: str
    start_time: datetime
    location: str
    max_participants: int | None
    current_participants: int = 0
    created_by: UUID
    created_at: datetime

    model_config = {"from_attributes": True}

class EventFilterDTO(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    start_date: date | None
    end_date: date | None