from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.domain.entities.registration import Registration
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository
from mpu_events.infra.database.models.registration_model import RegistrationModel
from mpu_events.infra.database.mappers.registration_mapper import RegistrationMapper


class SQLAlchemyRegistrationRepository(RegistrationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, event_id: UUID) -> Registration:
        model = RegistrationModel(user_id=user_id, event_id=event_id)
        self.session.add(model)
        await self.session.flush()
        return RegistrationMapper.to_entity(model)

    async def exists(self, user_id: UUID, event_id: UUID) -> bool:
        result = await self.session.execute(
            select(RegistrationModel).where(
                RegistrationModel.user_id == user_id,
                RegistrationModel.event_id == event_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def count_by_event(self, event_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count()).where(RegistrationModel.event_id == event_id)
        )
        return result.scalar_one()

    async def get_by_user(self, user_id: UUID) -> list[Registration]:
        result = await self.session.execute(
            select(RegistrationModel).where(RegistrationModel.user_id == user_id)
        )
        return [RegistrationMapper.to_entity(m) for m in result.scalars().all()]

    async def get_by_user_and_event(self, user_id: UUID, event_id: UUID) -> Registration | None:
        result = await self.session.execute(
            select(RegistrationModel)
            .where(RegistrationModel.user_id == user_id)
            .where(RegistrationModel.event_id == event_id)
        )
        model = result.scalar_one_or_none()
        return RegistrationMapper.to_entity(model) if model else None

    async def delete(self, registration_id: UUID) -> None:
        result = await self.session.execute(
            select(RegistrationModel).where(
                RegistrationModel.id == registration_id,
            )
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()

    async def delete_by_event(self, event_id: UUID) -> None:
        stmt = delete(RegistrationModel).where(RegistrationModel.event_id == event_id)
        await self.session.execute(stmt)
        await self.session.flush()

