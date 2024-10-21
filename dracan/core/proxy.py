import requests
import json

def load_proxy_config(file_path='proxy_config.json'):
    """
    Load the destination service configuration from a JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def load_rules_config(file_path='rules_config.json'):
    """
    Load the filtering, limiting, and validation rules from a JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to forward the request to the destination server
def forward_request(request, config):
    """
    Forward the incoming request to the destination service.
    :param request: The original incoming request.
    :param config: The loaded proxy configuration.
    :return: Response from the destination service.
    """
    # Construct the destination URL using the config
    destination_url = f"http://{config['destination']['host']}:{config['destination']['port']}{config['destination']['path']}"

    # Forward the request based on its method
    if request.method == 'GET':
        response = requests.get(destination_url, headers=request.headers, params=request.args)
    elif request.method == 'POST':
        response = requests.post(destination_url, headers=request.headers, json=request.get_json())
    elif request.method == 'PUT':
        response = requests.put(destination_url, headers=request.headers, json=request.get_json())
    elif request.method == 'DELETE':
        response = requests.delete(destination_url, headers=request.headers)

    # Return the response from the destination
    return response
