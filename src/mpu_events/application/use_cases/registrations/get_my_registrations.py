from uuid import UUID
from typing import List
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository
from mpu_events.application.dto.registration_dto import RegistrationResponseDTO


class GetMyRegistrationsUseCase:
    def __init__(self, registration_repo: RegistrationRepository):
        self.registration_repo = registration_repo

    async def execute(self, user_id: UUID) -> List[RegistrationResponseDTO]:
        registrations = await self.registration_repo.get_by_user(user_id)

        return [
            RegistrationResponseDTO.model_validate(reg)
            for reg in registrations
        ]