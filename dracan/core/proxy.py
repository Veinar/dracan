from flask import request, jsonify
import requests
import json

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

def forward_request(request, config):
    """
    Forward the incoming request to the destination service.
    :param request: The original incoming request.
    :param config: The loaded proxy configuration.
    :return: Response from the destination service.
    """
    destination_url = f"http://{config['destination']['host']}:{config['destination']['port']}{config['destination']['path']}"
    
    if request.method == 'GET':
        response = requests.get(destination_url, headers=request.headers, params=request.args)
    elif request.method == 'POST':
        response = requests.post(destination_url, headers=request.headers, json=request.get_json())
    elif request.method == 'PUT':
        response = requests.put(destination_url, headers=request.headers, json=request.get_json())
    elif request.method == 'DELETE':
        response = requests.delete(destination_url, headers=request.headers)
    
    return response

def handle_proxy(config, rules_config, validate_method, validate_json):
    """
    Handle the request forwarding after validating the method and JSON body.
    
    :param config: The proxy configuration for the destination service.
    :param rules_config: The rules configuration for filtering.
    :param validate_method: The method validator function.
    :param validate_json: The JSON validator function.
    :return: Response object or error response.
    """
    # First, validate the method
    is_valid, validation_response = validate_method()
    if not is_valid:
        return validation_response

    # Then, validate the request's JSON (if applicable)
    is_valid, validation_response = validate_json()
    if not is_valid:
        return validation_response

    # If both validations pass, forward the request
    try:
        response = forward_request(request, config)
        return (response.content, response.status_code, response.headers.items())

    except Exception as e:
        # Handle any exception during the forwarding process
        return jsonify({'error': str(e)}), 500