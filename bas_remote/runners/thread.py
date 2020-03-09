from random import randint
from typing import Optional, Dict

from bas_remote.errors import AlreadyRunningError
from .runner import BasRunner


class BasThread(BasRunner):
    """Basic class for interacting with BAS threads."""

    _is_running: bool = False

    def __init__(self, client):
        """Create an instance of BasThread class.

        Args:
            client: Remote client object.
        """
        super().__init__(client)

    def run_function(self, name: str, params: Optional[Dict] = None):
        """Call the BAS function asynchronously.

        Args:
            name (str): BAS function name as string.
            params (dict, optional): BAS function arguments list. Defaults to None.
        """
        self._run(name, params)
        return self

    async def _run_function(self, name: str, params: Optional[Dict] = None) -> None:
        if self.id and self.is_running:
            raise AlreadyRunningError()

        if not self.id:
            self._id = randint(1, 1000000)
            await self._client.start_thread(self.id)

        self._is_running = True
        await self._run_task(name, params)
        self._is_running = False

    async def stop(self) -> None:
        """Immediately stops thread execution."""
        if self.id:
            await self._client.stop_thread(self.id)

        self._is_running = False
        self._id = 0

    @property
    def is_running(self) -> bool:
        """Check if thread is already busy with running function."""
        return self._is_running


__all__ = ['BasThread']
