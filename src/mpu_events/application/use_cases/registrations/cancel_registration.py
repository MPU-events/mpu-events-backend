from uuid import UUID

from mpu_events.domain.exceptions.events.events import EventNotFoundException
from mpu_events.domain.exceptions.events.registrations import RegistrationNotFoundException
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository


class CancelRegistrationUseCase:
    def __init__(self, event_repo: EventRepository, registration_repo: RegistrationRepository):
        self.event_repo = event_repo
        self.registration_repo = registration_repo

    async def execute(self, user_id: UUID, event_id: UUID) -> None:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundException()

        registration = await self.registration_repo.get_by_user_and_event(user_id, event_id)
        if not registration:
            raise RegistrationNotFoundException()

        await self.event_repo.update(event)
        await self.registration_repo.delete(registration.id)