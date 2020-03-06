import asyncio

from websockets import WebSocketClientProtocol, connect
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK
)

from bas_remote.errors import SocketNotConnectedError
from bas_remote.types import Message

SEPARATOR = '---Message--End---'


class SocketService:
    """Service that provides methods for interacting with BAS socket."""

    _socket: WebSocketClientProtocol = None

    _buffer: str = ''

    def __init__(self, client):
        """Create an instance of SocketService class."""
        self._emit = client.emit
        self._loop = client.loop

    async def start(self, port: int) -> None:
        """Asynchronously start the socket service with the specified port.

        Arguments:
            port (int): Selected port number.
        """
        attempt = 1
        while not self.is_connected:
            try:
                self._socket = await connect(f'ws://127.0.0.1:{port}', loop=self._loop)
            except ConnectionRefusedError:
                if attempt == 60:
                    raise SocketNotConnectedError()
                await asyncio.sleep(1)
                attempt += 1
        self._opened()

    @property
    def is_connected(self) -> bool:
        return self._socket is not None and self._socket.open

    def _process_data(self, data: str) -> None:
        buffer = (self._buffer + data).split(SEPARATOR)
        for message in [item for item in buffer if item]:
            unpacked = Message.from_json(message)
            self._emit('message_received', unpacked)
        self._buffer = buffer.pop()

    def _closed(self) -> None:
        """Function that is called when the connection is closed."""
        self._emit('socket_close')
        self._loop.create_task(self.close())

    def _opened(self) -> None:
        """Function that is called when the connection is opened."""
        self._emit('socket_open')
        self._loop.create_task(self.listen())

    async def listen(self) -> None:
        while True:
            try:
                data = await self._socket.recv()
                self._process_data(data)
            except ConnectionClosedError:
                break
            except ConnectionClosedOK:
                break
        self._closed()

    async def send(self, message: Message) -> int:
        packet = message.to_json() + SEPARATOR
        await self._socket.send(packet)
        self._emit('message_sent', message)
        return message.id_

    async def close(self) -> None:
        if not self.is_connected:
            return
        await self._socket.close()


__all__ = ['SocketService']
