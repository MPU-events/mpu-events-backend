from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.application.dto.event_dto import CreateEventDTO, EventResponseDTO, UpdateEventDTO
from mpu_events.application.use_cases.events.create_event import CreateEventUseCase
from mpu_events.application.use_cases.events.delete_event import DeleteEventUseCase
from mpu_events.application.use_cases.events.get_event import GetEventUseCase
from mpu_events.application.use_cases.events.list_events import ListEventsUseCase
from mpu_events.application.use_cases.events.update_event import UpdateEventUseCase
from mpu_events.domain.exceptions.auth import PermissionDeniedException
from mpu_events.domain.exceptions.events.events import EventNotFoundException
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

@router.put("/{event_id}", response_model=EventResponseDTO)
async def update_event(
    event_id: UUID,
    dto: UpdateEventDTO,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = UpdateEventUseCase(
        event_repo=SQLAlchemyEventRepository(session),
        registration_repo=SQLAlchemyRegistrationRepository(session),
    )
    
    try:
        return await use_case.execute(
            event_id=event_id,
            dto=dto,
            current_user_id=current_user.id,
            is_admin=current_user.is_admin()
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except EventNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteEventUseCase(
        event_repo=SQLAlchemyEventRepository(session),
        registration_repo=SQLAlchemyRegistrationRepository(session),
    )
    
    try:
        await use_case.execute(
            event_id=event_id,
            current_user_id=current_user.id,
            is_admin=current_user.is_admin()
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except EventNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
