# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random


class ResponseNutted(ResponseCooldown):

    RESPONSE_KEY = "#nutted"

    HELP_RESPONSE = "Sends a nutted"

    COOLDOWN = 1 * 60 * 60 / 4

    nutted_responses = ["http://i.imgur.com/PytWiWF.gif",
			"https://i.imgur.com/GysC7A7.jpg",
			"http://i.imgur.com/op9PWrr.gif",
			"http://38.media.tumblr.com/b9b77be967bf161e4a6b1b18b2c62ff5/tumblr_natck3oNET1s373hwo1_400.gif",
			"http://www.reactiongifs.com/wp-content/uploads/2012/11/spidermanlol.gif",
			"http://i.imgur.com/IDJyi9y.gif",
			"http://i.imgur.com/Hx27goS.gif",
			"http://i.imgur.com/jAfPHQ7.gif",
			"https://i.imgur.com/qkyZIx3.jpg",
			"http://i.imgur.com/SOlQj3w.gif",
			"http://i.imgur.com/0qtNLtx.gif",
			"http://i.imgur.com/8BOLncT.gif",
			"http://giant.gfycat.com/UnripeGiddyGlowworm.gif",
			"https://i.imgur.com/EL6kUeb.jpg",
			"http://i.imgur.com/ZrqYuoD.gif",
			"http://i.imgur.com/uz8k97i.gif",
			"http://i.imgur.com/NWFwek7.gif",
			"http://i1.wp.com/sourcefed.com/wp-content/uploads/2014/11/woody-rocket.gif?resize=500%2C230",
			"https://i.imgur.com/U8oi07c.jpg",
			"http://i.imgur.com/ODQ0CEc.gif",
			"http://i.imgur.com/3uGw8Op.gif",
			"https://i.imgur.com/6h2aS1z.gif",
			"http://i.imgur.com/peFgSoo.gif",
			"https://i.imgur.com/Nu8Mw0i.jpg",
			"http://i.imgur.com/WMp4vh5.gif",
			"http://i.imgur.com/t1aUqD3.gif",
			"http://i.imgur.com/Nyop7iN.gif",
			"http://i.imgur.com/0bkyUix.gif",
			"http://38.media.tumblr.com/7703784383b0aade9728673ea37aed89/tumblr_nj3ygtOZ5Q1qb5gkjo4_500.gif",
			"http://i.imgur.com/LNBnojc.gif",
			"http://www.gfycat.com/FarflungIdealisticFugu",
			"http://i.imgur.com/cJK57Ii.gifv",
			"https://gfycat.com/MetallicPerfumedAcouchi#",
			"http://i.imgur.com/XeZwYd8.gif",
			"http://i.imgur.com/byYDWCw.gif",
			"https://38.media.tumblr.com/7b735928419c67c53bbf229d5ee19e05/tumblr_mouegrKZeo1svh7j5o1_500.gif",
			"http://i.imgur.com/gSqZUWf.gifv"]

    def __init__(self, msg):
        super(ResponseNutted, self).__init__(msg, self.__module__, ResponseNutted.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = random.choice(ResponseNutted.nutted_responses)
            self.note_response(out)
            return out
        print("not responding to nutted because sender {} is on cooldown".format(self.msg.name))
