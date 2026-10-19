from enum import StrEnum


class HttpMetricsClientType(StrEnum):
    API = "api"
    INTEGRATION = "integration"
    NOTIFICATION = "notification"
