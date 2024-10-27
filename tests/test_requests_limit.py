import requests
import time
import pytest
from threading import Thread
from dracan.core.app_factory import create_app
from tests.destination_mock import app as mock_app

# Set up the mock destination server in a separate thread
@pytest.fixture(scope="module", autouse=True)
def run_mock_server():
    mock_thread = Thread(target=mock_app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    mock_thread.daemon = True
    mock_thread.start()
    time.sleep(1)  # Give the mock server time to start
    yield
    mock_thread.join(timeout=1)

# Set up the Dracan proxy server in a separate thread
@pytest.fixture(scope="module")
def run_dracan_server():
    dracan_app = create_app()
    dracan_thread = Thread(target=dracan_app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    dracan_thread.daemon = True
    dracan_thread.start()
    time.sleep(1)  # Give Dracan server time to start
    yield
    dracan_thread.join(timeout=1)

# Test for rate limiting specifically
def test_rate_limiting(run_dracan_server):
    url = "http://127.0.0.1:5000/health"
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}

    # Exceed the rate limit of 20 per minute by sending more than 20 requests within a minute
    exceeded_rate = False
    for i in range(25):
        response = requests.get(url, headers=headers)
        if response.status_code == 429:  # Rate limit exceeded
            exceeded_rate = True
            break
        time.sleep(1.5)  # Slightly delay each request to stay within range of 20/minute

    # Confirm that we did indeed exceed the rate limit
    assert exceeded_rate, "Rate limiting did not trigger as expected after 20 requests."

    # Wait a little over the rate limit reset period to verify that requests succeed afterward
    time.sleep(61)  # Waiting 61 seconds to ensure the limit resets
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Request did not succeed after rate limit reset."
