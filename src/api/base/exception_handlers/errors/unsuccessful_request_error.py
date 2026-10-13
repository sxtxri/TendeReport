__all__ = ["setup_unsuccessful_request_exception_handler"]

import json

from pydantic import ConfigDict
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from api.base.schemas.responses import ErrorAPIResponse, RefinedJSONResponse
from common.errors.base import ErrorSchema
from infrastructure.clients.errors import UnSuccessfulRequestError


class UnSuccessfulRequestErrorResponseSchema(ErrorAPIResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "message": "Логическая ошибка.",
                    "errors": [
                        {
                            "message": "Логическая ошибка.",
                            "reason": "BaseUnprocessableEntityError",
                        }
                    ],
                    "service": "Сервис, источник ошибки.",
                },
            }
        }
    )


def setup_unsuccessful_request_exception_handler(app):
    @app.exception_handler(UnSuccessfulRequestError)
    async def unsuccessful_request_exception_handler(
        request: Request,
        exc: UnSuccessfulRequestError,
    ) -> RefinedJSONResponse:
        try:
            json_msg = json.loads(exc.msg)
            if exc.service:
                json_msg["service"] = exc.service
            return RefinedJSONResponse(status_code=exc.status_code, content=json_msg)
        except json.JSONDecodeError:
            return RefinedJSONResponse(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                content=UnSuccessfulRequestErrorResponseSchema(
                    error=GeneralErrorInformationSchema(
                        message="UnSuccessfulRequestError",
                        errors=[
                            ErrorSchema(
                                message=(
                                    exc.msg[-100:] if len(exc.msg) >= 100 else exc.msg
                                ),
                                reason="UnprocessableEntityError",
                            )
                        ],
                        service=getattr(exc, "service", None),
                    ),
                ).model_dump(by_alias=True),
            )
