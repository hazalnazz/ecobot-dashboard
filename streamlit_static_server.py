"""
Helper script to serve static files (like 3D models) for Streamlit.
Run this in a separate terminal: python streamlit_static_server.py
"""

import http.server
import socketserver
from pathlib import Path
import sys

# Get the directory containing this script, which should be the project root
# Use Path(__file__).parent for robustness
try:
    base_dir = Path(__file__).parent.absolute()
except NameError:
     # Handle cases where __file__ is not defined (e.g., interactive interpreter)
     base_dir = Path('.').absolute()


PORT = 8502  # Default Streamlit port, ensure it doesn't clash if Streamlit uses another
DIRECTORY = base_dir  # Serve files from the project root

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs) # Pass directory explicitly

    def end_headers(self):
        # Add CORS headers - Allow requests from any origin for local dev
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200, "ok")
        self.end_headers()

    def log_message(self, format, *args):
        # Quieter logging or customize as needed
        # print(f"StaticServer: {self.path} - Status: {args[1]}")
        pass # Suppress most logs unless it's an error

    def log_error(self, format, *args):
        # Log errors to stderr
        print(f"StaticServerError: {format % args}", file=sys.stderr)


def run_server(port=PORT):
    # Check if port is already in use (basic check)
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving static files from '{DIRECTORY}' on http://localhost:{port}")
            print("Press Ctrl+C to stop the server.")
            httpd.serve_forever()
    except OSError as e:
        if "address already in use" in str(e).lower():
            print(f"Error: Port {port} is already in use.", file=sys.stderr)
            print("Please stop the other process using this port or choose a different port.", file=sys.stderr)
            print(f"Ensure STATIC_SERVER_URL in config.py matches the port (currently set for {port}).", file=sys.stderr)
        else:
            print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStatic server stopped.")
        sys.exit(0)


if __name__ == "__main__":
    # You could add argparse here to allow changing the port via command line
    run_server(port=PORT)
