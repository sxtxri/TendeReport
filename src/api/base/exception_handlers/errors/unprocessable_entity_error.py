__all__ = [
    "UnprocessableEntityErrorResponseSchema",
    "setup_unprocessable_entity_exception_handler",
]

from pydantic import ConfigDict
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from api.base.schemas.responses import ErrorAPIResponse, RefinedJSONResponse
from common.errors.base import ErrorSchema
from common.errors.errors import BaseUnprocessableEntityError


class UnprocessableEntityErrorResponseSchema(ErrorAPIResponse):
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
                },
            }
        }
    )


def setup_unprocessable_entity_exception_handler(app):
    @app.exception_handler(BaseUnprocessableEntityError)
    async def unprocessable_entity_exception_handler(
        request: Request,
        exc: BaseUnprocessableEntityError,
    ) -> RefinedJSONResponse:

        return RefinedJSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content=UnprocessableEntityErrorResponseSchema(
                error=GeneralErrorInformationSchema(
                    message=exc.msg,
                    errors=[
                        ErrorSchema(
                            message=exc.msg,
                            reason="UnprocessableEntityError",
                        )
                    ],
                ),
            ).model_dump(by_alias=True),
        )
