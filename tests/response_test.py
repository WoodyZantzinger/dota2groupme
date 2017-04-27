__author__ = 'woodyzantzinger'

import unittest
import bot

msg = """{
  "attachments": [],
  "avatar_url": "http://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id": "16905359",
  "id": "1",
  "name": "Woody",
  "sender_id": "7340477",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": false,
  "text": "#last",
  "user_id": "73450477"
    } """

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        bot.app.config['TESTING'] = True
        self.app = bot.app.test_client()

    def test_hello_world_db(self):
        rv = self.app.get('/')
        assert b'Hello world!' in rv.data

if __name__ == '__main__':
    unittest.main()