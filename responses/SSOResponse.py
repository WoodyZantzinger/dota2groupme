# -*- coding: utf-8 -*
from .AbstractResponse import *
from data import SSO_Manager

# credentials manager?

# Get this information from an api:
# AUTH_URL = r"https://www.strava.com/oauth/authorize"
# TOKEN_REFRESH_URL = r"https://www.strava.com/oauth/token"
# DATA_ACCESS_URL = r"https://www.strava.com/api/v3/activities"
# REQUEST_SCOPES = [
#     "activity:read_all"
# ]

# Set up information from an API:
# 1. Create an account with the API
# 2. Configure Authorized Callback Domains with API:
#   Need to include young-fortress-3393.herokuapp.com
# 3. Get client id, client secret from API
# 4a. Add id/secret to local_variables.json
# 4b. Add same to https://dashboard.heroku.com/apps/young-fortress-3393/settings

class SSO_Response(AbstractResponse):

    REDIRECT_URI = r'https://young-fortress-3393.herokuapp.com/oauth_callback/'
    #   static variables:
    #   auth_url
    #   token_refresh_url
    #   endpoint_url


    def __init__(self, msg, obj):
        super(SSO_Response, self).__init__(msg, obj)
        self.msg = msg
        self.data = None
        self.obj = obj
        self.outcome = None
        self.authenticate(obj, msg)

    def authenticate(self, obj, msg):
        self.outcome = SSO_Manager.get_SSO_data(obj, msg)

    def _respond(self):
        if self.outcome.outcome_type == SSO_Manager.SSO_Outcome_Type.NO_TOKEN:
            self.response = f"Please authenticate before using {self.clazzname}:\n{self.outcome.auth_url}"
        if self.outcome.outcome_type == SSO_Manager.SSO_Outcome_Type.REJECTED:
            self.response = f"Unknown failure in using {self.clazzname}"
        return self.response

    def make_auth_state(self):
        return self.clazzname + "|" + self.msg.sender_id
        pass

    def id_key_name(self):
        # id, or username, for access to API (generated manually)
        rval = self.clazzname + "_ID"
        return rval

    def key_key_name(self):
        # key, or password, for accesss to API (generated manually)
        rval = self.clazzname + "_KEY"
        return rval

    def token_key_name(self):
        rval = self.clazzname + "_TOKEN"
        return rval

    @classmethod
    def exchange_code_for_first_key(self, code, clazz, id):
        SSO_Manager.get_first_token(clazz, id, code)
        pass


def main():
    gmid = "3328256"
    rsso = ResponseSSO(1, 1)
    user = rsso.authenticate({"user_id": gmid}, 123)
    print(user)
