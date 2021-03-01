#!/usr/bin/env python3

import hashlib
import hmac
import json
import os
import shutil
import subprocess
import sys
import tempfile

PREFIX = "ugra_said_secret_service_secretly_succumbs_"
SECRET1 = b"Duyaiquaeboop1ye"
SALT1_SIZE = 16
SECRET2 = b"AiKee0Je2shi0que"
SALT2_SIZE = 12


def get_user_tokens():
    user_id = sys.argv[1]

    token = hmac.new(SECRET1, str(user_id).encode(), "sha256").hexdigest()[:SALT1_SIZE]
    flag = PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]

    return token, flag


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    token, flag = get_user_tokens()

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": [f"https://compliance.{{hostname}}/{token}/"]
    }, sys.stdout)

if __name__ == "__main__":
    generate()
