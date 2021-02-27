#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import aiohttp_session
import base64
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import asyncio
import base64
import math
import hmac
import json
import os
import sys
import numpy as np
from datetime import datetime, timezone
from dataclasses import dataclass, field
import dataclasses_json
from dataclasses_json import dataclass_json
from typing import Optional, Generator, Iterable
from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR
DATABASE = os.path.join(STATE_DIR, "db.sqlite3")

PREFIX = "ugra_gotta_hit_fast_"
SECRET2 = b"aRUpGrnZ3XkYgfzZ"
COOKIE_SECRET = b"KC0gBmM0LzIntvY1dHSTPxJ10nPW9MdNffHEf1YDdDY="
SALT2_SIZE = 12

MAX_GAME_TIME = 30
GAME_FPS = 1
GAME_DT = 1 / GAME_FPS
SHIP_SPEED = 100
FIELD_FROM = np.array([-200, -200])
FIELD_TO = np.array([200, 200])
ROCKET_SIZE = np.array([1, 1])
GAME_TRIES = 6

def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]

@dataclass_json
@dataclass
class State:
    position: np.ndarray = field(
        metadata=dataclasses_json.config(
            encoder=list,
            decoder=np.array,
        ),
    )
    angle: float
    time: float

UNIT_VECTOR = np.array([1.0, 0.0])

def step(state: State, angle_change: float, speed: float, dt: float) -> State:
    new_angle = (state.angle + angle_change) % (2 * math.pi)
    direction = np.array([math.sin(new_angle), math.cos(new_angle)])
    new_position = state.position + dt * speed * direction
    return State(
        position=new_position,
        angle=new_angle,
        time=state.time + dt,
    )

def random_step(state: State, speed: float, dt: float) -> State:
    angle_change = np.random.default_rng().uniform(-math.pi / 2, +math.pi / 2)
    return step(state, angle_change, speed, dt)

def random_state(from_pos: Optional[np.ndarray] = None, to_pos: Optional[np.ndarray] = None) -> State:
    if from_pos is None:
        from_pos = np.array([-1, -1])
    if to_pos is None:
        to_pos = np.array([1, 1])
    position = np.random.default_rng().uniform(from_pos, to_pos)
    angle = np.random.default_rng().uniform(0, 2 * math.pi)
    return State(
        position=position,
        angle=angle,
        time=0,
    )


def clear_session(session):
    del session["ship"]
    del session["start"]
    del session["tries"]


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()


    @routes.get('/{token}/')
    async def main(request):
        return jinja2.render_template(f'game.html', request, {})

    @routes.post('/{token}/reset')
    async def reset_game(request):
        session = await get_session(request)
        ship = random_state(FIELD_FROM, FIELD_TO)
        session["ship"] = ship.to_dict()
        session["start"] = datetime.now(timezone.utc).isoformat()
        session["tries"] = GAME_TRIES
        return web.json_response({"status": "ok", "tries_left": GAME_TRIES})

    @routes.post('/{token}/fire')
    async def fire_rocket(request):
        token = request.match_info["token"]
        session = await get_session(request)
        if "ship" not in session or "start" not in session or "tries" not in session:
            return web.json_response({"status": "game_not_started"}, status=400)
        curr_time = datetime.now(timezone.utc)
        start_time = datetime.fromisoformat(session["start"])
        seconds_passed = (curr_time - start_time).total_seconds()
        if seconds_passed >= MAX_GAME_TIME:
            clear_session(session)
            return web.json_response({"status": "game_over"}, status=400)
        ship = State.from_dict(session["ship"])
        tries = session["tries"]
        form = await request.post()
        point = np.array([float(form["x"]), float(form["y"])])

        while ship.time + GAME_DT < seconds_passed:
            new_ship = random_step(ship, SHIP_SPEED, GAME_DT)
            print(f"Stepping the ship, old position: {ship.position}, new position: {new_ship.position}")
            ship = new_ship

        if (ship.position > point - ROCKET_SIZE / 2).all() and (ship.position < point + ROCKET_SIZE / 2).all():
            clear_session(session)
            return web.json_response({"status": "hit", "treasure": get_flag(token)})
        elif tries <= 1:
            clear_session(session)
            return web.json_response({"status": "rockets_ran_out"})
        else:
            tries -= 1
            session["ship"] = ship.to_dict()
            session["tries"] = tries
            distance = np.linalg.norm(ship.position - point)
            return web.json_response({
                "status": "miss",
                "time_passed": seconds_passed,
                "tries_left": tries,
                "distance": distance,
            })

    app.add_routes(routes)

    aiohttp_session.setup(app, EncryptedCookieStorage(base64.b64decode(COOKIE_SECRET)))
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
        web.run_app(app, path=os.path.join(STATE_DIR, 'battleship.sock'))


if __name__ == '__main__':
    start()
