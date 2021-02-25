#!/usr/bin/env python3

import hmac
import json
import subprocess
import random
import tempfile
import os
import re
import sys

PREFIX = "ugra_null_pager_quad_jogger_collab_"
SECRET = b"ncu1mKqMvpleNa14"
SALT_SIZE = 12


LETTERS = { # r1, r2, p1, p2
    "_": (100, 100, -120, -60),
    "a": (100, 70, -405, 0),
    "b": (100, 20, -225, 225),
    "c": (80, 100, 45, 315),
    "d": (20, 100, 0, 405),
    "e": (20, 100, -495, 0),
    "g": (100, 20, -495, -45),
    "j": (100, 70, -90, 45),
    "l": (100, 70, 135, 270),
    "n": (90, 100, -45, 225),
    "o": (100, 100, 0, 360),
    "p": (40, 100, -180, 225),
    "q": (100, 40, -60, 360),
    "r": (100, 70, 90, 180),
    "u": (80, 100, -225, 45),
}


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + (hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]
                     .translate("".maketrans("0123456789f", "abcdeabcded")))


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    flag = get_flag()

    json.dump({
        "flags": [flag],
        "substitutions": dict(sum((
            list({
                     "r_1_%02d" % (i+1): str(LETTERS[flag[i]][0]),
                     "r_2_%02d" % (i+1): str(LETTERS[flag[i]][1]),
                     "p_1_%02d" % (i+1): str(LETTERS[flag[i]][2]),
                     "p_2_%02d" % (i+1): str(LETTERS[flag[i]][3]),
                 }.items())
            for i in range(len(flag))), [])),
        "urls": []
    }, sys.stdout)


if __name__ == "__main__":
    generate()
