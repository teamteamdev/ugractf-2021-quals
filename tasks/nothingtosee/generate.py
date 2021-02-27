#!/usr/bin/env python3

import hmac
import sys
import json

PREFIX = 'ugra_v1_p0sm0tr3l1_'
TOKEN_SECRET = b"71A4f8fdE203ab7D"
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b'810adD012KSDAl10'
FLAG_SALT_SIZE = 12


def get_token():
    user_id = sys.argv[1]

    token1 = hmac.new(TOKEN_SECRET, str(user_id).encode(), "sha256").hexdigest()[:TOKEN_SALT_SIZE]
    token2 = hmac.new(TOKEN_SECRET, token1.encode(), "sha256").hexdigest()[:TOKEN_SALT_SIZE]

    return token1 + token2


def get_flag(token):
    return PREFIX + hmac.new(FLAG_SECRET, token.encode(), "sha256").hexdigest()[:FLAG_SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print('Usage: generate.py user_id target_dir', file=sys.stderr)
        sys.exit(1)

    token = get_token()
    flag = get_flag(token)

    json.dump({
        'flags': [flag],
        'substitutions': {},
        'urls': [f'https://{token}.nothing.{{hostname}}']
    }, sys.stdout)


if __name__ == '__main__':
    generate()
