import jwt
from datetime import datetime, timedelta, UTC
from uuid import UUID
from mpu_events.config import config
from mpu_events.domain.entities.user import UserRole
from mpu_events.domain.exceptions.auth import UnauthorizedException, JWTExpiresUnauthorizedException, \
    JWTInvalidUnauthorizedException


class TokenService:
    @staticmethod
    def create_access_token(user_id: UUID, role: UserRole) -> str:
        payload = {
            "sub": str(user_id),
            "role": role.value,
            "exp": datetime.now(UTC) + timedelta(
                minutes=config.auth.access_token_expire_minutes
            ),
        }
        return jwt.encode(payload, config.auth.jwt_secret_key, algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, config.auth.jwt_secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise JWTExpiresUnauthorizedException()
        except jwt.InvalidTokenError:
            raise JWTInvalidUnauthorizedException()