#!/usr/bin/env python3

import hashlib
import hmac
import json
import os
import shutil
import subprocess
import sys
import tempfile

PREFIX = "ugra_from_friendship_in_sports_to_the_world_on_the_land_"
SECRET1 = b"cu1aj9eeLohPh4ge"
SALT1_SIZE = 16
SECRET2 = b"ohf4achah5quai6A"
SALT2_SIZE = 12
SECRET3 = b"Ohvaz3iJi8Aetahh"


def get_user_tokens():
    user_id = sys.argv[1]

    token = hmac.new(SECRET1, str(user_id).encode(), "sha256").hexdigest()[:SALT1_SIZE]
    flag = PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]

    return token, flag


def _code(i, user_id):
    h = hashlib.sha1(repr((i, user_id)).encode() + SECRET3).hexdigest()
    sig = hmac.new(SECRET3, h.encode(), "sha256").hexdigest()
    return h + sig


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    token, flag = get_user_tokens()

    json.dump({
        "flags": [flag],
        "substitutions": {("code%d" % i): _code(i, sys.argv[1]) for i in range(8)},
        "urls": [f"https://dreamteam.{{hostname}}/{token}/gGeQ3Et32Jw.jpg",
                 f"https://dreamteam.{{hostname}}/{token}/"]
    }, sys.stdout)

if __name__ == "__main__":
    generate()
