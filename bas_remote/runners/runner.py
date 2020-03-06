import asyncio
import json
from typing import Optional, Dict


class Runner:
    _future: asyncio.Future = None
    """Future object for function execution."""

    _id: int = 0
    """Current thread id."""

    def __init__(self, client):
        """Create an instance of Runner class.

        Args:
            client: Remote client object.
        """
        self._loop = client.loop
        self._client = client

    @property
    def id(self) -> int:
        """Gets current thread id."""
        return self._id

    async def run_function(self, name: str, params: Optional[Dict] = None) -> asyncio.Future:
        """Call the BAS function asynchronously.

        Args:
            name (str): BAS function name as string.
            params (dict, optional): BAS function arguments list. Defaults to None.
        """
        self._future = asyncio.Future(loop=self._loop)
        await self._run_function(
            name=name,
            params=params,
            on_result=lambda result: self._future.set_result(result),
            on_error=lambda error: self._future.set_exception(error)
        )
        return await self._future

    async def _run_function(self, name: str, params: dict, on_result, on_error):
        """Call the BAS function asynchronously.

        Args:
            name (str): BAS function name as string.
            params (dict): BAS function arguments list.
            on_result: [description]
            on_error: [description]
        """
        pass

    async def _run_task(self, name: str, params: dict, callback):
        """Run the BAS task asynchronously.

        Args:
            name (str): BAS function name as string.
            params (dict): BAS function arguments list.
            callback: Function that will be executed after receiving the result.
        """
        await self._client.send_async('run_task', {
            'params': json.dumps(params),
            'function_name': name,
            'thread_id': self.id
        }, callback)

    async def stop(self) -> None:
        """Immediately stops runner execution."""
        pass


__all__ = ['Runner']
