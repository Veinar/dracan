import os
import pytest
import requests
import time
from threading import Thread
from dracan.core.app_factory import create_app

def start_dracan_with_env(env_vars):
    """
    Start Dracan app with specified environment variables.
    """
    for key, value in env_vars.items():
        os.environ[key] = value

    app = create_app()
    thread = Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": 5000})
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Allow the server time to start
    return thread

def stop_dracan_server(thread):
    """
    Stop the Dracan app server.
    """
    if thread.is_alive():
        thread.join(timeout=1)
    
    if "ALLOW_METRICS_ENDPOINT" in os.environ:
        del os.environ["ALLOW_METRICS_ENDPOINT"]
    if "METRICS_PORT" in os.environ:
        del os.environ["METRICS_PORT"]

def test_metrics_default_port_enabled():
    """
    Test that the metrics server is running on the default port if enabled.
    """
    thread = start_dracan_with_env({
        "ALLOW_METRICS_ENDPOINT": "true"
    })

    try:
        response = requests.get("http://127.0.0.1:9100/metrics")
        assert response.status_code == 200
    finally:
        stop_dracan_server(thread)

def test_metrics_custom_port_enabled():
    """
    Test that metrics start on a custom port if specified.
    """
    thread = start_dracan_with_env({
        "ALLOW_METRICS_ENDPOINT": "true",
        "METRICS_PORT": "2000"
    })

    try:
        response = requests.get("http://127.0.0.1:2000/metrics")
        assert response.status_code == 200
    finally:
        stop_dracan_server(thread)

def test_metrics_data_gathering():
    """
    Test that metrics data is gathered when requests are made to the Dracan app.
    """
    # Start Dracan app with metrics enabled on default port
    thread = start_dracan_with_env({
        "ALLOW_METRICS_ENDPOINT": "true"
    })

    try:
        # Make some requests to the main Dracan app (proxy routes)
        requests.get("http://127.0.0.1:5000/")
        requests.post("http://127.0.0.1:5000/data", json={"name": "Alice"})
        
        # Fetch metrics data from the metrics endpoint
        metrics_response = requests.get("http://127.0.0.1:9100/metrics")
        assert metrics_response.status_code == 200

        # Check that some metrics are being gathered (look for request count or latency data)
        metrics_data = metrics_response.text
        assert "http_requests_total" in metrics_data  # Ensure request count metric is present
        assert "http_response_size_bytes_sum" in metrics_data  # Check latency metric presence
        assert "GET" in metrics_data or "POST" in metrics_data  # Confirm that methods used are tracked

    finally:
        stop_dracan_server(thread)

def test_metrics_data_gathering_custom_port():
    """
    Test that metrics data is gathered when requests are made to the Dracan app.
    """
    # Start Dracan app with metrics enabled on default port
    thread = start_dracan_with_env({
        "ALLOW_METRICS_ENDPOINT": "true",
        "METRICS_PORT": "2000"
    })

    try:
        # Make some requests to the main Dracan app (proxy routes)
        requests.get("http://127.0.0.1:5000/")
        requests.post("http://127.0.0.1:5000/data", json={"name": "Alice"})
        
        # Fetch metrics data from the metrics endpoint
        metrics_response = requests.get("http://127.0.0.1:2000/metrics")
        assert metrics_response.status_code == 200

        # Check that some metrics are being gathered (look for request count or latency data)
        metrics_data = metrics_response.text
        assert "http_requests_total" in metrics_data  # Ensure request count metric is present
        assert "http_response_size_bytes_sum" in metrics_data  # Check latency metric presence
        assert "GET" in metrics_data or "POST" in metrics_data  # Confirm that methods used are tracked

    finally:
        stop_dracan_server(thread)
