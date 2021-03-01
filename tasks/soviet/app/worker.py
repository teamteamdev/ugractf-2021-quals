#!/usr/bin/env python3

import itertools
import hmac
import random
import sys

import pyqrcode

sys.stdout.reconfigure(encoding='cp866')


PREFIX = "ugra_soviet_technologies_are_eternal_"
TOKEN_SECRET = b"fluctuation-constellation-accumulation-architecture-refrigerator"
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b"comfortable-intermediate-battlefield-firefighter-contradiction"
FLAG_SALT_SIZE = 12


def add_noise(code):
    code = [list(line) for line in code]
    size = len(code)

    for _ in range(64):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)

        if (y < 15 and (x < 15 or x >= size - 11) or
                y >= size - 15 and (x < 15 or x >= size - 15)):
            continue

        code[x][y] = '1' if code[x][y] == '0' else '0'

    return code


def verify_token(token):
    return hmac.new(
        TOKEN_SECRET,
        token[:-TOKEN_SALT_SIZE].encode(),
        'sha256'
    ).hexdigest()[:TOKEN_SALT_SIZE] == token[-TOKEN_SALT_SIZE:]


def get_flag(token):
    return PREFIX + hmac.new(FLAG_SECRET, token.encode(), 'sha256').hexdigest()[:FLAG_SALT_SIZE]


def main():
    print('PWD?', flush=True)
    token = input().strip()

    if not verify_token(token):
        print('FATAL WRONG', flush=True)
        return

    code = add_noise(pyqrcode.create(
        get_flag(token),
        error='H'
    ).text(quiet_zone=0).split())

    size = len(code)

    encoded_code = []

    for line_top, line_bottom in itertools.zip_longest(
            code[0::2], code[1::2],
            fillvalue='0'*size
    ):
        for char_top, char_bottom in itertools.zip_longest(
                line_top, line_bottom,
                fillvalue='0'
        ):
            if char_top == char_bottom == '1':
                encoded_code.append(0xdb)
            elif char_top == char_bottom == '0':
                encoded_code.append(0x20)
            elif char_top == '1':
                encoded_code.append(0xdf)
            else:
                encoded_code.append(0xdc)

    print(bytearray(encoded_code).decode('cp866'), end='', flush=True)


if __name__ == '__main__':
    main()
