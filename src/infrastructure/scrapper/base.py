__all__ = ["Scrapper"]


class Scrapper:
    def __init__(self, client):
        self.client = client

    async def parse(self):
        raise NotImplementedError
