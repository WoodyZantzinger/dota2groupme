# -*- coding: utf-8 -*
from .AbstractResponse import *


class ResponseJohnCena(AbstractResponse):

    RESPONSE_KEY = "john cena"

    def __init__(self, msg):
        super(ResponseJohnCena, self).__init__(msg)

    def respond(self):
        return "DAAH DAAHT DOOT DAAH"

