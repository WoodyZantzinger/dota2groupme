__author__ = 'woodyzantzinger'

import unittest
import logging
import sys
import json

import bot

#

MSG_TEMPLATE = {
  "attachments": [],
  "avatar_url":  "http://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id":  "16705359",
  "id":  "1",
  "name": "Woody",
  "sender_id": "7340477",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": False,
  "text": "#?",
  "user_id": "7340477"
    }

RESPONSES_CACHE = []

class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = bot.app.test_client()

    def setUp(self):
        #do nothing right now
        logging.info("Running new test")

    def test_hello_world(self):
        rv = self.app.get('/')
        assert b'Hello world!' in rv.data

    def test_not_sUN(self):
        test_msg = dict(MSG_TEMPLATE)
        test_msg["name"] = "sUN"
        test_msg["user_id"] = "219313"
        test_msg["sender_id"] = "219313"
        test_msg["text"] = "#?"
        result = self.app.post('/message/', data=json.dumps(test_msg), content_type='application/json')
        assert 'No Response' in result.data



def test_responses_generator(msg):
    def test(self):
        test_msg = dict(MSG_TEMPLATE)
        logging.debug(u"Testing Responses")
        test_msg["text"] = msg
        result = self.app.post('/message/', data=json.dumps(test_msg), content_type='application/json')
        logging.debug(u"Testing: {0} \t\t got \t '{1}'".format(res.RESPONSE_KEY, result.data))
        assert "OK - Response Sent" in result.data

    return test

if __name__ == '__main__':
    print("Spa")

    bot.app.config['TESTING'] = True
    bot.DEBUG = True
    bot.set_debug(True)
    bot.load_responses()

    for res in bot.RESPONSES_CACHE:
        if res.RESPONSE_KEY != "\0":
            print("xx")
            test_name = 'test_%s' % str(res).split(".")[2]
            test_name = filter(str.isalnum, test_name)
            test = test_responses_generator(res.RESPONSE_KEY)
            setattr(FlaskTestCase, test_name, test)

    unittest.main()

