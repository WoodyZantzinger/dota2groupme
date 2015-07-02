# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import steamapi


class ResponseNow(AbstractResponse):

    api = steamapi.core.APIConnection(AbstractResponse.key)

    person_status_template = "{name} : {status}\n"

    RESPONSE_KEY = "#now"

    def __init__(self, msg):
        super(ResponseNow, self).__init__(msg)

    def respond(self):
        out = ""
        for person, steamid in AbstractResponse.GroupMetoSteam.iteritems():
            steamuser = steamapi.user.SteamUser(steamid)

            playing = steamuser.currently_playing
            print(person)
            print(playing)
            if playing:
                game = playing._cache['name'][0]
                out += ResponseNow.person_status_template.format(name=person, status=game)
        if not out:
            return "Nobody's online :("
        return out


