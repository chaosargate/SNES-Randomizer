#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
import json
from numpy import random
import requests


class SNESRandomizer:
    def __init__(self):
        self.token = self.read_token()
        self.game_mapping = {}
        self.game_list = self.fetch_game_list()

    def fetch_game_list(self):
        game_list = []
        params = {
            "user-key": self.token,
            "Accept": "application/json"
        }

        r = requests.get(
            "https://api-endpoint.igdb.com/platforms/19",
            headers=params
        )

        r_json = r.json()

        for platform in r_json:
            for game in platform.get("games", []):
                game_list.append(game)
                #self.fetch_game_name(game)
        return game_list

    def fetch_game_name(self, game_id):
        if game_id not in self.game_mapping:
            params = {
                "user-key": self.token,
                "Accept": "application/json"
            }

            r = requests.get(
                "https://api-endpoint.igdb.com/games/{id}".format(id=game_id),
                headers=params
            )

            r_json = r.json()
            for game in r_json:
                game_name = game.get("name", "")
                print(game_id, game_name)
                self.game_mapping[game_id] = game_name

        return self.game_mapping[game_id]

    def read_token(self):
        token = None
        with open("../bin/token.txt") as token_txt:
            token = token_txt.read()
        return token

    @cherrypy.expose()
    def check_stored_games(self):
        return json.dumps({"ids": self.game_list,
                           "mapping": self.game_mapping,
                           "count": len(self.game_list)})

    @cherrypy.expose()
    def index(self):
        rand_int = random.randint(0, len(self.game_list))

        game_id = self.game_list[rand_int]
        game_name = self.fetch_game_name(game_id)

        return json.dumps({"id": game_id,
                           "name": game_name})


if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_port': 8080,
        'server.socket_host': "192.168.1.179",
        'response.timeout': 1600000
    })
    cherrypy.quickstart(SNESRandomizer())
