#!/usr/bin/env python3

import hmac
import json
import sys

PREFIX = "ugra_what_a_beautiful_number_"
TOKEN_SECRET = b"comprehensive-exploration-participate-comfortable-fashionable"
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b"deteriorate-institution-transaction-architecture-grandmother"
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
        "urls": [
            f"https://congress.{{hostname}}/?ref={token}"
        ]
    }, sys.stdout)


if __name__ == "__main__":
    generate()
