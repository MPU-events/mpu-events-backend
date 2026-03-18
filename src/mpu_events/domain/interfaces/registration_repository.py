from abc import ABC, abstractmethod
from uuid import UUID

from mpu_events.domain.entities.registration import Registration


class RegistrationRepository(ABC):
    @abstractmethod
    async def create(self, user_id: UUID, event_id: UUID) -> Registration: ...

    @abstractmethod
    async def exists(self, user_id: UUID, event_id: UUID) -> bool: ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[Registration]: ...

    @abstractmethod
    async def delete(self, registration_id: UUID) -> None: ...

    @abstractmethod
    async def count_by_event(self, event_id: UUID) -> int: ...

    @abstractmethod
    async def get_by_user_and_event(self, user_id: UUID, event_id: UUID) -> Registration | None: ...