from fastapi.exceptions import RequestValidationError
from pydantic import ConfigDict
from pydantic.alias_generators import to_pascal
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from api.base.schemas.responses import ErrorAPIResponse, RefinedJSONResponse
from common.errors.errors import BaseValidationError, ValidationErrorSchema


class ValidationErrorResponseSchema(ErrorAPIResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "message": "Дата конца выборки должна быть меньше сегодняшней даты.",
                    "errors": [
                        {
                            "message": "Дата конца выборки должна быть меньше сегодняшней даты.",
                            "location": ("body", "endDate"),
                            "reason": "ValueError",
                        }
                    ],
                },
            }
        }
    )


def setup_validation_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> RefinedJSONResponse:
        messages = [error.get("msg") for error in exc.errors()]
        errors = [
            ValidationErrorSchema(
                location=error.get("loc"),
                message=error.get("msg"),
                reason=to_pascal(error.get("type")),
            )
            for error in exc.errors()
        ]

        msg = " ".join(messages)

        return RefinedJSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=ValidationErrorResponseSchema(
                error=GeneralErrorInformationSchema(
                    message=msg,
                    errors=errors,
                ),
            ).model_dump(by_alias=True),
        )

    @app.exception_handler(BaseValidationError)
    async def custom_validation_exception_handler(
        request: Request,
        exc: BaseValidationError,
    ) -> RefinedJSONResponse:
        return RefinedJSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=ValidationErrorResponseSchema(
                error=GeneralErrorInformationSchema(
                    message=exc.msg,
                    errors=[
                        ValidationErrorSchema(
                            message=exc.msg,
                            location=exc.loc,
                            reason=exc.type,
                        )
                    ],
                ),
            ).model_dump(by_alias=True),
        )
