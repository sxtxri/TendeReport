from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from api.base.schemas.responses import (
    ErrorAPIResponse,
    ItemsAPIResponse,
    ObjectAPIResponse,
)
from common.types import TenderId
from queries.bootstrap import get_tender_service
from queries.entities import Tender
from queries.services import TenderService

tenders_router = APIRouter()


@tenders_router.get(
    "/tenders/{tender_id}",
    summary="Поиск тендера по его идентификатору",
    description="Поиск тендера по его идентификатору",
    responses={
        status.HTTP_200_OK: {"model": ObjectAPIResponse[Tender]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorAPIResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorAPIResponse},
    },
    tags=["Тендеры"],
)
async def get_tender(
    tender_id: Annotated[TenderId, Path(description="ID тендера")],
    service: Annotated[TenderService, Depends(get_tender_service)],
) -> ObjectAPIResponse[Tender] | ErrorAPIResponse:

    tender: Tender | None = await service.get_tender(tender_id=tender_id)

    return ObjectAPIResponse(data=tender)


@tenders_router.get(
    "/tenders:find",
    summary="Получение тендеров по фильтрам",
    description="Получение тендеров по фильтрам",
    responses={
        status.HTTP_200_OK: {"model": ItemsAPIResponse[Tender]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorAPIResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorAPIResponse},
    },
    tags=["Тендеры"],
)
async def find_tenders(
    service: Annotated[TenderService, Depends(get_tender_service)],
    city: Annotated[str | None, Query(description="Фильтр по городу проведения тендера")] = None,
    application_deadline_from: Annotated[date | None, Query(description="Срок подачи заявки: начало диапазона")] = None,
    application_deadline_to: Annotated[date | None, Query(description="Срок подачи заявки: конец диапазона")] = None,
    is_price_defined: Annotated[bool | None, Query(description="Фильтр: указана ли цена тендера")] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Количество тендеров на странице")] = 20,
    offset: Annotated[int, Query(ge=0, description="Смещение от начала списка")] = 0,
) -> ItemsAPIResponse[Tender] | ErrorAPIResponse:
    tenders, tenders_count = await service.find_tenders(
        city=city,
        application_deadline_from=application_deadline_from,
        application_deadline_to=application_deadline_to,
        is_price_defined=is_price_defined,
        limit=limit,
        offset=offset,
    )
    return ItemsAPIResponse(
        data={"items": tenders},
        items_per_page=limit,
        start_index=offset,
        total_results=tenders_count,
    )


@tenders_router.get(
    "/cities",
    summary="Поиск всех городов у тендеров",
    description="Поиск всех городов у тендеров",
    responses={
        status.HTTP_200_OK: {"model": ObjectAPIResponse[list[str]]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorAPIResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorAPIResponse},
    },
    tags=["Тендеры"],
)
async def get_cities(
    service: Annotated[TenderService, Depends(get_tender_service)],
) -> ObjectAPIResponse[list[str]] | ErrorAPIResponse:

    cities: list[str] = await service.get_cities()

    return ObjectAPIResponse(data=cities)
