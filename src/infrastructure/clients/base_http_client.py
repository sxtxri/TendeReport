from typing import Any

from httpx import AsyncClient, Request, Response

# часть источников (например, zakupki.gazprom-neft.ru) отдаёт 403,
#   если User-Agent похож на запрос не из браузера
# TODO(sxtxri): переместить куда-то, либо использовать либу для генерации
_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


class MonitoredClientMixin(AsyncClient):
    """
    Http-клиент с телеметрией
    Крайне рекомендуется создавать один экземпляр на хост,
        чтобы использовать пул соединений
    """

    def __init__(self, client_type: Any, *args, **kwargs):
        self._client_type = client_type

        headers = kwargs.pop("headers", None) or {}
        headers.setdefault("User-Agent", _DEFAULT_USER_AGENT)
        kwargs["headers"] = headers

        super().__init__(*args, **kwargs)

    async def send(self, request: Request, *args, **kwargs) -> Response:
        """
        Отправить запрос на источник и обновить метрики запроса, если включены
        :param request: запрос
        :param args:
        :param kwargs:
        :return:
        """
        # TODO(sxtxri): можно добавить сбор метрик по self._client_type, когда появится телеметрия для HTTP-клиентов
        return await super().send(request, *args, **kwargs)
