#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cherrypy
import json
import requests
sys.path.append('../')

from numpy import random
from src.utils import read_token, cookie_html
from src.enums import SNES


class SNESRandomizer:
    """
    SNES Randomizer class.
    """

    def __init__(self, console_id, pre_fetch=False):
        """
        Class initializer.
        :param pre_fetch: Fetch the game-mapping on startup? (This will make tons of requests so its super slow!!!)
        """
        self.pre_fetch = pre_fetch
        self.token = read_token()
        self.game_mapping = {}
        self.game_list = self.fetch_game_list(console_id)

    def fetch_game_list(self, console_id):
        """
        Fetches the overall list of games.
        :return: A list of igdb game IDs.
        """
        game_list = []

        r_json = self.make_api_call("platforms", console_id)

        for platform in r_json:

            for game in platform.get("games", []):

                game_list.append(game)

                if self.pre_fetch:
                    self.fetch_game_name(int(game))

        return game_list

    def fetch_game_name(self, game_id):
        """
        Fetches the name of the game corresponding to game_id.
        :param game_id: The ID of the game we're looking up.
        :return: The name of game_id.
        """

        if game_id not in self.game_mapping:

            r_json = self.make_api_call("games", game_id)

            for game in r_json:

                game_name = game.get("name", "")
                print(game_id, game_name)
                self.game_mapping[game_id] = game_name

        return self.game_mapping[game_id]

    def make_api_call(self, endpoint, endpoint_id=None):
        """
        Makes an API call to igdb.
        :param endpoint: The specific endpoint we want to hit.
        :param endpoint_id: The ID for the endpoint we want.
        :return: The JSON result of the request to the endpoint.
        """

        print("Making call to " + endpoint)
        print("ID: " + str(endpoint_id))
        headers = {
            "user-key": self.token,
            "Accept": "application/json"
        }

        url = "https://api-endpoint.igdb.com/{endpoint}{id}".format(
            endpoint=endpoint,
            id="/" + str(endpoint_id) if endpoint_id else ""
        )
        r = requests.get(url, headers=headers)
        return r.json()

    @cherrypy.expose()
    def check_stored_games(self):
        """
        API endpoint to check the overall list of games, the current mapping of game IDs to names, and the total number.
        :return: A JSON object of the stored stats.
        """
        return json.dumps({"ids": self.game_list,
                           "mapping": self.game_mapping,
                           "count": len(self.game_list)})

    @cherrypy.expose()
    def index(self):
        """
        Default method that fetches a random game and returns it and its name.
        :return: A JSON object that maps a game ID to its name.
        """
        rand_int = random.randint(0, len(self.game_list))

        game_id = self.game_list[rand_int]
        game_name = self.fetch_game_name(int(game_id))

        return cookie_html(game_name)


if __name__ == "__main__":

    cherrypy.config.update({
        'server.socket_port': 8080,
        'server.socket_host': "192.168.1.179",
        'response.timeout': 1600000
    })
    cherrypy.quickstart(SNESRandomizer(SNES))
