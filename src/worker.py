from celery import Celery

from config import settings
from utils.debug_tools import get_module_name

_MODULE_NAME = get_module_name(__file__)

CELERY_APP_PATH = f"{_MODULE_NAME}:celery_app"


celery_app = Celery(
    settings.SERVICE_NAME,
    broker=settings.celery.BROKER_URL,
    backend=settings.celery.RESULT_BACKEND,
    include=["integration.tasks"],
)

celery_app.conf.update(
    task_track_started=True,
)
