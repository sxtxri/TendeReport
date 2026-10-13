from typing import Any

from httpx import AsyncClient, Request, Response


class MonitoredClientMixin(AsyncClient):
    """
    Http-клиент с телеметрией
    Крайне рекомендуется создавать один экземпляр на хост,
        чтобы использовать пул соединений
    """

    def __init__(self, client_type: Any, *args, **kwargs):
        self._client_type = client_type
        super().__init__(*args, **kwargs)

    async def send(self, request: Request, *args, **kwargs) -> Response:
        """
        Отправить запрос на источник и обновить метрики запроса, если включены
        :param request: запрос
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError
