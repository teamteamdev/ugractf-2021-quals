#!/usr/bin/env python3

import hmac
import json
import subprocess
import tempfile
import base64
import glob
import os
import sys

PREFIX = "ugra_not_as_easy_as_it_used_to_be"
SECRET = b"tbsVmqAAt2fnnGwD"
SALT_SIZE = 40 - len(PREFIX)


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    target_dir = sys.argv[2]

    flag = get_flag()

    image_files = os.path.join("private", "image")
    image_tmp = os.path.join(tempfile.gettempdir(), "image.iso")
    subprocess.run(["mkisofs", "-R", "-J", "-V", "My files", "-o", image_tmp, image_files], check=True)
    with open(image_tmp, "rb") as f:
        image_data = f.read()

    encoded_flag = base64.b32encode(flag.encode("utf-8")).decode("utf-8")
    for i, file in enumerate(glob.glob(os.path.join(image_files, "*"))):
        name, ext = os.path.splitext(os.path.basename(file))
        short_name = (name[:8] + ext[:4]).upper().replace("-", "_")
        part_name = encoded_flag[:8]
        encoded_flag = encoded_flag[8:]
        if len(part_name) != 8:
            raise RuntimeError("Invalid encoded string size")
        fname = "{}.{:03d}".format(part_name[:8], i)
        # print(f"Writing part of flag {part_name}, remaining {encoded_flag}, replacing {short_name} with {fname}")
        image_data = image_data.replace(short_name.encode("utf-8"), fname.encode("utf-8"))
    if len(encoded_flag) != 0:
        raise RuntimeError("Invalid encoded string size")

    image_path = os.path.join(target_dir, "image.iso")
    with open(image_path, "wb") as f:
        f.write(image_data)

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": []
    }, sys.stdout)


if __name__ == "__main__":
    generate()
