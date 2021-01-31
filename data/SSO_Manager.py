import urllib

from data import DataAccess
import requests
from requests_oauthlib import OAuth2Session
from responses import SSOResponse
from enum import Enum
import json
import time
import pprint

"""

Generally for a new SSO path:

1. Prompt user to login -->
2. User logs in --> (server sends back `authorization_code` and `state`)
3. sUN exchanges authorization_code/state for access token
4. sUN uses access token to get data

Control flow:
1. Check if we have a token attached to this control flow
    user.[SPOTIFY] --> {
        (from API) "access_token": "NgCXRK...MzYjw",
        (from API) "token_type": "Bearer",
        (from API) "scope": "user-read-private user-read-email",
        (from API) "expires_in": 3600,
        (from API) "refresh_token": "NgAagA...Um_SHo"
        (from sUN/API) "expires_at": 1611628195
    }
2. if NO TOKEN:
    2.1. Prompt user to login (dm?) ==> send them a link with this info in it
        {
            client_id: our secret API key granted by system
            response_type: "code" (required)
            redirect_uri: sUN/ssoPath
            state: string, returned in redirect URI
                include:
                    groupme_user_id
                    name of requesting class
            scope: whatever needed for our access // specific to each API
        }
    2.2. The user authorizes (or doesn't), and we get back:
        {
            code: authorization code to be exchanged for a token
            state: string sent in prompt
        }
    2.3 We use code in combination with our client_id to get a token:
        {
            grant_type: "authorization_code"
            code: the authorization code from above
            redirect_uri: must exactly match redirect URI used in 2.1,  not actually redirected to
        }

        and (if successful) is returned (see 1)
    2.4 We shove response into database
        2.4.1 Add "expires_at" if not found
        2.4.2 Get user (based on params in state, using DataAccess)
        2.4.3 Add modified token dict to user in database
    2.5 DM user to ask them to try to use #{service} again
3. If TOKEN:
    3.1 Check access token expiration time against now:
        3.1.1 If token expired, request new access token using refresh token:
            {
                client_id
                client_secret
                grant_type: "refresh_token"
                refresh_token: <token obtained in 1>
            }
            if successful, returns token from (1).
        3.1.2 Shove token into database
            See 2.4
    3.2 Use token to request data
        header: AUTHORIZATION TOKEN
        body {
            parameters for this specific command
        }

    General functions needed:
        add_token_to_database(user, token)
        get_token_for_user(user)

SSO_Manager.get_data(<classname>, msg)
    id, secret = get_secret_keys(classname)
    token = get_user_token(<classname>, msg)
    if not token:
        start_original_token_generation(<classname>, msg)
        return none
    else:
        token = refresh_token(<classname>, msg)
        data = do_data_request(<classname>, msg, token)
        return data
if data:
    (work with data and make response)
    return response


"""


class SSO_Outcome_Type(Enum):
    SUCCESS = 1
    NO_TOKEN = 2
    TOKEN_EXPIRED = 3
    OUT_OF_SCOPE = 4
    REJECTED = 5


class SSO_Outcome(object):
    def __init__(self, outcome_type, data, auth_url):
        self.outcome_type = outcome_type
        self.data = data
        self.auth_url = auth_url


def build_data_request_params(clazz, id):
    pass


def make_oauth_session(clazz, client_id):
    oauth = OAuth2Session(
        client_id=client_id,
        redirect_uri=type(clazz).REDIRECT_URI,
        scope=type(clazz).REQUEST_SCOPES,
    )

    return oauth

def start_original_token_generation(clazz, id, client_id, client_secret):
    # build access request:
    # client_id         => api_id
    # redirect_uri      =>
    # response_type     => `code`
    # scope             => clazz.SCOPE
    # state             => string returned to redirect_url

    oauth = make_oauth_session(clazz, client_id)

    auth_url, state = oauth.authorization_url(
        url=type(clazz).AUTH_URL,
        state=clazz.make_auth_state(),
    )

    return auth_url


def refresh_token(clazz, id, token):
    now = time.time()
    if now < token['expires_at']:
        return token
    # ok, we have to exchange for a new token using `token['refresh_token']`
    client_id, client_secret = DataAccess.get_secret_keys(clazz)

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    google = OAuth2Session(client_id, token=token)
    token = google.refresh_token(type(clazz).TOKEN_REFRESH_URL, **extra)
    return token


def do_data_request(clazz, id, token):
    client_id, client_secret = DataAccess.get_secret_keys(clazz)
    session = OAuth2Session(client_id, token=token)
    data = session.get(type(clazz).DATA_ACCESS_URL)
    return json.loads(data.content)

def get_first_token(clazz, id, code):
    client_id, client_secret = DataAccess.get_secret_keys(clazz)
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": type(clazz).REDIRECT_URI,

    }
    response = requests.post(type(clazz).TOKEN_REFRESH_URL, data=params)
    token = json.loads(response.content.decode('utf-8'))
    DataAccess.store_token(clazz, id, token)

def get_SSO_data(clazz, msg):
    user_groupme_id = msg.sender_id
    client_id, client_secret = DataAccess.get_secret_keys(clazz)
    token = DataAccess.get_current_token(clazz, user_groupme_id)
    if not token:
        auth_url = start_original_token_generation(clazz, user_groupme_id, client_id, client_secret)
        return SSO_Outcome(SSO_Outcome_Type.NO_TOKEN, None, auth_url)
    else:
        token = refresh_token(clazz, user_groupme_id, token)
        if not token:
            return SSO_Outcome(SSO_Outcome_Type.REJECTED, None, None)
        DataAccess.store_token(clazz, user_groupme_id, token)
        data = do_data_request(clazz, user_groupme_id, token)
        return SSO_Outcome(SSO_Outcome_Type.SUCCESS, data, None)
