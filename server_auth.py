#!/usr/bin/env python3
"""Simple HTTP server with basic auth."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import hashlib
import base64

HOST = '0.0.0.0'
PORT = 8080

# Simple auth: user=admin, password=agents2024
VALID_USERS = {
    b'admin': b'5e884898da28047dcf1b7ea3c2bb8f7a'  # sha256 of "agents2024"
}

class AuthHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get('Authorization', '')
        if not auth.startswith('Basic '):
            self.send_auth()
            return
        
        try:
            encoded = auth[6:]
            decoded = base64.b64decode(encoded).decode()
            user, pw = decoded.split(':', 1)
            user_b = user.encode()
            pw_hash = hashlib.sha256(pw.encode()).hexdigest()
            
            if user_b in VALID_USERS and VALID_USERS[user_b].encode() == pw_hash.encode():
                super().do_GET()
                return
        except:
            pass
        
        self.send_auth()
    
    def send_auth(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Agents"')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Auth required</h1></body></html>')

print(f"Starting server on {HOST}:{PORT}")
HTTPServer((HOST, PORT), AuthHandler).serve_forever()
