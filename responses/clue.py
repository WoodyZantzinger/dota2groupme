# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import random

things = []
with open(os.path.join("utils", "things.txt")) as f:
    things = [line.rstrip('\n') for line in f]

places = []
with open(os.path.join("utils", "places.txt")) as f:
    places = [line.rstrip('\n') for line in f]

people = []
for person, steamid in AbstractResponse.GroupMetoSteam.iteritems():
    people.append(person)


class ResponseClue(ResponseCooldown):

    RESPONSE_KEY = "#clue"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseClue, self).__init__(msg, self.__module__, ResponseClue.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            outwho = random.choice(people)
            outwhat = random.choice(things)
            outwhere = random.choice(places)
            out = "%s with the %s in the %s." % (outwho, outwhat, outwhere)
            self.note_response(out)
            return out
        else:
            print("not responding to #clue because sender {} is on cooldown".format(self.msg.name))