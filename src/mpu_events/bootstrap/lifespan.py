from contextlib import asynccontextmanager
from fastapi import FastAPI
from mpu_events.config import config
from mpu_events.infra.database.manager import DatabaseManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DatabaseManager(
        database_url=config.database.dsn,
        echo=config.debug,
    )
    app.state.db = db

    yield

    await db.close()