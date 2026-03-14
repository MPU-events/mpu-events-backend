from fastapi import FastAPI
from mpu_events.bootstrap.lifespan import lifespan
from mpu_events.bootstrap.router_setup import setup_routers
from mpu_events.bootstrap.exception_setup import setup_exceptions
from mpu_events.config import config


def create_app() -> FastAPI:
    app = FastAPI(
        title=config.project_name,
        version=config.version,
        lifespan=lifespan,
    )
    setup_routers(app)
    setup_exceptions(app)
    return app