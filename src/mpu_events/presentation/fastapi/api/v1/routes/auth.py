from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mpu_events.application.dto.auth_dto import RegisterUserDTO, LoginUserDTO, AuthTokenDTO, UserResponseDTO
from mpu_events.application.services.password_service import PasswordService
from mpu_events.application.services.token_service import TokenService
from mpu_events.application.use_cases.auth.register_user import RegisterUserUseCase
from mpu_events.application.use_cases.auth.login_user import LoginUserUseCase
from mpu_events.infra.database.repositories.user_repository import SQLAlchemyUserRepository
from mpu_events.presentation.fastapi.dependencies.db import get_db
from mpu_events.presentation.fastapi.dependencies.auth import get_current_user
from mpu_events.domain.entities.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

password_service = PasswordService()
token_service = TokenService()


@router.post("/register", response_model=UserResponseDTO, status_code=201)
async def register(dto: RegisterUserDTO, session: AsyncSession = Depends(get_db)):
    use_case = RegisterUserUseCase(
        user_repo=SQLAlchemyUserRepository(session),
        password_service=password_service,
    )
    return await use_case.execute(dto)


@router.post("/login", response_model=AuthTokenDTO)
async def login(dto: LoginUserDTO, session: AsyncSession = Depends(get_db)):
    use_case = LoginUserUseCase(
        user_repo=SQLAlchemyUserRepository(session),
        password_service=password_service,
        token_service=token_service,
    )
    return await use_case.execute(dto)


@router.get("/me", response_model=UserResponseDTO)
async def me(current_user: User = Depends(get_current_user)):
    return current_user