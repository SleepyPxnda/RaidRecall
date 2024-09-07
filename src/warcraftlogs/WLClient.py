import datetime
import json
from types import SimpleNamespace

import requests
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from requests.auth import HTTPBasicAuth

from src.utils import get_bot_settings


class WLClient:
    def __init__(self, link: str):
        self.renew_timestamp = datetime.datetime.now()
        self.bearer_token = None
        self.link = link

    def retrieve_auth_token(self):
        client_id = get_bot_settings("wl_client_id")
        client_secret = get_bot_settings("wl_client_secret")


        basic_auth = HTTPBasicAuth(client_id, client_secret)
        token_response = requests.post("https://www.warcraftlogs.com/oauth/token", auth=basic_auth, data={'grant_type': 'client_credentials'})

        self.bearer_token = token_response.json()["access_token"]
        self.renew_timestamp = datetime.datetime.now().timestamp() + token_response.json()["expires_in"]

    async def request_data(self):
        if self.bearer_token is None or self.renew_timestamp < datetime.datetime.now():
            self.retrieve_auth_token()
        with open("warcraftlogs/raid_schema.graphql") as f:
            string_query = f.read()
        transport = AIOHTTPTransport(url="https://www.warcraftlogs.com/api/v2/client", headers={'Authorization': 'Bearer ' + self.bearer_token})
        client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=30)
        query = gql(string_query)
        result = await client.execute_async(query, variable_values={"id": "WFbmDarcwqHpjvTh"})

        #with open("warcraftlogs/response_mock.json", encoding="utf8") as f:
        #    result = json.load(f)

        return result

