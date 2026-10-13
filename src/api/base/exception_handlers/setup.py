from fastapi import FastAPI

from api.base.exception_handlers.errors import setup_unauthorized_exception_handlers
from api.base.exception_handlers.errors.not_found_error import (
    setup_not_found_exception_handler,
)
from api.base.exception_handlers.errors.server_error import (
    setup_server_exception_handlers,
)
from api.base.exception_handlers.errors.unprocessable_entity_error import (
    setup_unprocessable_entity_exception_handler,
)
from api.base.exception_handlers.errors.unsuccessful_request_error import (
    setup_unsuccessful_request_exception_handler,
)
from api.base.exception_handlers.errors.validation_error import (
    setup_validation_exception_handlers,
)


def setup_exception_handlers(app: FastAPI):
    setup_validation_exception_handlers(app)
    setup_server_exception_handlers(app)
    setup_not_found_exception_handler(app)
    setup_unprocessable_entity_exception_handler(app)
    setup_unsuccessful_request_exception_handler(app)
    setup_unauthorized_exception_handlers(app)