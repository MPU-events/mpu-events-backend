from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.application.services.token_service import TokenService
from mpu_events.domain.entities.user import User, UserRole
from mpu_events.domain.exceptions.exceptions import UnauthorizedException
from mpu_events.infra.database.repositories.user_repository import SQLAlchemyUserRepository
from mpu_events.presentation.fastapi.dependencies.db import get_db

bearer_scheme = HTTPBearer()
token_service = TokenService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    payload = token_service.decode_token(credentials.credentials)
    user_id = UUID(payload["sub"])

    repo = SQLAlchemyUserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise UnauthorizedException("User not found")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    #TODO: реализовать, для mvp без админов
    #if not current_user.is_admin():
    #    raise UnauthorizedException("Admin access required")
    return current_user