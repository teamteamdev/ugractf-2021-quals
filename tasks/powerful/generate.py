#!/usr/bin/env python3

import base64
import hmac
import json
import math
import os
import random
import sys

PREFIX = "ugra_it_is_too_powerful_rsa_right_"
SECRET = b"indication-strength-nominate-knowledge-security"
SALT_SIZE = 11

def get_flag(user_id):
    return PREFIX + hmac.new(SECRET, user_id.encode(), "sha256").hexdigest()[:SALT_SIZE]


def get_phi(n):
    phi = int(n > 1 and n)
    for p in range(2, int(n ** .5) + 1):
        if not n % p:
            phi -= phi // p
            while not n % p:
                n //= p
    if n > 1:
        phi -= phi // n
    return phi


def solve(a, b):
    # find solution for ax + by == 1 that 0 < x < n

    if a == 0:
        return (0, 1)

    x, y = solve(b % a, a)
    x, y = y - (b // a) * x, x

    while x < 0:
        x += b
        y -= a

    return (x, y)


def inverse(a, n):
    x, _ = solve(a, n)
    return x


def is_prime(n):
    # Base check

    prime_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                  59, 61, 67, 71, 73, 79, 83, 89, 97]

    for prime in prime_list:
        if n % prime == 0:
            return False

    # Miller-Rabin primality test

    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for _ in range(128):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False

    return True


def generate_prime_number(length):
    found_prime = False

    while not found_prime:
        p = random.getrandbits(length)
        p |= (1 << length - 1) | 1

        found_prime = is_prime(p)

    return p


def encrypt(x):
    three = random.randint(0, 1)
    while True:
        p = generate_prime_number(13 if three == 1 else 9)
        q = generate_prime_number(13 if three == 1 else 9)
        r = 1 if three == 1 else generate_prime_number(8)

        if p == q or q == r or r == p:
            continue

        n = p * q * r
        phi = (p - 1) * (q - 1) * max(r - 1, 1)
        break

    while True:
        c = random.randint(phi // 4, phi - 1)
        d = random.randint(phi // 4, phi - 1)
        e = pow(c, d, phi)
        if math.gcd(e, phi) != 1:
            continue

        ie = inverse(e, phi)
        ab = pow(x, ie, n)
        break

    while True:
        ib = random.randint(3, phi - 1)
        if math.gcd(ib, phi) != 1:
            continue

        b = inverse(ib, phi)
        a = pow(ab, ib, n)
        break

    return a, (b, n), (c, d)


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir <...>", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    target_dir = sys.argv[2]

    random.seed(hmac.new(SECRET, user_id.encode(), "sha256").digest())
    flag = get_flag(user_id)

    dump = {
        "common_key": [(1, 50041451)],
        "private_key": [(1, 1)]
    }
    encrypted_flag = [7694194]

    for c1, c2, c3 in zip(flag[3::3], flag[4::3], flag[5::3]):
        x = 65536 * ord(c1) + 256 * ord(c2) + ord(c3)

        e, common, private = encrypt(x)

        encrypted_flag.append(e)
        dump["common_key"].append(common)
        dump["private_key"].append(private)

    with open(os.path.join(target_dir, "powerful.key"), "wb") as f:
        f.write(base64.b64encode(json.dumps(dump).encode()))

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": [],
        "bullets": [f"Флаг: <code>{' '.join(map(str, encrypted_flag))}</code>"]
    }, sys.stdout)


if __name__ == "__main__":
    generate()
