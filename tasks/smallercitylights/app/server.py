#!/usr/bin/env python3

import aiohttp.web as web
import aiohttp_jinja2 as jinja2

import errno
import hashlib
import hmac
import os
import sys

from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR
TYPE = os.environ["TYPE"]  # smallercitylights or dreamteam

if TYPE == "smallercitylights":
    PREFIX = "ugra_we_will_go_we_will_swim_we_will_crawl_"
    SECRET2 = b"huZu3wop5Muich5o"
    SALT2_SIZE = 12
    SECRET3 = b"Aengo4Kuaxee7xei"
    HEIC_DATA = open("IMG_0586.HEIC", "rb").read()
    ANSWERS = {"Россия, Омская область, г. Омск, ул. Богдана Хмельницкого, д. 38"}
elif TYPE == "dreamteam":
    HEIC_DATA = None
    ANSWERS = {}

def verify_code(code):
    h, sig = code[:40], code[40:]
    signature = hmac.new(SECRET3, h.encode(), "sha256").hexdigest()
    return all(i in "0123456789abcdef" for i in code) and sig == signature


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()


    @routes.get('/{token}/IMG_0586.HEIC')
    async def heic(request):
        if HEIC_DATA:
            resp = web.StreamResponse()
            resp.headers["Content-type"] = "image/heic"
            await resp.prepare(request)
            await resp.write(HEIC_DATA)
            return resp
        else:
            raise web.NotFoundError


    @routes.get('/{token}/')
    async def main(request):
        return jinja2.render_template('main.html', request, {"type": TYPE})


    @routes.post('/{token}/check')
    async def check(request):
        token = request.match_info['token']
        data = await request.post()
        answer, code = data.get("answer", ""), data.get("code", "")
        flag = None

        if verify_code(code):
            try:
                fd = os.open(os.path.join(STATE_DIR, code), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                with os.fdopen(fd, "w") as f:
                    f.write(repr((answer, request.remote, request.headers)))

                if answer in ANSWERS:
                    status = "flag"
                    flag = get_flag(token)
                else:
                    status = "answer-wrong"
            except OSError as e:
                if e.errno == errno.EEXIST:
                    status = "code-used"
                else:
                    raise
        else:
            status = "code-wrong"

        return jinja2.render_template('main.html', request,
                                      {"type": TYPE, "status": status, "flag": flag})


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))
    return app


if __name__ == '__main__':
    app = build_app()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(STATE_DIR, TYPE + '.sock'))
