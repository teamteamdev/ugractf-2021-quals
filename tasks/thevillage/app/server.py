#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import aiohttp_session
import cryptography
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import asyncio

import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import asyncio
import base64
import random
import math
import hmac
import json
import os
import io
import sys
from jinja2 import FileSystemLoader
import base64
import time

from pyzbar.pyzbar import decode
from PIL import Image

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR

PREFIX = "ugra_come_for_tasks_stay_for_"
SECRET2 = b"GfkGCGfrk5l6S521koyfjR24fkFsdufgEndEFlfPvFwJR"
COOKIE_SECRET = b"bG9va2tlZWtvbWFhYWFnYWZqZmpma2ZrZmthYWFhZAo="
SALT1_SIZE = 16
SALT2_SIZE = 12

PROHIBITED_INVITE = 313337

INVITES = 7777777
FREE = 37

BRUTES = {}

messages = {
    'fa': 'Вы что вообще заслали? Ну-ка быстренько исправляемся!',
    'l': 'Ошибка: инвитик староват!!',
    'g': 'Error: Hi! У вас инвит недействительный! Good bye!'
}

def get_suffix(token):
    return hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def get_flag(token):
    return PREFIX + get_suffix(token)


def get_free_invites(token):
    random.seed(token)
    free = sorted([random.randint(INVITES // 3, INVITES - INVITES // 3) for x in range(FREE)])
    free = filter(lambda x: x != PROHIBITED_INVITE, free)
    return list(free)

def reverse_bin_search(invite, invites):
    try:
        invite = int(invite)
    except:
        return 'fa', -1
    if invite > INVITES:
        return 'fa', -1
    elif invite in invites:
        return 'eq', 0
    elif invite < invites[-1]:
        return 'l', invites[-1] - invite
    elif invite > invites[-1]:
        return 'g', invite - invites[-1]


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()


    @routes.get('/{token}')
    async def landing(request):
        session = await get_session(request)
        is_in = session.get("invite")
        token = request.match_info['token']

        if is_in:
            return jinja2.render_template(f'app.html', request, {
                'suffix': get_suffix(token)
            })            
        
        return jinja2.render_template(f'index.html', request, {})


    @routes.post('/{token}')
    async def degenerate(request):
        data = await request.post()        
        email = data.get('email')
        session = await get_session(request)
        token = request.match_info['token']

        lock = asyncio.Lock()
        async with lock:
            if not BRUTES.get(token):
                BRUTES[token] = 1, time.time()
            else:
                tries, last = BRUTES[token]
                if tries > 60:
                    if time.time() - last > 60:
                        BRUTES[token] = 0, time.time()
                    else:
                        raise web.HTTPTooManyRequests()
                else:
                    BRUTES[token] = tries + 1, last
        
        if not email or '@' not in email:
            return jinja2.render_template(f'index.html', request, {
                'error': "E-mail такого нету или неправильный."
            })

        tokens = get_free_invites(token)
        print(tokens)

        try:
            invite = data['invite'].file
            invite = decode(Image.open(invite))[0].data            
            invite = base64.b64decode(invite).decode('ascii')
        except:
            return jinja2.render_template(f'index.html', request, {
                'error': "Вы вообще ЧТО загрузили? xD"
            }) 

        status, diff = reverse_bin_search(invite, tokens)

        if status == 'eq':
            session["invite"] = invite
            return web.HTTPFound(f'/{token}')
        else:        
            return jinja2.render_template(f'index.html', request, {
                'error': messages[status]
            })
    

    routes.static('/static', 'static')

    aiohttp_session.setup(app, EncryptedCookieStorage(base64.b64decode(COOKIE_SECRET)))
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
        web.run_app(app, path=os.path.join(STATE_DIR, 'thevillage.sock'))


if __name__ == '__main__':
    start()
