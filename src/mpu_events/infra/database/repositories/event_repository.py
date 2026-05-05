from datetime import date, datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.domain.entities.event import Event
from mpu_events.domain.exceptions.events.events import EventNotFoundException
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.infra.database.models.event_model import EventModel
from mpu_events.infra.database.mappers.event_mapper import EventMapper


class SQLAlchemyEventRepository(EventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, event_id: UUID) -> Event | None:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        model = result.scalar_one_or_none()
        return EventMapper.to_entity(model) if model else None

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 20,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Event]:
        query = select(EventModel)
        
        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            start_datetime = start_datetime.replace(tzinfo=timezone.utc)
            query = query.where(EventModel.start_time >= start_datetime)
        
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            end_datetime = end_datetime.replace(tzinfo=timezone.utc)
            query = query.where(EventModel.start_time <= end_datetime)
        
        query = query.order_by(EventModel.start_time.asc())
        
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        models = result.scalars().all()
        
        return [EventMapper.to_entity(model) for model in models]

    async def create(self, event: Event) -> Event:
        model = EventMapper.to_model(event)
        self.session.add(model)
        await self.session.flush()
        return EventMapper.to_entity(model)

    async def update(self, event: Event) -> Event:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise EventNotFoundException()

        model.title = event.title
        model.description = event.description
        model.start_time = event.start_time
        model.location = event.location
        model.max_participants = event.max_participants
        await self.session.flush()
        return EventMapper.to_entity(model)

    async def delete(self, event_id: UUID) -> None:
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()