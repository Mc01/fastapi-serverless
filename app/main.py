from fastapi import FastAPI

from .urls import router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


api = get_application()
