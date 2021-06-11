# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import yfinance

def pct_diff(today, past):
    change = round(today - past, 2)
    pct = round(100 * change / past, 2)
    if change > 0:
        change = "+" + str(change)
    if pct > 0:
        pct = "+" + str(pct) + "%" # "% \u1F4C89"
    else:
        pct = str(pct) + "%" # "% \u1F4C9"
    return f"{change} ({pct})"


class ResponseStonk(ResponseCooldown):

    RESPONSE_KEY = "#stonk"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseStonk, self).__init__(msg, self, ResponseStonk.COOLDOWN)

    def _respond(self):
        ticker_name = self.msg.text.partition(ResponseStonk.RESPONSE_KEY)[-1].strip()
        print(f"Searching for ticker name = '{ticker_name}'")
        ticker = yfinance.Ticker(ticker_name)
        history = ticker.history("1y")
        open_prices = history['Open']
        open_prices = [round(_, 2) for _ in open_prices]
        if not len(open_prices):
            return f"Couldn't find ticker {ticker_name}"
        price_1y_ago = open_prices[0]
        price_1m_ago = open_prices[-3]
        price_1w_ago = open_prices[-8]
        price_1d_ago = open_prices[-2]
        price_0d_ago = open_prices[-1]
        resp = f"""{ticker.info['shortName']} ({ticker_name}) today: {round(price_0d_ago, 2)}
    1d: {pct_diff(price_0d_ago, price_1d_ago)}
    1w: {pct_diff(price_0d_ago, price_1w_ago)}
    1m: {pct_diff(price_0d_ago, price_1m_ago)}
    1y: {pct_diff(price_0d_ago, price_1y_ago)}
"""
        return resp