from mpu_events.domain.interfaces.user_repository import UserRepository
from mpu_events.domain.entities.user import User
from mpu_events.domain.exceptions.users.users import EmailAlreadyExistsException
from mpu_events.application.dto.auth_dto import RegisterUserDTO, UserResponseDTO
from mpu_events.application.services.password_service import PasswordService


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository, password_service: PasswordService):
        self.user_repo = user_repo
        self.password_service = password_service

    async def execute(self, dto: RegisterUserDTO) -> UserResponseDTO:
        existing = await self.user_repo.get_by_email(str(dto.email))
        if existing:
            raise EmailAlreadyExistsException(str(dto.email))

        user = User(
            email=str(dto.email),
            full_name=dto.full_name,
            group_number=dto.group_number,
            hashed_password=self.password_service.hash(dto.password),
        )
        created = await self.user_repo.create(user)
        return UserResponseDTO.model_validate(created)