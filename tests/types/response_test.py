import unittest

from bas_remote.types.response import Response


class ResponseTestCase(unittest.TestCase):

    def test_response_from_json(self):
        resp = Response(message='Hello', success=True, result=None)
        self.assertEqual(Response.from_json('{"Success": true, "Message": "Hello", "Result": null}'), resp)

    def test_response_to_json(self):
        resp = Response(message='Hello', success=True, result=None)
        self.assertEqual(resp.to_json(), '{"Success": true, "Message": "Hello", "Result": null}')


if __name__ == '__main__':
    unittest.main()
