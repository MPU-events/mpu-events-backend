from uuid import UUID

from mpu_events.domain.exceptions.base import DomainException


class UserNotFoundException(DomainException):
    def __init__(self, id_uuid: str | UUID):
        super().__init__(f"Пользователь '{id_uuid}' не найден")


class EmailAlreadyExistsException(DomainException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Пользователь с почтой '{email}' уже зарегистрирован")