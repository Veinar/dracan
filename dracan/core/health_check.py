import os
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthCheckHandler(BaseHTTPRequestHandler):
    """
    A simple HTTP request handler for health check purposes.

    This handler responds to GET requests on the root ("/") path with a JSON 
    response indicating the service is "running". Requests to any other path 
    result in a 404 Not Found response.

    Methods:
        do_get: Handles HTTP GET requests. Sends a 200 OK response with a 
                JSON payload {"status": "running"} if the path is "/".
                Otherwise, responds with a 404 Not Found.
    """
    
    def log_message(self, format, *args):
        """Override to disable logging of HTTP requests in console."""
        pass

    def do_GET(self):
        if self.path == "/":
            # Send a 200 OK response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Write JSON response
            response = json.dumps({"status": "running"})
            self.wfile.write(response.encode())
        else:
            # Send a 404 Not Found response for other paths
            self.send_response(404)
            self.end_headers()

def run_health_check_server():
    health_port = int(os.getenv("HEALTHCHECK_PORT", 9000))
    server_address = ('', health_port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    # Get the current timestamp and print the message with date and time (emulate logger for information about setting up HC)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    print(f"{timestamp} [INFO] Health check server running on port {health_port}")
    httpd.serve_forever()
