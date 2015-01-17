
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

match_performance_template = "As {hero} you went {k}:{d}:{a} with {GPM} GPM finishing at level {level}"

team_template = "The best team ever: {}, {}, {}, {}, {}"

mean_names = ["bitch", "loser", "jabroni", "fudgepacker", "dipshit", "idiot", "assjacker", "axwound", "boner",
                "butt-pirate", "cockface", "dickbag", "fuckstick", "jackass", "muffdiver", "prick", "queef", "rimjob",
                "shitstain", "thundercunt", "unclefucker"]


burn_responses = ["http://media.giphy.com/media/LOVjuAnxaUR6U/giphy.gif",
                    "http://media.giphy.com/media/jAugkVty2VCDu/giphy.gif",
                    "http://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States",
                    "http://www.cabn.ca/en/canadian-burn-units-survivor-support-groups",
                    "https://38.media.tumblr.com/a86240b247fc8a3579fab663a61fec86/tumblr_mi1n1cm5a51rqfhi2o1_500.gif",
                    "http://spaghettiwithcrocetti.files.wordpress.com/2014/07/giphy-51.gif",
                    "http://i489.photobucket.com/albums/rr257/BBladem83/BurnNotice.gif"

                    ]


# mapping of words to notice to responses
# if bot sees a word in the message, it will respond with the easy response
easy_jokes = {"sausage": "but they don''t even have any money"}

def name_to_dotaID(name):
    return int(GroupMetoDOTA[name])


def has_dotaID(name):
    return GroupMetoDOTA.has_key(name)


def has_steamID(name):
    return GroupMetoSteam.has_key(name)


def name_to_steamID(name):
    return int(GroupMetoSteam[name])
