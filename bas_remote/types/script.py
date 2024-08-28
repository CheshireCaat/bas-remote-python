from packaging.version import Version


class Script:
    supported_version = '22.4.2'

    def __init__(self, data):
        self._data = data

    @property
    def engine_version(self) -> str:
        return self._data['engversion']

    @property
    def is_supported(self) -> bool:
        if not self.engine_version:
            return False

        supported = Version(self.supported_version)
        engine = Version(self.engine_version)
        return engine >= supported

    @property
    def is_exist(self) -> bool:
        return self._data['success']

    @property
    def is_free(self) -> bool:
        return self._data['free']

    @property
    def hash(self) -> str:
        return self._data['hash']


__all__ = ['Script']
