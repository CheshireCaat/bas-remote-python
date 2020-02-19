import asyncio
from .errors import (FunctionError, AlreadyRunningError)


class BasThread():
    """Basic class for interacting with BAS threads."""

    def __init__(self, client):
        self._client = client
        self._running = False
        self._thread_id = 0

    async def run_function(self, function_name: str, function_params: dict = {}):
        future = asyncio.Future()

        if self._thread_id:
            future.set_exception(AlreadyRunningError())
            return future
        if self._running:
            future.set_exception(AlreadyRunningError())
            return future

    async def stop(self) -> None:
        if (self._thread_id):
            await self._client.send('stop_thread', {
                'thread_id': self._thread_id
            })

        self._running = False
        self._thread_id = 0

    @property
    def thread_id(self) -> int:
        return self._thread_id

    @property
    def running(self) -> bool:
        return self._running
