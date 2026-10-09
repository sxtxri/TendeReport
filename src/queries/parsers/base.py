__all__ = ["BaseParser"]


class BaseParser:
    def __init__(self, client: BaseClient):
        self.client = client

    async def parse(self):
        raise NotImplementedError