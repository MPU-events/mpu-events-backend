from uuid import UUID
from mpu_events.domain.exceptions.auth import PermissionDeniedException
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository
from mpu_events.domain.exceptions.events.events import EventNotFoundException
from mpu_events.domain.exceptions.events.registrations import AlreadyRegisteredException


class DeleteEventUseCase:
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
        current_user_id: UUID,
        is_admin: bool
    ) -> None:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundException(event_id)

        if not is_admin and event.created_by != current_user_id:
            raise PermissionDeniedException()

        current_count = await self.registration_repo.count_by_event(event_id)
        if current_count > 0 and not is_admin:
            raise ValueError(f"Нельзя удалить мероприятие, на которое уже записалось {current_count} человек")

        await self.registration_repo.delete_by_event(event_id)
        
        await self.event_repo.delete(event_id)