from pydantic import ConfigDict
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from api.base.schemas.responses import ErrorAPIResponse, RefinedJSONResponse
from common.errors.base import ErrorSchema
from common.errors.errors import BaseUnauthorizedError


class UnauthorizedErrorResponseSchema(ErrorAPIResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": HTTP_401_UNAUTHORIZED,
                    "message": "Авторизация не пройдена.",
                    "errors": [
                        {
                            "message": "Авторизация не пройдена.",
                            "type": "UnauthorizedError",
                        }
                    ],
                },
            }
        }
    )


def setup_unauthorized_exception_handlers(app):
    @app.exception_handler(BaseUnauthorizedError)
    async def unauthorized_exception_handler(
        request: Request,
        exc: BaseUnauthorizedError,
    ) -> RefinedJSONResponse:
        return RefinedJSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content=UnauthorizedErrorResponseSchema(
                error=GeneralErrorInformationSchema(
                    code=HTTP_401_UNAUTHORIZED,
                    message=exc.msg,
                    errors=[
                        ErrorSchema(
                            message=exc.msg,
                            reason="UnauthorizedError",
                        )
                    ],
                ),
            ).model_dump(by_alias=True),
        )
