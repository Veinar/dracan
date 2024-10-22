from flask import Flask
from .proxy import load_proxy_config, load_rules_config, handle_proxy
from ..middleware.limiter import create_limiter
from ..validators.json_validator import create_json_validator
from ..validators.method_validator import create_method_validator
import os

def create_app():
    """
    Factory function to create a Flask app based on environment settings.
    """
    app = Flask(__name__)

    # Load configurations
    proxy_config = load_proxy_config()
    rules_config = load_rules_config()

    # Read environment variables or default settings
    method_validation_enabled = os.getenv("METHOD_VALIDATION_ENABLED", "true").lower() == "true"
    json_validation_enabled = os.getenv("JSON_VALIDATION_ENABLED", "true").lower() == "true"
    rate_limiting_enabled = os.getenv("RATE_LIMITING_ENABLED", "true").lower() == "true"

    # Create validators if flags are set
    validate_method = create_method_validator(rules_config) if method_validation_enabled else lambda: (True, None)
    validate_json = create_json_validator(rules_config) if json_validation_enabled else lambda: (True, None)

    # Apply rate limiter if enabled
    if rate_limiting_enabled:
        create_limiter(app, rules_config)

    # Route handling
    @app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy_route_without_sub():
        return handle_proxy(proxy_config, rules_config, validate_method, validate_json)

    @app.route('/<path:sub>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy_route(sub):
        return handle_proxy(proxy_config, rules_config, validate_method, validate_json, sub=sub)

    return app
