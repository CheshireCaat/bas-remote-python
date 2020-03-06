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

    async def run_function(self, function_name: str, function_params: Optional[Dict] = None) -> asyncio.Future:
        """Call the BAS function asynchronously.

        Args:
            function_name (str): BAS function name as string.
            function_params (dict, optional): BAS function arguments list. Defaults to None.
        """
        self._future = asyncio.Future(loop=self._loop)
        await self._run_function(
            function_name=function_name,
            function_params=function_params,
            on_result=lambda result: self._future.set_result(result),
            on_error=lambda error: self._future.set_exception(error)
        )
        return await self._future

    async def _run_function(self, function_name: str, function_params: dict, on_result, on_error):
        """Call the BAS function asynchronously.

        Args:
            function_name (str): BAS function name as string.
            function_params (dict): BAS function arguments list.
            on_result: [description]
            on_error: [description]
        """
        pass

    async def _run_task(self, function_name: str, function_params: dict, callback):
        """Run the BAS task asynchronously.

        Args:
            function_name (str): BAS function name as string.
            function_params (dict): BAS function arguments list.
            callback: Function that will be executed after receiving the result.
        """
        await self._client.send_async('run_task', {
            'params': json.dumps(function_params),
            'function_name': function_name,
            'thread_id': self.id
        }, callback)

    async def stop(self) -> None:
        """Immediately stops runner execution."""
        pass


__all__ = ['Runner']
