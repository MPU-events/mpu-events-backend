from mpu_events.domain.exceptions.base import DomainException


class AlreadyRegisteredException(DomainException):
    def __init__(self):
        super().__init__("Вы уже зарегистрированы на данное мероприятие")

class RegistrationNotAllowedException(DomainException):
    def __init__(self):
        super().__init__("Нельзя зарегистрироваться на это мероприятие")

class RegistrationNotFoundException(DomainException):
    def __init__(self):
        super().__init__("Нельзя отменить регистрацию на мероприятие, на которое вы не регистрировались")