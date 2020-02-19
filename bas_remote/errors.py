__all__ = [
    'SocketNotConnectedError',
    'ScriptNotSupportedError',
    'ScriptNotExistError'
]


class BasError(Exception):
    def __init__(self, message=None):
        self.message = message


class SocketNotConnectedError(BasError):
    _message = 'Cannot connect to the WebSocket server'

    def __init__(self):
        super().__init__(self._message)


class ScriptNotSupportedError(BasError):
    _message = 'Script engine not supported (Required 22.4.2 or newer)'

    def __init__(self):
        super().__init__(self._message)


class ScriptNotExistError(BasError):
    _message = 'Script with selected name not exist'

    def __init__(self):
        super().__init__(self._message)


class AuthenticationError(BasError):
    _message = 'Unsuccessful authentication'

    def __init__(self):
        super().__init__(self._message)


class AlreadyRunningError(BasError):
    _message = 'Another task is already running. Unable to start a new one'

    def __init__(self):
        super().__init__(self._message)


class FunctionError(BasError):
    def __init__(self, message):
        super().__init__(message)
