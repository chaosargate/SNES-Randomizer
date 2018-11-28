from src.utils import *
from numpy import random


class GameRandomizer:
    """
    SNES Randomizer class.
    """

    def __init__(self, console_id, token):
        """
        Class initializer.
        """
        self.token = token
        self.game_mapping = {}
        self.game_list = []

        platform_json = make_api_call("platforms", self.token, console_id)[0]

        for game in platform_json.get("games", []):

            self.game_list.append(game)

        self.name = platform_json.get("name", "")

    def get_name(self):
        return self.name

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

    def index(self):
        """
        Default method that fetches a random game and returns it and its name.
        :return: A JSON object that maps a game ID to its name.
        """
        rand_int = random.randint(0, len(self.game_list))

        game_id = self.game_list[rand_int]
        game_name = self.fetch_game_name(int(game_id))

        cookie_html = read_file("cookie.html").replace("{game_title}", game_name)
        cookie_html = cookie_html.replace("{game_console}", self.name)

        return cookie_html
