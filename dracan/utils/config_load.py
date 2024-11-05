import os
import json
import sys

def get_config_file_path(filename):
    """
    Determine the configuration file path, using CONFIG_LOCATION if set,
    otherwise falling back to the default location in the root directory.
    """
    config_location = os.getenv("CONFIG_LOCATION", "")
    return os.path.join(config_location, filename) if config_location else filename

def check_required_files(required_files):
    """
    Check for the presence of required configuration files and exit if any are missing.
    """
    for filename in required_files:
        file_path = get_config_file_path(filename)
        if not os.path.exists(file_path):
            print(f"Error: Required configuration file '{filename}' is missing.")
            print("Visit https://github.com/Veinar/dracan for more information.")
            sys.exit(1)

def load_proxy_config():
    """
    Load the destination service configuration from a JSON file.
    """
    file_path = get_config_file_path("proxy_config.json")
    with open(file_path, "r") as f:
        return json.load(f)

def load_rules_config():
    """
    Load the filtering, limiting, and validation rules from a JSON file.
    """
    file_path = get_config_file_path("rules_config.json")
    with open(file_path, "r") as f:
        return json.load(f)
