import asyncio

from bas_remote.options import Options
from .callback import ClientCallback
from .services import EngineService
from .services import SocketService
from typing import Callable, Optional
from typing import Dict
from inspect import getfullargspec
from random import randint
from json import loads

__all__ = ['BasRemoteClient']


class BasRemoteClient():
    """Class that provides methods for remotely interacting with BAS."""

    _def_requests: Dict[int, Callable] = {}

    _arg_requests: Dict[int, Callable] = {}

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

    async def _on_message_received(self, message: dict) -> None:
        await self._callback.on_message_received(message)

        msg_type, msg_id = message['type'], message['id']

        if msg_type == 'thread_start' and not self._future.done():
            self._future.set_result(True)

        if msg_type == 'message' and not self._future.done():
            self._future.set_exception(ValueError('message'))

        if msg_type == 'initialize':
            await self.send('accept_resources', {'-bas-empty-script-': True})
        elif message['async'] and msg_id:
            if msg_id in self._arg_requests:
                func = self._arg_requests.pop(msg_id)
                func(message['data'])
            if msg_id in self._def_requests:
                func = self._def_requests.pop(msg_id)
                func()

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

    async def send_async(self, message_type: str, params: dict = {}, callback: Optional[Callable] = None) -> None:
        message_id = await self.send(message_type, params, True)
        if callback and args_len(callback) == 1:
            self._arg_requests[message_id] = callback
            return
        if callback and args_len(callback) == 0:
            self._def_requests[message_id] = callback
            return

    async def send(self, message_type: str, params: dict = {}, is_async: bool = False) -> int:
        """Send the custom message and get message id as result.

        Args:
            message_type (str): [description]
            params (dict, optional): [description]. Defaults to {}.
            is_async (bool, optional): [description]. Defaults to False.

        Returns:
            int: message id number.
        """
        message = new_message(message_type, params, is_async)
        await self._socket.send(message)
        return message['id']

    async def start(self) -> None:
        """Start the client and wait for it initialize."""
        await self._engine.initialize()

        port = randint(10000, 20000)

        await self._engine.start(port)
        await self._socket.start(port)

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


def args_len(func):
    return len(getfullargspec(func).args)
