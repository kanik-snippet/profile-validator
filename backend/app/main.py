from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controller.server import controller
from app.api.routes import router
from app.core.config import get_settings
from app.core.constants import API_VERSION
from app.core.database import Base, engine
from app.core.http import http_client
from app.core.logger import configure_logger
from app.core.state import application_state


@asynccontextmanager
async def lifespan(_: FastAPI):

    configure_logger()

    # Development only
    Base.metadata.create_all(bind=engine)

    await http_client.startup()

    application_state.initialized = True

    try:
        yield

    finally:

        application_state.initialized = False

        await http_client.shutdown()


app = FastAPI(
    title=get_settings().app_name,
    version=API_VERSION,
    lifespan=lifespan,
)

# Local controller
app.include_router(controller.router)

# REST API
app.include_router(router)