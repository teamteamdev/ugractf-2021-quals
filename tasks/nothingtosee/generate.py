import hmac
import sys
import json
import OpenSSL
from OpenSSL import crypto
import os
import tempfile

PREFIX = 'ugra_v1_p0sm0tr3l1_'
SECRET1 = b"71A4f8fdE203ab7D"
SALT1_SIZE = 16
SECRET2 = b'810adD012KSDAl10'
SALT2_SIZE = 12


def get_user_tokens():
    user_id = sys.argv[1]

    token = hmac.new(SECRET1, str(user_id).encode(), 'sha256').hexdigest()[:SALT1_SIZE]
    flag = PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]

    return token, flag


def generate():
    if len(sys.argv) < 3:
        print('Usage: generate.py user_id target_dir', file=sys.stderr)
        sys.exit(1)

    token, flag = get_user_tokens()

    json.dump({
        'flags': [flag],
        'substitutions': {},
        'urls': [f'https://{token}.nothing.{{hostname}}']
    }, sys.stdout)


if __name__ == '__main__':
    generate()
