import json
from asyncio import Future, AbstractEventLoop
from typing import Optional, Dict

from bas_remote.errors import FunctionError
from bas_remote.types import Response


class BasRunner:
    _loop: AbstractEventLoop = None

    _future: Future = None

    _id: int = 0

    def __init__(self, client):
        """Create an instance of Runner class.

        Args:
            client: Remote client object.
        """
        self._loop = client.loop
        self._client = client

    def __await__(self):
        return self._future.__await__()

    def _run(self, name: str, params: Optional[Dict] = None):
        self._future = self._loop.create_future()
        task = self._run_function(name, params)
        self._loop.create_task(task)

    async def _run_function(self, name: str, params: Optional[Dict] = None):
        """Run the BAS function asynchronously.

        Args:
            name (str): BAS function name as string.
            params (dict, optional): BAS function arguments list.
        """
        pass

    async def _run_task(self, name: str, params: Optional[Dict] = None):
        """Run the BAS task asynchronously.

        Args:
            name (str): BAS function name as string.
            params (dict, optional): BAS function arguments list.
        """
        result = await self._client.send_async('run_task', {
            'params': json.dumps(params if params else {}),
            'function_name': name,
            'thread_id': self.id
        })
        response = Response.from_json(result)
        if response.success:
            self._future.set_result(response.result)
        else:
            exception = FunctionError(response.message)
            self._future.set_exception(exception)

    @property
    def id(self) -> int:
        """Gets current thread id."""
        return self._id


__all__ = ['BasRunner']
