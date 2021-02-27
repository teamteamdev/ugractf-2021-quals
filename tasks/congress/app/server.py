#!/usr/bin/env python3

import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import aiosqlite

import hmac
import os
import sys
import time

from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR

PREFIX = "ugra_what_a_beautiful_number_"
TOKEN_SECRET = b"comprehensive-exploration-participate-comfortable-fashionable"
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b"deteriorate-institution-transaction-architecture-grandmother"
FLAG_SALT_SIZE = 12

cache = {}


def check_cache(token):
    current_time = time.time()
    cache.setdefault(token, [])
    local_cache = cache[token]

    while len(local_cache) > 0 and current_time - local_cache[0] > 300:
        local_cache.pop(0)

    if len(local_cache) < 5:
        local_cache.append(current_time)
        return True
    else:
        return False


def verify_token(token):
    return hmac.new(
        TOKEN_SECRET,
        token[:-TOKEN_SALT_SIZE].encode(),
        'sha256'
    ).hexdigest()[:TOKEN_SALT_SIZE] == token[-TOKEN_SALT_SIZE:]


def get_flag(token):
    return PREFIX + hmac.new(FLAG_SECRET, token.encode(), 'sha256').hexdigest()[:FLAG_SALT_SIZE]


def build_app():
    # pylint: disable=unused-variable

    app = web.Application()
    routes = web.RouteTableDef()
    routes.static('/static', 'static')


    @routes.get('/')
    async def main_page(request):
        ref = request.query.get('ref', '')
        return jinja2.render_template('main.html', request, {"ref": ref})


    @routes.get('/check')
    async def check(request):
        ref = request.query.get('ref', '')
        q = request.query.get('q', '')

        try:
            q = int(q)
        except ValueError:
            return web.json_response({
                'status': 'error',
                'error': 'Please pass a number.'
            })

        if not verify_token(ref):
            return web.json_response({
                'status': 'error',
                'error': 'You have no invitation.'
            })

        if not check_cache(ref):
            return web.json_response({
                'status': 'error',
                'error': 'Too many queries. Try again later.'
            })

        result = []

        async with aiosqlite.connect(
                f'file:{os.path.join(BASE_DIR, "oeis.sqlite")}?mode=ro',
                uri=True
        ) as db:
            async with db.execute(
                    'select seq.* from seq_items natural join seq where seq_items.number = ?',
                    (q, )
            ) as cursor:
                async for row in cursor:
                    result.append({
                        'id': row[0],
                        'desc': row[1]
                    })

        return web.json_response({
            'status': 'ok',
            'count': len(result),
            'items': result
        })


    @routes.get('/register')
    @routes.post('/register')
    async def register(request):
        ref = request.query.get('ref', '')

        if not verify_token(ref):
            return jinja2.render_template('noinvite.html', request, {})

        errors = []
        first_name = ''
        last_name = ''
        login = ''
        pin = ''

        if request.method == 'POST':
            first_name = (await request.post()).get('first_name', '')
            last_name = (await request.post()).get('last_name', '')
            login = (await request.post()).get('login', '')
            pin = (await request.post()).get('pin', '')

            if not check_cache(ref):
                errors.append('Too many requests.')
            else:
                if first_name == '' or last_name == '' or login == '':
                    errors.append('All fields are required')

                if pin == '':
                    errors.append('PIN field is required')
                elif len(pin) != 4:
                    errors.append('PIN should contain 4 characters.')
                elif pin != '9935':
                    errors.append('PIN is too easy. Enable JavaScript to see details.')

            if len(errors) == 0:
                return jinja2.render_template('personal.html', request, {
                    'ref': ref,
                    'flag': get_flag(ref),
                    'first_name': first_name,
                    'last_name': last_name
                })

        return jinja2.render_template('register.html', request, {
            'ref': ref,
            'errors': errors,
            'first_name': first_name,
            'last_name': last_name,
            'login': login,
            'pin': pin
        })


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))
    return app


def main():
    app = build_app()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(STATE_DIR, 'congress.sock'))


if __name__ == '__main__':
    main()
