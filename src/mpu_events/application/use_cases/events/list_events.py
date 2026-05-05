from mpu_events.application.dto.event_dto import EventFilterDTO, EventResponseDTO
from mpu_events.domain.interfaces.event_repository import EventRepository
from mpu_events.domain.interfaces.registration_repository import RegistrationRepository


class ListEventsUseCase:
    def __init__(
        self, 
        event_repo: EventRepository, 
        registration_repo: RegistrationRepository
    ):
        self.event_repo = event_repo
        self.registration_repo = registration_repo

    async def execute(self, filters: EventFilterDTO) -> list[EventResponseDTO]:
        events = await self.event_repo.get_all(
            skip=filters.skip,
            limit=filters.limit,
            start_date=filters.start_date,
            end_date=filters.end_date,
        )
        
        result = []
        for event in events:
            count = await self.registration_repo.count_by_event(event.id)
            result.append(EventResponseDTO.model_validate({
                **event.__dict__,
                "current_participants": count,
            }))
        return result