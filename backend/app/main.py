from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.constants import API_VERSION
from app.core.database import Base, engine
from app.core.logger import configure_logger
from app.core.state import application_state


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logger()
    Base.metadata.create_all(bind=engine)
    application_state.initialized = True
    try:
        yield
    finally:
        application_state.initialized = False


app = FastAPI(title=get_settings().app_name, version=API_VERSION, lifespan=lifespan)
app.include_router(router)
