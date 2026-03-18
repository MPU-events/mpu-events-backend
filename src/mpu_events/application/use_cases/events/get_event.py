from uuid import UUID
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository
from mpu_events.application.dto.event_dto import EventResponseDTO
from mpu_events.domain.exceptions.events.events import EventNotFoundException


class GetEventUseCase:
    def __init__(
            self,
            event_repo: EventRepository,
            registration_repo: RegistrationRepository
    ):
        self.event_repo = event_repo
        self.registration_repo = registration_repo

    async def execute(self, event_id: UUID) -> EventResponseDTO:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundException()

        current_participants = await self.registration_repo.count_by_event(event_id)

        return EventResponseDTO(
            id=event.id,
            title=event.title,
            description=event.description,
            start_time=event.start_time,
            location=event.location,
            max_participants=event.max_participants,
            current_participants=current_participants,
            created_by=event.created_by,
            created_at=event.created_at
        )