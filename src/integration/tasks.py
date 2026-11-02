__all__ = ["integrate_tenders_task"]

import asyncio

from integration.bootstrap import get_tender_integration_service
from worker import celery_app


@celery_app.task(name="integration.integrate_tenders")
def integrate_tenders_task() -> None:
    service = get_tender_integration_service()
    asyncio.run(service.integrate())
