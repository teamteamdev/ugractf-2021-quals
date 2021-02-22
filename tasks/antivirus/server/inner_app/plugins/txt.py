import re

VIRUS_SIGNATURES = [
    "virus",
    "trojan",
    "malware",
    "spyware",
    "miner",
    "вирус",
    "троян",
    "вредоносное",
    "шпионское",
]

def check(path):
    with open(path) as f:
        data = f.read()
        for sign in VIRUS_SIGNATURES:
            if sign in data:
                return sign
