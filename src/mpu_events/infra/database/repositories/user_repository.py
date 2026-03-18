from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.domain.entities.user import User
from mpu_events.domain.exceptions.users.users import UserNotFoundException
from mpu_events.domain.interfaces.user_repository import UserRepository
from mpu_events.infra.database.models.user_model import UserModel
from mpu_events.infra.database.mappers.user_mapper import UserMapper


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def create(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self.session.add(model)
        await self.session.flush()
        return UserMapper.to_entity(model)

    async def update(self, user: User) -> User:
        model = await self.session.get(UserModel, user.id)
        if not model:
            raise UserNotFoundException(user.id)

        model.email = user.email
        model.full_name = user.full_name
        model.group_number = user.group_number
        model.role = user.role


        if user.hashed_password and user.hashed_password != model.hashed_password:
            model.hashed_password = user.hashed_password

        await self.session.flush()
        await self.session.refresh(model)
        return UserMapper.to_entity(model)

    async def delete(self, user_id: UUID) -> None:
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(stmt)
        await self.session.flush()