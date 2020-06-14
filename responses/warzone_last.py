from .AbstractResponse import *
import requests
import os
import pickle

class WarzoneLast(AbstractResponse):
    RESPONSE_KEY = "#zonelast"

    HELP_RESPONSE = "Shows your personel stats from the last game, add a user argument to find someone elses stats"

    DOTABUFF_LINK_TEMPLATE = "http://www.dotabuff.com/matches/{id}"

    def __init__(self, msg):
        super(WarzoneLast, self).__init__(msg)
        self.auth_session = None

    def get_match(self, session, name):

        platform = name.split(":")[0]
        username = name.split(":")[1]

        URL = "https://my.callofduty.com/api/papi-client/crm/cod/v2/title/mw/platform/{platform}/gamer/{name}/matches/warzone/start/0/end/0/details".format(name = username, platform = platform)
        matches = session.get(URL)
        return matches

    def reauth(self):

        # Request a basic page to get the CSRF
        cod_session = requests.Session()

        url = 'https://profile.callofduty.com/cod/login'
        req = cod_session.get(url)

        header_data = dict(req.headers)["Set-Cookie"].split(";")
        for cookie in header_data:
            split = cookie.split("=")
            if split[0] == "XSRF-TOKEN": CSRF = split[1]

        url = 'https://profile.callofduty.com/do_login?new_SiteId=cod'
        values = {'username': "dimos84696@reqaxv.com", 'password': AbstractResponse.local_var["COD_PASS"], 'remember_me': "true", "_csrf": CSRF}

        #Make a second request to login
        req2 = cod_session.post(url, data=values)
        ATKN = cod_session.cookies.get_dict()["atkn"]

        os.environ['COD_CSRF'] = CSRF
        os.environ['COD_ATKN'] = ATKN

        #Save this session (and the cookies)
        self.auth_session = cod_session
        with open('COD_session.pickle', 'wb') as handle:
            pickle.dump(cod_session, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Printing session file")

    def respond(self):

        canonical_name = next(key for key, value in AbstractResponse.GroupMeIDs.items() if value == self.msg.sender_id)
        COD_name = AbstractResponse.GroupMetoCODName[canonical_name]

        if COD_name == None: return "I don't know your Call of Duty ID"

        #open the saved file. If that fails, write a new one
        try:
            with open('COD_session.pickle', 'rb') as handle:
                self.auth_session = pickle.load(handle)
        except Exception as error:
            print("File not found")
            self.reauth()

        if self.auth_session is not None:
            print("Auth is set")
            match_history = self.get_match(self.auth_session, COD_name)

            if match_history.status_code != 200 or "matches" not in match_history.json()["data"]:
                #Maybe the Authentication is stale? Reauthenticate and try again

                self.reauth()
                match_history = self.get_match(self.auth_session, COD_name)

            matches_data = match_history.json()["data"]["matches"][0]


            match_performance_template = "{name} of clan {clan} finished {place}th with {kills} kills and {damage} damage. He "

            gulag = "didn't go to the gulag"
            place = "?"
            if "gulagKills" in matches_data["playerStats"]:
                if matches_data["playerStats"]["gulagKills"] > 0: gulag = "won his gulag (ez)"
                if matches_data["playerStats"]["gulagDeaths"] > 0: gulag = "lost his gulag (bitch)"
                place = int(matches_data["playerStats"]["teamPlacement"])
            else:
                gulag = "played some wierd mode"

            if "clantag" not in matches_data["player"]: matches_data["player"]["clantag"] = "looking for love"

            return match_performance_template.format(
                name = matches_data["player"]["username"],
                clan = matches_data["player"]["clantag"],
                place = place,
                damage = matches_data["playerStats"]["damageDone"],
                kills = int(matches_data["playerStats"]["kills"])
            ) + gulag