import asyncio
import unittest

from bas_remote import BasRemoteClient, Options


class BaseTest(unittest.TestCase):
    client = None

    loop = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.loop = asyncio.get_event_loop()
        cls.options = Options(working_dir='../../bas-remote-app',
                              script_name='TestRemoteControl')
        cls.client = BasRemoteClient(cls.options, cls.loop)
        cls.loop.run_until_complete(cls.client.start())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.loop.run_until_complete(cls.client.close())
        cls.loop.close()

    def run_functions(self, runner, x: list, y: list):
        tasks = []
        for i in range(len(x)):
            if isinstance(runner, BasRemoteClient):
                task = get_func(runner, x[i], y[i])
            else:
                task = get_func(runner[i], x[i], y[i])
            tasks.append(task)
        return self.loop.run_until_complete(asyncio.gather(*tasks, loop=self.loop))

    def run_function(self, runner, x: int, y: int):
        return self.loop.run_until_complete(get_func(runner, x, y))

    def run_fail(self, runner, x: int, y: int):
        return self.loop.run_until_complete(get_func(runner, x, y, 'Add1'))


def get_func(runner, x: int, y: int, name: str = 'Add'):
    params = {'X': x, 'Y': y}
    return runner.run_function(name, params)
