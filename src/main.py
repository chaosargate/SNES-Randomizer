#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('../')
from src.utils import read_file, make_console_links
from src.randomizer import GameRandomizer
import cherrypy
import json


class Root:

    token = read_file("token.txt")
    platform_list = read_file("platforms.txt")
    platforms = json.loads(platform_list)

    console_map = {}

    for p_index, platform_id in enumerate(platforms):
        if platform_id not in console_map:
            console_map[platform_id] = GameRandomizer(platform_id, token)

    @cherrypy.expose()
    def index(self, pid=None):

        if pid:
            if pid in Root.console_map:
                return Root.console_map[pid].index()

        links = make_console_links(Root.console_map)
        index_html = read_file("index.html").replace("{links}", links)
        return index_html


if __name__ == "__main__":

    host = read_file("host.txt").strip()

    cherrypy.config.update({
        'server.socket_port': 8080,
        'server.socket_host': host,
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
