from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from mpu_events.application.dto.registration_dto import RegistrationResponseDTO
from mpu_events.application.use_cases.registrations.register_for_event import RegisterForEventUseCase
from mpu_events.application.use_cases.registrations.cancel_registration import CancelRegistrationUseCase
from mpu_events.application.use_cases.registrations.get_my_registrations import GetMyRegistrationsUseCase
from mpu_events.infra.database.repositories.event_repository import SQLAlchemyEventRepository
from mpu_events.infra.database.repositories.registration_repository import SQLAlchemyRegistrationRepository
from mpu_events.presentation.fastapi.dependencies.db import get_db
from mpu_events.presentation.fastapi.dependencies.auth import get_current_user
from mpu_events.domain.entities.user import User

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.post("/{event_id}", response_model=RegistrationResponseDTO, status_code=201)
async def register_for_event(
    event_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = RegisterForEventUseCase(
        event_repo=SQLAlchemyEventRepository(session),
        registration_repo=SQLAlchemyRegistrationRepository(session),
    )
    return await use_case.execute(current_user.id, event_id)


@router.delete("/{event_id}", status_code=204)
async def cancel_registration(
    event_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = CancelRegistrationUseCase(
        registration_repo=SQLAlchemyRegistrationRepository(session),
        event_repo=SQLAlchemyEventRepository(session)
    )
    await use_case.execute(current_user.id, event_id)


@router.get("/me", response_model=list[RegistrationResponseDTO])
async def my_registrations(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = GetMyRegistrationsUseCase(
        registration_repo=SQLAlchemyRegistrationRepository(session),
    )
    return await use_case.execute(current_user.id)