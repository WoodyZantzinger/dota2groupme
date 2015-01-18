class AbstractResponse(object):

    # default response key
    # should respond to no messages
    RESPONSE_KEY = "\0"

    # priority of message overriding other messsages
    # to allow some things to make others not come through the pipe
    OVERRIDE_PRIORITY = -1

    # default help response
    HELP_RESPONSE = "Not implemented for " + RESPONSE_KEY

    GroupMetoSteam = {
          'Woody Zantzinger': 76561197990341684,
          'Andy Esposito': 76561198044654320,
          'Sty': 76561198038745659,
          'Armadilldo': 76561198067289145,
          'Matthew': 76561198079784406,
          'Kevin': 76561198097020021,
          'Jonny G': 76561198025357651,
    }

    GroupMetoDOTA = {
        'Woody Zantzinger': 30075956,
        'Andy Esposito': 84388592,
        'Sty': 78479931,
        'Armadilldo': 107023417,
        'Matthew': 119518678,
        'Kevin': 136754293,
        'Jonny G': 65091923,
    }

    key =  "63760574A669369C2117EA4A30A4768B"

    @classmethod
    def name_to_dotaID(cls, name):
        return int(AbstractResponse.GroupMetoDOTA[name])

    @classmethod
    def has_dotaID(cls, name):
        return AbstractResponse.GroupMetoDOTA.has_key(name)

    @classmethod
    def has_steamID(cls, name):
        return AbstractResponse.GroupMetoSteam.has_key(name)

    @classmethod
    def name_to_steamID(cls, name):
        return int(AbstractResponse.GroupMetoSteam[name])



    def __init__(self, msg, sender):
        super(AbstractResponse, self).__init__()
        self.msg = msg
        self.sender = sender

    def respond(self):
        return None

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        if cls.RESPONSE_KEY in msg.lower():
            return True
        else:
            return False


if __name__ == "__main__":
    mg = AbstractResponse("#text", "sty")
    print(AbstractResponse.is_relevant_msg("hello", "sty"))