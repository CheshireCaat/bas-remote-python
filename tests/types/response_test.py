import unittest

from bas_remote.types.response import Response


class ResponseTestCase(unittest.TestCase):
    test_data = [
        (Response(message='Hello', success=True, result=None),
         {"Success": True, "Message": "Hello", "Result": None}),
        (Response(message='Hello', success=False, result=None),
         {"Success": False, "Message": "Hello", "Result": None})
    ]

    def test_response_from_dict(self):
        for i in range(len(self.test_data)):
            with self.subTest(i=i):
                response = self.test_data[i][0]
                dict_ = self.test_data[i][1]
                self.assertEqual(Response.from_dict(dict_), response)

    def test_response_to_dict(self):
        for i in range(len(self.test_data)):
            with self.subTest(i=i):
                response = self.test_data[i][0]
                dict_ = self.test_data[i][1]
                self.assertEqual(response.to_dict(), dict_)


if __name__ == '__main__':
    unittest.main()
