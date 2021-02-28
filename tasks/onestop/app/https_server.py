#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os

os.chdir("public")
httpd = HTTPServer(('localhost', 17443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="../server.pem", server_side=True)
print("Serving")
httpd.serve_forever()
