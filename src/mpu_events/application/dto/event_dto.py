from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


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