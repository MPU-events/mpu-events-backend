from uuid import UUID

from mpu_events.domain.exceptions.base import DomainException


class EventNotFoundException(DomainException):
    def __init__(self):
        super().__init__(f"Мероприятие не найдено")

class EventFullException(DomainException):
    def __init__(self):
        super().__init__("На данное мероприятие больше нет мест")