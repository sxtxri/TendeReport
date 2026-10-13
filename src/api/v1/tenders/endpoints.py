from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.base.schemas.responses import ErrorAPIResponse, ObjectAPIResponse
from queries.bootstrap import (
    get_tender_service
)
from common.types import TenderId
from queries.entities import Tender
from queries.services import TenderService

tenders_router = APIRouter()


@tenders_router.get(
    "/tenders/{tenderId}",
    summary="Поиск тендера по его идентификатору",
    description="Поиск тендера по его идентификатору",
    responses={
        status.HTTP_200_OK: {"model": ObjectAPIResponse[Tender]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorAPIResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorAPIResponse},
    },
    tags=["Интервалы"],
)
async def find(
    tender_id: TenderId,
    service: Annotated[TenderService, Depends(get_tender_service)],
) -> ObjectAPIResponse[Tender] | ErrorAPIResponse:

    tender: Tender = await service.get_tender(tender_id=tender_id)

    return ObjectAPIResponse(
        data=tender
    )
