import unittest

from bas_remote.errors import FunctionError
from .base import BaseTest
from .helpers import *


class ThreadTestCase(BaseTest):

    def test_parallel_function_run(self):
        threads = create_threads(self.client)
        x, y = generate_pairs()

        result = self.run_functions(threads, x, y)
        expected = [i + j for i, j in zip(x, y)]
        self.assertEqual(result, expected)
        self.assertThreads(threads)

    def test_multiple_function_run(self):
        threads = create_threads(self.client)
        x, y = generate_pairs()

        for i in range(len(x)):
            with self.subTest(x=x[i], y=y[i]):
                result = self.run_function(threads[i], x[i], y[i])
                self.assertEqual(result, x[i] + y[i])
        self.assertThreads(threads)

    def test_not_existing_function_run(self):
        thread = self.client.create_thread()
        x, y = generate_pair()

        with self.subTest(x=x, y=y):
            with self.assertRaises(FunctionError):
                self.run_fail(thread, x, y)
        self.assertThread(thread)

    def test_function_run(self):
        thread = self.client.create_thread()
        x, y = generate_pair()

        result = self.run_function(thread, x, y)
        self.assertEqual(result, x + y)
        self.assertThread(thread)

    def assertThreads(self, threads):
        for thread in threads:
            self.assertThread(thread)

    def assertThread(self, thread):
        self.loop.run_until_complete(thread.stop())
        self.assertFalse(thread.is_running)
        self.assertTrue(thread.id == 0)


if __name__ == '__main__':
    unittest.main()
