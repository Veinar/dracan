import pytest
import requests
import time
from threading import Thread
from http.server import HTTPServer
from dracan.core.health_check import HealthCheckHandler  # Adjust import based on your structure

@pytest.fixture(scope="module")
def run_health_check_server():
    """
    Fixture to start the HealthCheckHandler server in a separate thread.
    """
    server_address = ('', 9000)  # Use the correct port for your setup
    httpd = HTTPServer(server_address, HealthCheckHandler)
    
    thread = Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    
    time.sleep(1)  # Give the server a moment to start
    yield  # Run tests
    httpd.shutdown()
    thread.join()

def test_health_check_status(run_health_check_server):
    """
    Test that the health check endpoint returns a 200 status.
    """
    response = requests.get("http://127.0.0.1:9000/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_health_check_response(run_health_check_server):
    """
    Test that the health check endpoint returns the expected JSON response.
    """
    response = requests.get("http://127.0.0.1:9000/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == {"status": "running"}

def test_health_check_invalid_path(run_health_check_server):
    """
    Test that a request to an invalid path returns a 404 status.
    """
    response = requests.get("http://127.0.0.1:9000/invalid-path")
    assert response.status_code == 404
