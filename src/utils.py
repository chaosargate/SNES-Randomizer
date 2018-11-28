import requests


def read_file(filename):
    file_txt = ""
    with open("../bin/{filename}".format(filename=filename)) as file_str:
        file_txt = file_str.read()
    return file_txt


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


def make_console_links(console_map):
    links = ""
    for i, console_id in enumerate(console_map):
        console = console_map[console_id]
        href = "?pid={id}".format(id=console_id)
        link = "<a class ='console' href='{href}'>{name}</a>".format(
            href=href,
            name=console.get_name()
        )
        links += link
    return links
