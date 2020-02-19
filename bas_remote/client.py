import asyncio

from bas_remote.options import Options
from .callback import ClientCallback
from .services import EngineService
from .services import SocketService
from typing import Callable, Any
from random import randint
from json import loads

__all__ = ['BasRemoteClient']


class BasRemoteClient():
    """Class that provides methods for remotely interacting with BAS."""

    def __init__(self, options: Options, callback: ClientCallback = None, loop: asyncio.BaseEventLoop = None):
        """Create an instance of BasRemoteClient class.

        Args:
            options (Options): Client options object.
            callback (ClientCallback, optional): Client callback object. Defaults to None.
            loop (asyncio.BaseEventLoop, optional): AsyncIO loop object. Defaults to None.
        """

        self._callback = callback or ClientCallback()
        self._loop = loop or asyncio.get_event_loop()
        self._options = options

        self._engine = EngineService(self)
        self._socket = SocketService(self)

        self._future = asyncio.Future()
        self._requests = {}

    async def _on_message_received(self, message: dict) -> None:
        await self._callback.on_message_received(message)

        msg_type, msg_id = message['type'], message['id']

        if msg_type == 'thread_start' and not self._future.done:
            self._future.set_result(True)

        if msg_type == 'message' and not self._future.done:
            self._future.set_exception(ValueError('message'))

        if msg_type == 'initialize':
            await self.send('accept_resources', {'-bas-empty-script-': True})
        elif message['async'] and msg_id:
            if msg_type == 'get_global_variable':
                func = self._requests.pop(msg_id)
                func(loads(message['data']))
            else:
                func = self._requests.pop(msg_id)
                func(message['data'])

    async def _on_message_sent(self, message: dict) -> None:
        await self._callback.on_message_sent(message)

    async def _on_socket_closed(self) -> None:
        await self._callback.on_socket_closed()

    async def _on_socket_opened(self) -> None:
        await self.send('remote_control_data', {
            'script': self._options.scriptName,
            'password': self._options.password,
            'login': self._options.login,
        })
        await self._callback.on_socket_opened()

    async def send_async(self, message_type: str, params: dict = {}, callback: Callable = None) -> None:
        message_id = await self.send(message_type, params, True)
        self._requests[message_id] = callback

    async def send(self, message_type: str, params: dict = {}, is_async: bool = False) -> int:
        message = new_message(message_type, params, is_async)
        await self._socket.send(message)
        return message['id']

    async def start(self) -> None:
        await self._engine.initialize()

        port = randint(10000, 20000)

        await self._engine.start(port)
        await self._socket.start(port)

        self._loop.create_task(self._listen())

        await self._wait()

    async def _listen(self) -> None:
        try:
            await self._socket.listen()
        except KeyboardInterrupt:
            pass
        finally:
            await self._engine.close()
            await self._socket.close()

    async def _wait(self) -> None:
        future = self._future
        loop = self._loop
        timeout = 60
        await asyncio.wait_for(
            future,
            timeout,
            loop=loop
        )


def new_message(message_type, params, is_async):
    return {
        'id': randint(100000, 999999),
        'type': message_type,
        'async': is_async,
        'data': params
    }
