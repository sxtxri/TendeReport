from fastapi import FastAPI

from api.base.exception_handlers.setup import setup_exception_handlers
from api.router import main_router
from config import settings
from utils.debug_tools import get_module_name
from utils.worker import run_worker

description = "Сервис подбора тендеров"

_MODULE_NAME = get_module_name(__file__)

API_APP_PATH = f"{_MODULE_NAME}:app"


app = FastAPI(
    title=settings.SERVICE_NAME,
    description=description,
    responses={
        "4XX": {},
        # Костыль чтобы в доку не добавлялась дефолтная 422, уберём этот статус
        # ниже в customize_openapi.
    },
    debug=settings.DEBUG,
)

setup_exception_handlers(app)

# routers
app.include_router(main_router)


if __name__ == "__main__":
    run_worker(
        fast_api_app_path=API_APP_PATH,
        default_host=settings.server.host,
        default_port=settings.server.port,
    )
