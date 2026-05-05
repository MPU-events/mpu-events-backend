from uuid import UUID
from datetime import datetime, timezone

from mpu_events.domain.exceptions.auth import PermissionDeniedException
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository
from mpu_events.application.dto.event_dto import UpdateEventDTO, EventResponseDTO
from mpu_events.domain.exceptions.events.events import EventNotFoundException
from mpu_events.domain.exceptions.events.registrations import AlreadyRegisteredException


class UpdateEventUseCase:
    def __init__(
        self, 
        event_repo: EventRepository,
        registration_repo: RegistrationRepository
    ):
        self.event_repo = event_repo
        self.registration_repo = registration_repo

    async def execute(
        self, 
        event_id: UUID, 
        dto: UpdateEventDTO,
        current_user_id: UUID,
        is_admin: bool
    ) -> EventResponseDTO:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundException(event_id)

        if not is_admin and event.created_by != current_user_id:
            raise PermissionDeniedException()

        if dto.title is not None:
            event.title = dto.title
        if dto.description is not None:
            event.description = dto.description
        if dto.location is not None:
            event.location = dto.location
        if dto.max_participants is not None:
            event.max_participants = dto.max_participants
        
        if dto.start_time is not None:
            start = dto.start_time
            if start.tzinfo is None:
                start = start.replace(tzinfo=timezone.utc)
            else:
                start = start.astimezone(timezone.utc)
            
            if start < datetime.now(timezone.utc):
                raise ValueError("Начало мероприятия не может быть в прошедшем времени")
            
            current_count = await self.registration_repo.count_by_event(event_id)
            if current_count > 0 and event.start_time != dto.start_time:
                print(f"⚠️ Внимание: изменение времени мероприятия, на которое уже записались {current_count} человек")
            
            event.start_time = dto.start_time

        updated = await self.event_repo.update(event)
        

        current_count = await self.registration_repo.count_by_event(event_id)

        return EventResponseDTO(
            id=updated.id,
            title=updated.title,
            description=updated.description,
            start_time=updated.start_time,
            location=updated.location,
            max_participants=updated.max_participants,
            current_participants=current_count,
            created_by=updated.created_by,
            created_at=updated.created_at
        )