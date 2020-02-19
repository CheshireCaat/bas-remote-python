
class ClientCallback():

    async def on_message_received(self, message: dict) -> None:
        """Gets called when WebSocket receives new message.

        Args:
            message (dict): message object dictionary.
        """
        pass

    async def on_message_sent(self, message: dict) -> None:
        """Gets called when WebSocket sends new message.

        Args:
            message (dict): message object dictionary.           
        """
        pass

    async def on_socket_closed(self) -> None:
        pass

    async def on_socket_opened(self) -> None:
        pass
