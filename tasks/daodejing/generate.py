#!/usr/bin/env python3

import hmac
import json
import subprocess
import random
import tempfile
import os
import re
import sys

PREFIX = "ugra_grandpa_take_your_pills_or_we_will_beat_up_your_"
SECRET = b"znO3n2w0bAq1LzzD"
SALT_SIZE = 16


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    target_dir = sys.argv[2]

    flag = get_flag()

    data = open(os.path.join("private", "template.svg")).read().replace("+++FLAG+++", flag)
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "f.svg"), "w") as f:
            f.write(data)

        subprocess.check_call("""inkscape --without-gui f.svg
                                --verb=EditSelectAll
                                --verb=ObjectToPath
                                --verb=SelectionCombine
                                --verb=FileSave
                                --verb=FileQuit
                              """.replace("\n", ""), shell=True, cwd=temp_dir)

        with open(os.path.join(target_dir, "daodejing.txt"), "w") as f:
            svg = open(os.path.join(temp_dir, "f.svg")).read()
            f.write(re.compile(' d="(.*?)"').findall(svg)[-1])

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": []
    }, sys.stdout)


if __name__ == "__main__":
    generate()
