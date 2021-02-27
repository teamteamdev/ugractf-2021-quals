#!/usr/bin/env python3

import asyncio
import itertools
import hmac
import os
import pyqrcode
import random
import socket
import sys


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


def log(message, client=None):
    if client:
        message = f'soviet:[sess-{id(client)}] {message}'
    else:
        message = f'soviet: {message}'
    print(message, file=sys.stderr)


async def handle_client(loop, client):
    try:
        await loop.sock_sendall(client, b'PWD?\n')
        token = b''
        while b'\n' not in token and len(token) < 64:
            token += (await loop.sock_recv(client, 64))
        token = token.decode()

        if not verify_token(token.strip()):
            log(f'Invalid token: {token.encode()}')
            await loop.sock_sendall(client, b'FATAL WRONG')
            return

        log(f'Token: {token}', client)

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

        await loop.sock_sendall(client, bytearray(encoded_code))
    except socket.error as e:
        log(f'Connection broken: {e}', client)
    except UnicodeDecodeError as e:
        log('Client set badly encoded data', client)
    finally:
        log('Connection closed', client)
        client.close()


async def run_server(loop):
    if 'LOCAL' in os.environ:
        if len(sys.argv) < 2:
            port = 7777
        else:
            port = int(sys.argv[1])
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', port))
        log(f'Server started on 0.0.0.0:{port}')
    else:
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        if len(sys.argv) < 2:
            print('Usage: server.py pathto.sock')
            sys.exit(1)

        path = os.path.join(sys.argv[1], 'soviet.sock')
        log(f'Starting server on {path}')
        server.bind(path)
    server.listen(8)
    server.setblocking(False)

    try:
        while True:
            client, (host, port) = await loop.sock_accept(server)
            log(f'Accepted a connection from {host}:{port}', client)
            loop.create_task(handle_client(loop, client))
    finally:
        log(f'Stopping server gracefully')
        server.close()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server(loop))


if __name__ == '__main__':
    main()
