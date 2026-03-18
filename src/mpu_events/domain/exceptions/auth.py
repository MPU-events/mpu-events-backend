from mpu_events.domain.exceptions.base import DomainException


class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Ошибка авторизации"):
        super().__init__(message)


class JWTExpiresUnauthorizedException(UnauthorizedException):
    def __init__(self):
        super().__init__("Срок действия токена авторизации истек")


class JWTInvalidUnauthorizedException(UnauthorizedException):
    def __init__(self):
        super().__init__("Невалидный токен авторизации")