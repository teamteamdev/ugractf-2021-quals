#!/usr/bin/env python3

import hmac
import json
import subprocess
import random
import tempfile
import os
import re
import sys

PREFIX = "ugra_just_honk_and_bibimbap_"
SECRET = b"shohc1Dish4paepi"
SALT_SIZE = 16

MAPPING = {'_': 'K', 'a': 'E', 'b': 'W', 'd': 'B', 'g': 'L', 'h': 'J', 'i': 'U', 'j': 'P',
           'k': 'X', 'm': 'M', 'n': 'F', 'o': 'A', 'p': 'O', 'r': 'V', 's': 'G', 't': 'Z', 'u': 'H'}


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + (hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]
                     .translate("".maketrans("cef", "abd")))


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    target_dir = sys.argv[2]

    flag = get_flag()

    with open(os.path.join(target_dir, "noteasy82.txt"), "w") as f:
        f.write(flag.translate({ord(k): ord(v) for k, v in MAPPING.items()}))

    json.dump({"flags": [flag], "substitutions": {}, "urls": []}, sys.stdout)


if __name__ == "__main__":
    generate()
