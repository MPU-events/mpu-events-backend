import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"


@dataclass
class User:
    email: str
    full_name: str
    hashed_password: str

    group_number: str | None = None
    role: UserRole = UserRole.STUDENT
    id: uuid.UUID | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self._validate_email()
        self._validate_full_name()

    def _validate_email(self) -> None:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
            raise ValueError(f"Некорректный email: {self.email}")

    def _validate_full_name(self) -> None:
        if not self.full_name or len(self.full_name.strip()) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def can_create_event(self) -> bool:
        return self.role == UserRole.ADMIN