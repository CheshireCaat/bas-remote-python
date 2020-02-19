class BaseService(object):
    """Base service class."""

    def __init__(self, client):
        self._loop = client._loop
        self._client = client

    async def start(self, port: int) -> None:
        pass

    def close(self) -> None:
        pass
