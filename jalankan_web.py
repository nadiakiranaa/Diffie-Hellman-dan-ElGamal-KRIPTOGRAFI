#!/usr/bin/env python3
# Menjalankan versi web lokal: python jalankan_web.py
# Hanya memakai library standar Python (http.server, webbrowser).
import http.server, socketserver, threading, webbrowser, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}/dh_elgamal.html"
    print(f"Server jalan di {url}\nTekan Ctrl+C untuk berhenti.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nBerhenti.")
