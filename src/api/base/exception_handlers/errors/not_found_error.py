from pydantic import ConfigDict
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from api.base.schemas.responses import ErrorAPIResponse, RefinedJSONResponse
from common.errors.base import ErrorSchema
from common.errors.errors import BaseNotFoundError


class NotFoundErrorResponseSchema(ErrorAPIResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "message": "Запись не найдена.",
                    "errors": [
                        {
                            "message": "Запись не найдена.",
                            "reason": "NotFoundError",
                        }
                    ],
                },
            }
        }
    )


def setup_not_found_exception_handler(app):
    @app.exception_handler(BaseNotFoundError)
    async def not_found_exception_handler(
        request: Request,
        exc: BaseNotFoundError,
    ) -> RefinedJSONResponse:

        return RefinedJSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content=NotFoundErrorResponseSchema(
                error=GeneralErrorInformationSchema(
                    message=exc.msg,
                    errors=[
                        ErrorSchema(
                            message=exc.msg,
                            reason="NotFoundError",
                        )
                    ],
                ),
            ).model_dump(by_alias=True),
        )
