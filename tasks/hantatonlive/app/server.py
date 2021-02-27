#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import array
import numpy as np
import base64
import asyncio
import base64
import math
import hmac
import json
import os
import io
import sys
from datetime import datetime, timezone
from typing import Optional, Generator, Iterable
from jinja2 import FileSystemLoader
import base64
from pydub import AudioSegment

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR
DATABASE = os.path.join(STATE_DIR, "db.sqlite3")

PREFIX = "ugra_everything_is_a_remix_even_"
SECRET2 = b"playmate-nibble-slobbery-nastily-retrace"
COOKIE_SECRET = b"KC0gBmM0LzIntvY1dHSTPxJ10nPW9MdNffHEf1YDdDY="
SALT1_SIZE = 16
SALT2_SIZE = 16

BAR = 667

SAMPLES = [
    '2kicks_1.mp3',
    'bass_a_1.mp3',
    'bass_b_1.mp3',
    'bass_d_1.mp3',
    'bass_f_1.mp3',
    'chord_a_1.mp3',
    'chord_b_1.mp3',
    'chord_d_1.mp3',
    'chord_f_1.mp3',
    'hats_1.mp3',
    'hats_fast_1.mp3',
    'kick_1.mp3',
    'kick_and_snare_1.mp3',
    'single_hat_1.mp3',
    'snare_1.mp3',
    'snare_fill_1.mp3'
]
SAMPLES_DIR = os.path.join('static', 'samples')
samples = None


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def load_sample(filename):
    return AudioSegment.from_mp3(os.path.join(SAMPLES_DIR, filename))


def stego(audio, token):
    bit = 6
    flag = ''.join(["{0:08b}".format(x) for x in get_flag(token).encode('ascii')])
    flag = list(map(int, flag))
    arr = np.array(audio.get_array_of_samples()).T.astype(np.int16)
    
    mask = np.zeros((len(arr), ), dtype=np.int16)
    mask[::len(arr)//len(flag)+1] = 1

    equalizer = np.where(
        mask > 0,
        (1 << bit - 1),
        0
    ).astype(np.int16)
    
    flagolizer = np.copy(mask)
    flagolizer[::len(arr)//len(flag)+1] = np.array(flag, dtype=np.int16) << (bit-1)

    arr = arr & ~equalizer ^ flagolizer
    arr = array.array(audio.array_type, arr)
    new_audio = audio._spawn(arr)
    return new_audio


def render(grid):
    global samples
    grid_audio = AudioSegment.silent(duration=1)
    for bar in grid:
        bar = bar
        bar_audio = AudioSegment.silent(duration=BAR)
        if bar != ['']:
            for sample in bar:
                bar_audio = bar_audio.overlay(samples[int(sample)])
            grid_audio += bar_audio
    return grid_audio


def build_app():
    global samples
    app = web.Application()
    routes = web.RouteTableDef()

    print("Loading samples...")
    samples = map(load_sample, SAMPLES)
    samples = list(samples)

    @routes.get('/{token}')
    async def main(request):
        return jinja2.render_template(f'game.html', request, {})

    @routes.get('/{token}/wav')
    async def generate(request):
        token = request.match_info['token']

        grid_b64 = request.query['grid']
        grid = base64.b64decode(grid_b64).decode('ascii')
        grid = [x.split(',') for x in grid.split(';')]

        audio = render(grid)
        audio = stego(audio, token)
        buffer = io.BytesIO()
        audio.export(buffer, format='wav')

        resp = web.StreamResponse()
        resp.headers["Content-type"] = "audio/wave"
        resp.headers["Content-disposition"] = "inline; filename=bounce.wav"
        await resp.prepare(request)
        await resp.write(buffer.getvalue())
        return resp


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
        web.run_app(app, path=os.path.join(STATE_DIR, 'hantatonlive.sock'))


if __name__ == '__main__':
    start()
