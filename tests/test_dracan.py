import pytest
import requests
import time
from threading import Thread
from dracan.core.app_factory import create_app
from tests.destination_mock import app as mock_app

# Set up the mock destination server in a separate thread
@pytest.fixture(scope="module", autouse=True)
def run_mock_server():
    mock_thread = Thread(target=mock_app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    mock_thread.daemon = True
    mock_thread.start()
    try:
        time.sleep(2)  # Wait for the mock server to start
        yield  # Run tests
    finally:
        mock_thread.join(timeout=1)

# Set up the Dracan proxy server in a separate thread
@pytest.fixture(scope="module")
def run_dracan_server():
    dracan_app = create_app()
    dracan_thread = Thread(target=dracan_app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    dracan_thread.daemon = True
    dracan_thread.start()
    try:
        time.sleep(2)  # Wait for Dracan to start
        yield  # Run tests
    finally:
        dracan_thread.join(timeout=1)

# Test cases for Dracan proxy server with destination_mock app

def test_health_check(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.get("http://127.0.0.1:5000/health", headers=headers, timeout=5)
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy', 'message': 'Server is running smoothly'}

def test_post_valid_json(run_dracan_server):
    valid_data = {"name": "John", "age": 30}
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["received_data"] == valid_data

def test_post_invalid_json(run_dracan_server):
    invalid_data = {"name": "John"}  # Missing "age"
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.post("http://127.0.0.1:5000/data", json=invalid_data, headers=headers, timeout=5)
    assert response.status_code == 400
    assert "Invalid JSON" in response.json()["error"]

def test_put_valid_json(run_dracan_server):
    valid_data = {"name": "Doe", "age": 25}
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.put("http://127.0.0.1:5000/update", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 200
    assert response.json()["status"] == "updated"
    assert response.json()["update_info"] == valid_data

def test_put_invalid_json(run_dracan_server):
    invalid_data = {"name": "Doe"}  # Missing "age"
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.put("http://127.0.0.1:5000/update", json=invalid_data, headers=headers, timeout=5)
    assert response.status_code == 400
    assert "Invalid JSON" in response.json()["error"]

def test_delete_request(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.delete("http://127.0.0.1:5000/delete", headers=headers, timeout=5)
    assert response.status_code == 204

def test_header_validation(run_dracan_server):
    valid_data = {"name": "Jane", "age": 28}
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 201

def test_payload_size_limiting(run_dracan_server):
    oversized_data = {"name": "A" * 2048, "age": 30}  # Exceeds max payload size of 1024 bytes
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.post("http://127.0.0.1:5000/data", json=oversized_data, headers=headers, timeout=5)
    assert response.status_code == 413  # Expecting 413 Payload Too Large

def test_missing_required_header(run_dracan_server):
    """Test request missing a required header"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {"Content-Type": "application/json"}  # Missing "X-API-KEY" and "Authorization"
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 403
    assert "Missing required header" in response.json()["error"]

def test_incorrect_required_header_value(run_dracan_server):
    """Test request with an incorrect value for a required header"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "wrong_key",
        "Authorization": "Bearer token123.abc.xyz"
    }
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 201

def test_prohibited_header_present(run_dracan_server):
    """Test request with a prohibited header present"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "test_key",
        "Authorization": "Bearer token123.abc.xyz",
        "X-Internal-Header": "should_not_be_here"  # Prohibited header
    }
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 403
    assert "Prohibited header" in response.json()["error"]

def test_wildcard_header_value(run_dracan_server):
    """Test request with wildcard value for a required header"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "any_value",  # Allowed due to wildcard
        "Authorization": "Bearer token123.abc.xyz"
    }
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 201
    assert response.json()["status"] == "success"

def test_regex_header_value(run_dracan_server):
    """Test request with a header matching the regular expression"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "test_key",
        "Authorization": "Bearer token123.abc.xyz"  # Matches regex pattern
    }
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 201
    assert response.json()["status"] == "success"

def test_regex_header_value_invalid(run_dracan_server):
    """Test request with a header that does not match the regular expression"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "test_key",
        "Authorization": "InvalidToken"  # Does not match regex pattern
    }
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 403
    assert "Invalid header" in response.json()["error"]

def test_no_headers_when_all_required(run_dracan_server):
    """Test request without any headers when headers are required"""
    valid_data = {"name": "Jane", "age": 28}
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, timeout=5)
    assert response.status_code == 403
    assert "Missing required header" in response.json()["error"]

def test_extra_headers_allowed(run_dracan_server):
    """Test request with extra headers that are neither required nor prohibited"""
    valid_data = {"name": "Jane", "age": 28}
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "test_key",
        "Authorization": "Bearer token123.abc.xyz",
        "X-Custom-Header": "extra_header_value"  # Extra header, should be ignored
    }
    response = requests.post("http://127.0.0.1:5000/data", json=valid_data, headers=headers, timeout=5)
    assert response.status_code == 201
    assert response.json()["status"] == "success"

# Testing unsupported HTTP methods on the /health endpoint
def test_unsupported_methods_on_health(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    url = "http://127.0.0.1:5000/health"

    # PATCH
    response = requests.patch(url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

    # HEAD
    response = requests.head(url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

    # TRACE
    response = requests.request("TRACE", url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

    # CONNECT (Using a low-level request for unsupported method)
    response = requests.request("CONNECT", url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed


# Testing unsupported HTTP methods on the /data endpoint
def test_unsupported_methods_on_data(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    url = "http://127.0.0.1:5000/data"

    # PATCH
    response = requests.patch(url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

    # HEAD
    response = requests.head(url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

    # TRACE
    response = requests.request("TRACE", url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

    # CONNECT
    response = requests.request("CONNECT", url, headers=headers, timeout=5)
    assert response.status_code == 405  # Method Not Allowed

def test_root_get_request(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.get("http://127.0.0.1:5000/", headers=headers, timeout=5)
    assert response.status_code == 200
    assert response.json() == {'status': 'root accessed', 'method': 'GET'}

def test_root_post_request(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    data = {"name": "Jane", "age": 28}
    response = requests.post("http://127.0.0.1:5000/", json=data, headers=headers, timeout=5)
    assert response.status_code == 201
    assert response.json() == {'status': 'root accessed', 'method': 'POST', 'received_data': data}

def test_root_put_request(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    data = {"name": "Jane", "age": 29}
    response = requests.put("http://127.0.0.1:5000/", json=data, headers=headers, timeout=5)
    assert response.status_code == 200
    assert response.json() == {'status': 'root accessed', 'method': 'PUT', 'update_info': data}
    
def test_root_delete_request(run_dracan_server):
    headers = {"Content-Type": "application/json", "X-API-KEY": "test_key", "Authorization": "Bearer token123.abc.xyz"}
    response = requests.delete("http://127.0.0.1:5000/", headers=headers, timeout=5)
    assert response.status_code == 204