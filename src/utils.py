def read_token():
    """
    Reads the token.txt file from the bin folder and stores that as the auth-key.
    :return: The token string.
    """
    token = None
    with open("../bin/token.txt") as token_txt:
        token = token_txt.read()
    return token


def cookie_html(title):
    html = ""
    with open("../bin/cookie.html") as html_file:
        html = html_file.read()
        html = html.replace("{game_title}", title)
    return html
