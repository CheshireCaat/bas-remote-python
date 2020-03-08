import unittest

from bas_remote.errors import FunctionError
from .base import BaseTest
from .helpers import *


class ClientTestCase(BaseTest):

    def test_parallel_function_run(self):
        x, y = generate_pairs()

        result = self.run_functions(self.client, x, y)
        expected = [i + j for i, j in zip(x, y)]
        self.assertEqual(result, expected)

    def test_multiple_function_run(self):
        x, y = generate_pairs()

        for i in range(len(x)):
            with self.subTest(x=x[i], y=y[i]):
                result = self.run_function(self.client, x[i], y[i])
                self.assertEqual(result, x[i] + y[i])

    def test_not_existing_function_run(self):
        x, y = generate_pair()

        with self.subTest(x=x, y=y):
            with self.assertRaises(FunctionError):
                self.run_fail(self.client, x, y)

    def test_function_run(self):
        x, y = generate_pair()

        result = self.run_function(self.client, x, y)
        self.assertEqual(result, x + y)


if __name__ == '__main__':
    unittest.main()
