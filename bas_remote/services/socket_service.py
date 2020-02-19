import asyncio
import json

from websockets.exceptions import (ConnectionClosedError, ConnectionClosedOK)
from websockets import WebSocketClientProtocol, connect
from bas_remote.errors import SocketNotConnectedError
from .base_service import BaseService

__all__ = ['SocketService']

SEPARATOR = '---Message--End---'


class SocketService(BaseService):
    """Service that provides methods for interacting with BAS socket."""

    def __init__(self, client):
        super().__init__(client)
        self._websocket = None
        self._buffer = ''

    async def _message_received(self, message) -> None:
        buffer = (self._buffer + message).split(SEPARATOR)
        for message in [item for item in buffer if item]:
            unpacked = json.loads(message)
            await self._client._on_message_received(unpacked)
        self._buffer = buffer.pop()

    async def _message_sent(self, message) -> None:
        await self._client._on_message_sent(message)

    async def _closed(self) -> None:
        await self._client._on_socket_closed()

    async def _opened(self) -> None:
        await self._client._on_socket_opened()

    async def start(self, port: int) -> None:
        """Asynchronously start the socket service with the specified port.

        Args:
            port (int): Selected port number.
        """
        attempt = 1
        while not self._websocket or not self._websocket.open:
            try:
                self._websocket = await connect(f'ws://127.0.0.1:{port}')
            except:
                if attempt == 60:
                    raise SocketNotConnectedError()
                await asyncio.sleep(1)
                attempt += 1
        await self._opened()
        await self._listen()

    async def listen(self) -> None:
        while True:
            try:
                message = await self._websocket.recv()
                await self._message_received(message)
            except ConnectionClosedError:
                break
            except ConnectionClosedOK:
                break
        await self._closed()

    async def send(self, message: dict) -> None:
        packet = json.dumps(message) + SEPARATOR
        await self._websocket.send(packet)
        await self._message_sent(message)

    async def close(self) -> None:
        await self._websocket.close()
