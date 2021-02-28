#!/usr/bin/env python3

import hmac
import json
import sys

PREFIX = "ugra_social_services_for_the_masses_"
TOKEN_SECRET = b"qpSRnuFNG7bhs4Sk"
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b"FX75zyKrr58f9fqq"
FLAG_SALT_SIZE = 12


def get_token():
    user_id = sys.argv[1]

    token1 = hmac.new(TOKEN_SECRET, str(user_id).encode(), "sha256").hexdigest()[:TOKEN_SALT_SIZE]
    token2 = hmac.new(TOKEN_SECRET, token1.encode(), "sha256").hexdigest()[:TOKEN_SALT_SIZE]
    
    return token1 + token2


def get_flag(token):
    return PREFIX + hmac.new(FLAG_SECRET, token.encode(), "sha256").hexdigest()[:FLAG_SALT_SIZE]


def generate():
    if len(sys.argv) < 2:
        print("Usage: generate.py user_id ...", file=sys.stderr)
        sys.exit(1)

    token = get_token()

    json.dump({
        "flags": [get_flag(token)],
        "substitutions": {},
        "urls": [f"https://onestop.{{hostname}}"]
        "bullets": [
            f"Пароль: <code>{token}</code>"
        ]
    }, sys.stdout)


if __name__ == "__main__":
    generate()
