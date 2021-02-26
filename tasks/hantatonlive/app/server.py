#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import base64
import asyncio
import base64
import math
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional, Generator, Iterable
from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR
DATABASE = os.path.join(STATE_DIR, "db.sqlite3")

PREFIX = "ugra_gotta_hit_fast_"
SECRET2 = b"aRUpGrnZ3XkYgfzZ"
COOKIE_SECRET = b"KC0gBmM0LzIntvY1dHSTPxJ10nPW9MdNffHEf1YDdDY="
SALT1_SIZE = 16
SALT2_SIZE = 16

def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()


    @routes.get('/{token}')
    async def main(request):
        return jinja2.render_template(f'game.html', request, {})

    routes.static('/static', 'static')
    
    app.add_routes(routes)
    jinja2.setup(
        app,
        loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates'))
    )
    return app


def start():
    app = build_app()

    loop = asyncio.get_event_loop()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(STATE_DIR, 'best-edm.sock'))


if __name__ == '__main__':
    start()
