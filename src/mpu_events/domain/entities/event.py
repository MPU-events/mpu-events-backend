from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID


@dataclass
class Event:
    title: str
    description: str
    start_time: datetime
    location: str
    created_by: UUID

    id: UUID|None = None
    max_participants: int|None = None
    created_at: datetime|None = None
    current_participants: int = 0

    def __post_init__(self):
        self._validate_start_time()
        self._validate_participants_count()

    def _validate_start_time(self) -> None:
        if not self.start_time:
            return

        start_time_utc = self.start_time.astimezone(timezone.utc)
        now_utc = datetime.now(timezone.utc)

        if start_time_utc < now_utc:
            raise ValueError("Начало мероприятия не может быть в прошедшем времени")

    def _validate_participants_count(self) -> None:
        if self.current_participants < 0:
            raise ValueError("Количество участников не может быть отрицательным")

    def can_register(self) -> bool:
        if self.max_participants is None:
            return True
        return self.current_participants < self.max_participants

    # TODO: убрать вероятно, не знаю понадобится ли вообще
    def is_full(self) -> bool:
        if self.max_participants is None:
            return False
        return self.current_participants >= self.max_participants

    def is_past(self) -> bool:
        return datetime.now(self.start_time.tzinfo) > self.start_time

    def is_upcoming(self) -> bool:
        return datetime.now(self.start_time.tzinfo) < self.start_time