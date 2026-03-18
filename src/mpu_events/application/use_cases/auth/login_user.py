from mpu_events.domain.interfaces.user_repository import UserRepository
from mpu_events.domain.exceptions.auth import UnauthorizedException
from mpu_events.application.dto.auth_dto import LoginUserDTO, AuthTokenDTO
from mpu_events.application.services.password_service import PasswordService
from mpu_events.application.services.token_service import TokenService


class LoginUserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
    ):
        self.user_repo = user_repo
        self.password_service = password_service
        self.token_service = token_service

    async def execute(self, dto: LoginUserDTO) -> AuthTokenDTO:
        user = await self.user_repo.get_by_email(str(dto.email))
        if not user:
            raise UnauthorizedException()

        if not self.password_service.verify(dto.password, user.hashed_password):
            raise UnauthorizedException()

        token = self.token_service.create_access_token(user.id, user.role)
        return AuthTokenDTO(access_token=token)