import base64
import json
import sys

if len(sys.argv) < 2:
    print("Usage: decrypt.py private_key")
    sys.exit(1)

print("RRSSA DECODER", file=sys.stderr, flush=True)
print("=============", file=sys.stderr, flush=True)
print("WARNING! This script might work slowly, please wait patiently and don't interrupt the execution!", file=sys.stderr, flush=True)

print("Enter your encrypted data: ", end="", file=sys.stderr, flush=True)

encrypted_data = list(map(int, input().split()))
with open(sys.argv[1], "rb") as f:
    key = json.loads(base64.b64decode(f.read()))

print("Your data is: ", end='', file=sys.stderr, flush=True)

for a, (b, n), (c, d) in zip(
    encrypted_data,
    key["common_key"],
    key["private_key"]
):
    x = (a ** b) ** (c ** d)
    c1 = chr((x % n) % 256)
    c2 = chr((x % n) // 256 % 256)
    c3 = chr((x % n) // 65536)

    print(c3, c2, c1, sep='', end='', flush=True)

print(flush=True)

print("Decoding finished!", file=sys.stderr, flush=True)
