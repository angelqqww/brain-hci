"""Launch Angela Wang's website on a local server.

Usage:
    python3 main.py

Serves this project folder at http://localhost:<port>/ and opens the site
in the default browser. Uses only the Python standard library, so there is
nothing to install. Press Ctrl+C to stop the server.
"""

import functools
import http.server
import os
import sys
import threading
import urllib.parse
import webbrowser

PAGE = "Angela Wang.html"   # the page to open
HOST = "127.0.0.1"          # only this computer can reach the server
PREFERRED_PORT = 8000

# Serve files from the folder this script lives in, no matter where it's run from
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def make_server():
    """Start on the preferred port, or fall back to any free port if it's taken."""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=PROJECT_DIR
    )
    try:
        return http.server.ThreadingHTTPServer((HOST, PREFERRED_PORT), handler)
    except OSError:
        print(f"Port {PREFERRED_PORT} is busy, picking a free port instead.")
        return http.server.ThreadingHTTPServer((HOST, 0), handler)


def main():
    if not os.path.isfile(os.path.join(PROJECT_DIR, PAGE)):
        sys.exit(f"Could not find '{PAGE}' in {PROJECT_DIR}")

    server = make_server()
    port = server.server_address[1]
    url = f"http://localhost:{port}/{urllib.parse.quote(PAGE)}"

    print(f"Serving {PROJECT_DIR}")
    print(f"Open {url}")
    print("Press Ctrl+C to stop.")

    # Open the browser shortly after the server starts listening
    threading.Timer(0.5, webbrowser.open, args=(url,)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
