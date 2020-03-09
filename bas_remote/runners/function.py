from random import randint
from typing import Optional, Dict

from .runner import BasRunner


class BasFunction(BasRunner):
    """Basic class for interacting with BAS functions."""

    def __init__(self, client, name: str, params: Optional[Dict] = None):
        """Create an instance of BasFunction class.

        Args:
            client: Remote client object.
            name (str): BAS function name as string.
            params (dict, optional): BAS function arguments list. Defaults to None.
        """
        super().__init__(client)
        self._run(name, params)

    async def _run_function(self, name: str, params: Optional[Dict] = None) -> None:
        self._id = randint(1, 1000000)
        await self._client.start_thread(self.id)
        await self._run_task(name, params)
        await self.stop()

    async def stop(self) -> None:
        """Immediately stops function execution."""
        await self._client.stop_thread(self.id)


__all__ = ['BasFunction']
