#!/usr/bin/python3

import hmac
import sys

PREFIX = "ugra_said_secret_service_secretly_succumbs_"
SECRET2 = b"AiKee0Je2shi0que"
SALT2_SIZE = 12

def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]

sys.stdout.write(get_flag(sys.argv[1]))
