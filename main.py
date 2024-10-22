from flask import Flask
from dracan.core.proxy import load_proxy_config, load_rules_config, handle_proxy
from dracan.middleware.limiter import create_limiter
from dracan.validators.json_validator import create_json_validator
from dracan.validators.method_validator import create_method_validator

app = Flask(__name__)

# Load the proxy and rules configurations
proxy_config = load_proxy_config()
rules_config = load_rules_config()

# Apply the rate limiter if needed
limiter = create_limiter(app, rules_config)

# Apply the method validator
validate_method = create_method_validator(rules_config)

# Apply the JSON validator if needed
validate_json = create_json_validator(rules_config)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_route():
    """
    Main route that proxies requests to the destination service after applying filtering and validation.
    """
    # Forward request to the proxy with both method and JSON validators
    return handle_proxy(proxy_config, rules_config, validate_method, validate_json)

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
