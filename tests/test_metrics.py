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
