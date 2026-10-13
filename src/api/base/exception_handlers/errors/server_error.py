from asgi_correlation_id import correlation_id
from pydantic import ConfigDict
from starlette import status
from starlette.requests import Request

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from api.base.schemas.responses import ErrorAPIResponse, RefinedJSONResponse
from common.errors.base import ErrorSchema


class ServerErrorResponseSchema(ErrorAPIResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "message": "Документ обработан с ошибкой, обратитесь к разработчикам.",
                    "errors": [
                        {
                            "reason": "ServerError",
                            "message": "Документ обработан с ошибкой, обратитесь к разработчикам.",
                        }
                    ],
                },
            }
        }
    )


def setup_server_exception_handlers(app):
    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def server_exception_handler(
        request: Request,
        exc: Exception,
    ) -> RefinedJSONResponse:

        return RefinedJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServerErrorResponseSchema(
                error=GeneralErrorInformationSchema(
                    message=str(exc),
                    errors=[
                        ErrorSchema(
                            message=str(exc),
                            reason=type(exc).__name__,
                        )
                    ],
                ),
            ).model_dump(by_alias=True),
            headers={"X-Request-ID": correlation_id.get() or ""},
        )
