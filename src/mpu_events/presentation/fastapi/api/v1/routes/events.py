from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.application.dto.event_dto import CreateEventDTO, EventResponseDTO
from mpu_events.application.use_cases.events.create_event import CreateEventUseCase
from mpu_events.application.use_cases.events.get_event import GetEventUseCase
from mpu_events.application.use_cases.events.list_events import ListEventsUseCase
from mpu_events.infra.database.repositories.event_repository import SQLAlchemyEventRepository
from mpu_events.infra.database.repositories.registration_repository import SQLAlchemyRegistrationRepository
from mpu_events.presentation.fastapi.dependencies.db import get_db
from mpu_events.presentation.fastapi.dependencies.auth import get_current_user, get_current_admin
from mpu_events.domain.entities.user import User

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[EventResponseDTO])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    use_case = ListEventsUseCase(
        event_repo=SQLAlchemyEventRepository(session),
        registration_repo=SQLAlchemyRegistrationRepository(session),
    )
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/{event_id}", response_model=EventResponseDTO)
async def get_event(
    event_id: UUID,
    session: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    use_case = GetEventUseCase(
        event_repo=SQLAlchemyEventRepository(session),
        registration_repo=SQLAlchemyRegistrationRepository(session),
    )
    return await use_case.execute(event_id)


@router.post("/", response_model=EventResponseDTO, status_code=201)
async def create_event(
    dto: CreateEventDTO,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    use_case = CreateEventUseCase(event_repo=SQLAlchemyEventRepository(session))
    return await use_case.execute(dto, current_admin.id)