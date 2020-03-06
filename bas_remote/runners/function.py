from random import randint

from bas_remote.errors import FunctionError
from bas_remote.types import Response
from .runner import Runner


class BasFunction(Runner):
    """Basic class for interacting with BAS functions."""

    def __init__(self, client):
        """Create an instance of BasFunction class.

        Args:
            client: Remote client object.
        """
        super().__init__(client)

    async def _run_function(self, function_name: str, function_params: dict, on_result, on_error):
        async def callback(result: str):
            response = Response.from_json(result)
            if not response.success:
                on_error(FunctionError(response.message))
            else:
                on_result(response.result)
            await self.stop()

        self._id = randint(1, 1000000)
        await self._client.start_thread(self.id)

        await self._run_task(function_name, function_params, callback)

    async def stop(self) -> None:
        """Immediately stops function execution."""
        await self._client.stop_thread(self.id)


__all__ = ['BasFunction']
