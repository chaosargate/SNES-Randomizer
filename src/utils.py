import requests


def read_token():
    """
    Reads the token.txt file from the bin folder and stores that as the auth-key.
    :return: The token string.
    """
    token = None
    with open("../bin/token.txt") as token_txt:
        token = token_txt.read()
    return token.strip()


def read_html(filename):
    html = ""
    with open("../bin/{filename}".format(filename=filename)) as html_file:
        html = html_file.read()
    return html


def make_api_call(endpoint, token, endpoint_id=None):
    """
    Makes an API call to igdb.
    :param endpoint: The specific endpoint we want to hit.
    :param token: The user auth token.
    :param endpoint_id: The ID for the endpoint we want.
    :return: The JSON result of the request to the endpoint.
    """

    print("Making call to " + endpoint)
    print("ID: " + str(endpoint_id))
    headers = {
        "user-key": token,
        "Accept": "application/json"
    }

    url = "https://api-endpoint.igdb.com/{endpoint}{id}".format(
        endpoint=endpoint,
        id="/" + str(endpoint_id) if endpoint_id else "/"
    )

    print("URL: " + url)

    r = requests.get(url, headers=headers)
    return r.json()


def fetch_game_list(token, console_id):
    """
    Fetches the overall list of games.
    :return: A list of igdb game IDs.
    """
    game_list = []

    r_json = make_api_call("platforms", token, endpoint_id=console_id)

    for platform in r_json:

        for game in platform.get("games", []):

            game_list.append(game)

    return game_list
