#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('../')
from numpy import random
from src.utils import read_token, read_html, make_api_call, fetch_game_list
from src.enums import SNES, PS4
import cherrypy
import json


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
        self.game_list = fetch_game_list(self.token, console_id)

    def fetch_game_name(self, game_id):
        """
        Fetches the name of the game corresponding to game_id.
        :param game_id: The ID of the game we're looking up.
        :return: The name of game_id.
        """

        if game_id not in self.game_mapping:

            r_json = make_api_call("games", self.token, endpoint_id=game_id)

            for game in r_json:

                game_name = game.get("name", "")
                print(game_id, game_name)
                self.game_mapping[game_id] = game_name

        return self.game_mapping[game_id]

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

        return read_html("cookie.html").replace("{game_title}", game_name)


class Root:
    snes = SNESRandomizer(SNES)
    ps4 = SNESRandomizer(PS4)

    @cherrypy.expose()
    def index(self, pid=None):

        if pid:
            pid = int(pid)
            if pid == SNES:
                return Root.snes.index()
            elif pid == PS4:
                return Root.ps4.index()
        else:
            return read_html("index.html")


if __name__ == "__main__":

    cherrypy.config.update({
        'server.socket_port': 5112,
        'server.socket_host': "192.168.1.179",
        'response.timeout': 1600000
    })

    conf = {"/css": {"tools.staticdir.on": True,
                     "tools.staticdir.dir": os.path.abspath("../bin/css"), },
            '/styles.css':
                {'tools.staticfile.on': True,
                 'tools.staticfile.filename': os.path.abspath("../bin/css/styles.css"),
                 }
            }

    cherrypy.quickstart(Root(), config=conf)
