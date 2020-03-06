import unittest

from bas_remote.types.message import Message


class MessageTestCase(unittest.TestCase):
    test_data = [
        (Message(id_=1, async_=True, type_='log', data='Hello'),
         {"async": True, "type": "log", "id": 1, "data": "Hello"}),
        (Message(id_=1, async_=False, type_='log', data='Hello'),
         {"async": False, "type": "log", "id": 1, "data": "Hello"})
    ]

    def test_message_from_dict(self):
        for i in range(len(self.test_data)):
            with self.subTest(i=i):
                message = self.test_data[i][0]
                dict_ = self.test_data[i][1]
                self.assertEqual(Message.from_dict(dict_), message)

    def test_message_to_dict(self):
        for i in range(len(self.test_data)):
            with self.subTest(i=i):
                message = self.test_data[i][0]
                dict_ = self.test_data[i][1]
                self.assertEqual(message.to_dict(), dict_)


if __name__ == '__main__':
    unittest.main()
