from random import randint

from bas_remote.errors import AlreadyRunningError, FunctionError
from bas_remote.types import Response
from .runner import Runner


class BasThread(Runner):
    """Basic class for interacting with BAS threads."""

    _is_running: bool = False

    def __init__(self, client):
        """Create an instance of BasThread class.

        Args:
            client: Remote client object.
        """
        super().__init__(client)

    @property
    def is_running(self) -> bool:
        """Check if thread is already busy with running function."""
        return self._is_running

    async def _run_function(self, function_name: str, function_params: dict, on_result, on_error):
        async def callback(result: str):
            response = Response.from_json(result)
            self._is_running = False
            if not response.success:
                on_error(FunctionError(response.message))
            else:
                on_result(response.result)

        if self.id and self.is_running:
            raise AlreadyRunningError()

        if not self.id:
            self._id = randint(1, 1000000)
            await self._client.start_thread(self.id)

        await self._run_task(function_name, function_params, callback)
        self._is_running = True

    async def stop(self) -> None:
        """Immediately stops thread execution."""
        if self.id:
            await self._client.stop_thread(self.id)

        self._is_running = False
        self._id = 0


__all__ = ['BasThread']
