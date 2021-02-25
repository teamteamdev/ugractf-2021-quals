#!/usr/bin/env python3

import hmac
import json
import subprocess
import tempfile
import base64
import glob
import os
import sys

PREFIX = "ugra_the_next_station_is_esoteric_programming_"
SECRET = b"NumPyIsLame86"
SALT_SIZE = 40 - len(PREFIX)


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 2:
        print("Usage: generate.py user_id", file=sys.stderr)
        sys.exit(1)

    flag = get_flag()
    alph = "abcdefghijklmnopqrstuvwxy_1234567890"
    
    polybius = lambda x: ''.join(map(str, (x // 6 + 1, x % 6 + 1)))
    ciphertext = ' '.join(polybius(alph.find(x)) for x in flag)

    json.dump({
        "flags": [flag],
        "substitutions": {"ciphertext", },
        "urls": []
    }, sys.stdout)


if __name__ == "__main__":
    generate()
