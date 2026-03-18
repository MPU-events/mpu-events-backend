from uuid import UUID

from mpu_events.domain.entities.registration import Registration
from mpu_events.domain.exceptions.events.events import EventNotFoundException
from mpu_events.domain.exceptions.events.registrations import RegistrationNotAllowedException, \
    AlreadyRegisteredException
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository
from mpu_events.application.dto.registration_dto import RegistrationResponseDTO


class RegisterForEventUseCase:
    def __init__(self, event_repo: EventRepository, registration_repo: RegistrationRepository):
        self.event_repo = event_repo
        self.registration_repo = registration_repo

    async def execute(self, user_id: UUID, event_id: UUID) -> RegistrationResponseDTO:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise EventNotFoundException()

        if not event.can_register():
            raise RegistrationNotAllowedException()

        existing = await self.registration_repo.get_by_user_and_event(user_id, event_id)
        if existing:
            raise AlreadyRegisteredException()

        await self.event_repo.update(event)

        registration = Registration(user_id=user_id, event_id=event_id)
        created = await self.registration_repo.create(user_id, registration.event_id)

        return RegistrationResponseDTO.model_validate(created)