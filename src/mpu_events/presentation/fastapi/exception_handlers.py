from fastapi import FastAPI
from fastapi.responses import JSONResponse

from mpu_events.domain.exceptions.auth import UnauthorizedException
from mpu_events.domain.exceptions.events.events import EventNotFoundException, EventFullException
from mpu_events.domain.exceptions.events.registrations import AlreadyRegisteredException
from mpu_events.domain.exceptions.users.users import UserNotFoundException, EmailAlreadyExistsException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EventNotFoundException)
    async def event_not_found(request, exc):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UserNotFoundException)
    async def user_not_found(request, exc):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(EmailAlreadyExistsException)
    async def email_exists(request, exc):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(AlreadyRegisteredException)
    async def already_registered(request, exc):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(EventFullException)
    async def event_full(request, exc):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized(request, exc):
        return JSONResponse(status_code=401, content={"detail": str(exc)})