import unittest

from bas_remote.types.message import Message


class MessageTestCase(unittest.TestCase):

    def test_message_from_json(self):
        msg = Message(id=1, async_=True, type_='log', data='Hello')
        self.assertEqual(Message.from_json('{"async": true, "type": "log", "id": 1, "data": "Hello"}'), msg)

    def test_message_to_json(self):
        msg = Message(id=1, async_=True, type_='log', data='Hello')
        self.assertEqual(msg.to_json(), '{"async": true, "type": "log", "id": 1, "data": "Hello"}')


if __name__ == '__main__':
    unittest.main()
