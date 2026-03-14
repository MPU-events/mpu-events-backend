from datetime import timezone
from uuid import UUID
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.entities.event import Event
from mpu_events.application.dto.event_dto import CreateEventDTO, EventResponseDTO


class CreateEventUseCase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    async def execute(self, dto: CreateEventDTO, admin_id: UUID) -> EventResponseDTO:
        event = Event(
            title=dto.title,
            description=dto.description,
            start_time=dto.start_time,
            location=dto.location,
            max_participants=dto.max_participants,
            created_by=admin_id,
        )
        created = await self.event_repo.create(event)
        return EventResponseDTO.model_validate(created)