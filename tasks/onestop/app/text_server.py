#!/usr/bin/env python3

import asyncio
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import hmac
import socket


PREFIX = "ugra_soviet_technologies_are_eternal_"
TOKEN_SECRET = b"fluctuation-constellation-accumulation-architecture-refrigerator"
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b"comfortable-intermediate-battlefield-firefighter-contradiction"
FLAG_SALT_SIZE = 12


def verify_token(token):
    return True
    return hmac.new(
        TOKEN_SECRET,
        token[:-TOKEN_SALT_SIZE].encode(),
        'sha256'
    ).hexdigest()[:TOKEN_SALT_SIZE] == token[-TOKEN_SALT_SIZE:]


def get_flag(token):
    return PREFIX + hmac.new(FLAG_SECRET, token.encode(), 'sha256').hexdigest()[:FLAG_SALT_SIZE]


async def handle_flag(reader, writer):
    writer.write(b'PWD?')
    await writer.drain()
    enc_token = await reader.read(100)
    token = enc_token.decode("utf-8").strip()

    if not verify_token(token):
        writer.write(b'FATAL WRONG')
        await writer.drain()
        return

    writer.write(get_flag(token).encode())
    await writer.drain()
    writer.close()

async def main():
    sslc = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslc.load_cert_chain('server.pem')
    server = await asyncio.start_server(
        handle_flag, '127.0.0.1', 17337, ssl=sslc)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
