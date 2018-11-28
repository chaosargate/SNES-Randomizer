#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('../')
from src.utils import read_html, make_console_links
from src.enums import *
from src.randomizer import GameRandomizer
import cherrypy


class Root:

    console_map = {
            SNES: GameRandomizer(SNES),
            PS4: GameRandomizer(PS4)
    }

    @cherrypy.expose()
    def index(self, pid=None):

        if pid:
            pid = int(pid)

            if pid in Root.console_map:
                return Root.console_map[pid].index()

        links = make_console_links(Root.console_map)
        index_html = read_html("index.html").replace("{links}", links)
        return index_html


if __name__ == "__main__":

    host = read_html("host.txt").strip()

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
