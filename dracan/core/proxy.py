import json
import os
import requests
from flask import request, jsonify, current_app as app

# Set a default timeout in seconds if PROXY_TIMEOUT is not specified in the environment
PROXY_TIMEOUT = int(os.getenv("PROXY_TIMEOUT", 180))

# Load the proxy configuration from the JSON file
def load_proxy_config(file_path='proxy_config.json'):
    """
    Load the destination service configuration from a JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

# Load the rules configuration from the JSON file
def load_rules_config(file_path='rules_config.json'):
    """
    Load the filtering, limiting, and validation rules from a JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def forward_request(request, config, sub=None):
    """
    Forward the incoming request to the destination service.
    :param request: The original incoming request.
    :param config: The loaded proxy configuration.
    :param sub: Optional additional path after the base URL.
    :return: Response from the destination service.
    """
    # Build the destination URL based on the proxy configuration and subpath
    destination_url = f"http://{config['destination']['host']}:{config['destination']['port']}{config['destination']['path']}"
    if sub:
        destination_url = f"{destination_url}/{sub}"

    app.logger.info(f"Forwarding {request.method} request to {destination_url}")  # Log request forwarding

    # Forward the request based on its method
    try:
        if request.method == 'GET':
            response = requests.get(destination_url, headers=request.headers, params=request.args, timeout=PROXY_TIMEOUT)
        elif request.method == 'POST':
            response = requests.post(destination_url, headers=request.headers, json=request.get_json(), timeout=PROXY_TIMEOUT)
        elif request.method == 'PUT':
            response = requests.put(destination_url, headers=request.headers, json=request.get_json(), timeout=PROXY_TIMEOUT)
        elif request.method == 'DELETE':
            response = requests.delete(destination_url, headers=request.headers, timeout=PROXY_TIMEOUT)

        app.logger.info(f"Received {response.status_code} from {destination_url}")  # Log response status
        return response

    except requests.exceptions.RequestException as e:
        # Log any exception that occurs during forwarding
        app.logger.error(f"Error forwarding request to {destination_url}: {str(e)}")
        raise

def handle_proxy(config, validate_method, validate_json, validate_headers, validate_payload_size=None, sub=None):
    """
    Handle the request forwarding after validating the method, JSON body, headers, and optional payload size.
    
    :param config: The proxy configuration for the destination service.
    :param validate_method: The method validator function.
    :param validate_json: The JSON validator function.
    :param validate_headers: The headers validator function.
    :param validate_payload_size: Optional function to validate payload size.
    :param sub: Optional substring for additional path handling.
    :return: Response object or error response.
    """
    # First, validate the method
    is_valid, validation_response = validate_method()
    if not is_valid:
        app.logger.warning("Method validation failed")
        return validation_response

    # Validate the request's JSON (if applicable)
    is_valid, validation_response = validate_json()
    if not is_valid:
        app.logger.warning("JSON validation failed")
        return validation_response

    # Validate the request's headers
    is_valid, validation_response = validate_headers()
    if not is_valid:
        app.logger.warning("Headers validation failed")
        return validation_response

    # Validate the payload size if the function is provided
    if validate_payload_size:
        is_valid, validation_response = validate_payload_size()
        if not is_valid:
            app.logger.warning("Payload size validation failed")
            return validation_response

    # If all validations pass, forward the request
    try:
        response = forward_request(request, config, sub=sub)
        return (response.content, response.status_code, response.headers.items())

    except Exception as e:
        # Handle any exception during the forwarding process and log it
        app.logger.error(f"Error during request forwarding: {str(e)}")
        return jsonify({'error': str(e)}), 500
