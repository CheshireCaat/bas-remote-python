import aiofiles
import aiohttp
import asyncio
import shutil
import os

from os import path
from zipfile import ZipFile
from subprocess import Popen
from platform import machine
from filelock import FileLock, Timeout
from bas_remote.errors import ScriptNotSupportedError
from bas_remote.errors import ScriptNotExistError
from bas_remote.objects import Script
from .base_service import BaseService


__all__ = ['EngineService']

ENDPOINT = 'https://bablosoft.com'


class EngineService(BaseService):
    """Service that provides methods for interacting with BAS engine."""

    def __init__(self, client):
        super().__init__(client)
        self.scriptName = client._options.scriptName
        self.workingDir = client._options.workingDir

        self.scriptDir = path.join(self.workingDir, "run", self.scriptName)
        self.engineDir = path.join(self.workingDir, "engine")

    async def start(self, port: int) -> None:
        """Asynchronously start the engine service with the specified port.

        Args:
            port (int): Selected port number.
        """

        zipName, urlName = get_names()

        zipPath = path.join(self.zipDir, f'{zipName}.zip')

        if not path.exists(self.zipDir):
            os.makedirs(self.zipDir)
            await self._download(zipPath, zipName, urlName)

        if not path.exists(self.exeDir):
            os.makedirs(self.exeDir)
            await self._extract(zipPath)

        self._start_engine_process(port)
        self._clear_run_directory()

    async def initialize(self):
        url = f'{ENDPOINT}/scripts/{self.scriptName}/properties'

        async with aiohttp.ClientSession(loop=self._loop) as session:
            async with session.get(url) as response:
                script = Script(await response.json())

        if not script.is_exist:
            raise ScriptNotExistError()

        if not script.is_supported:
            raise ScriptNotSupportedError()

        self.zipDir = path.join(self.engineDir, script.engine_version)
        self.exeDir = path.join(self.scriptDir, script.hash[0:5])

    async def _download(self, zipPath: str, zipName: str, urlName: str) -> None:
        url = f'{ENDPOINT}/distr/{urlName}/{path.basename(self.zipDir)}/{zipName}.zip'

        async with aiohttp.ClientSession(loop=self._loop) as session:
            async with session.get(url) as response:
                async with aiofiles.open(zipPath, 'wb') as file:
                    while True:
                        chunk = await response.content.read(1024 * 16)
                        if not chunk:
                            break
                        await file.write(chunk)
                    return await response.release()

    async def _extract(self, zipPath: str) -> None:
        # TODO: aiozipstream
        with ZipFile(zipPath, 'r') as file:
            async def coro(member): 
                file.extract(member, self.exeDir, None)

            tasks = [self._loop.create_task(coro(member))
                     for member in file.namelist()]
            await self._loop.wait(tasks)

    def _start_engine_process(self, port: int):
        self._process = Popen(
            [
                path.join(self.exeDir, 'FastExecuteScript.exe'),
                f'--remote-control-port={port}',
                f'--remote-control'
            ],
            cwd=self.exeDir)
        lock = path.join(self.exeDir, '.lock')
        self._lock = FileLock(lock)
        self._lock.acquire()

    def _clear_run_directory(self):
        for name in os.listdir(self.scriptDir):
            name = path.join(self.scriptDir, name)
            file = path.join(name, '.lock')
            if not path.isfile(name):
                if not is_locked(file):
                    shutil.rmtree(name)

    async def close(self) -> None:
        self._process.kill()
        self._lock.release()


def is_locked(path):
    try:
        with FileLock(path, timeout=0.5) as lock:
            with lock.acquire():
                return False
    except Timeout:
        return True


def get_names():
    arch = 64 if machine().endswith('64') else 32
    zip_name = f'FastExecuteScriptProtected.x{arch}'
    url_name = f'FastExecuteScriptProtected{arch}'
    return zip_name, url_name
