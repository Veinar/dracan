from flask import Flask
from .proxy import load_proxy_config, load_rules_config, handle_proxy
from ..middleware.limiter import create_limiter
from ..validators.json_validator import create_json_validator
from ..validators.method_validator import create_method_validator
from ..validators.path_validator import create_path_validator
from ..validators.headers_validator import create_header_validator
from ..middleware.payload_limiter import create_payload_size_limiter
import os

def create_app():
    """
    Factory function to create a Flask app based on environment settings.
    """
    app = Flask(__name__)

    # Set up logging
    setup_logging(app)

    # Load configurations
    proxy_config = load_proxy_config()
    rules_config = load_rules_config()

    # Read environment variables or default settings
    method_validation_enabled = os.getenv("METHOD_VALIDATION_ENABLED", "true").lower() == "true"
    json_validation_enabled = os.getenv("JSON_VALIDATION_ENABLED", "true").lower() == "true"
    uri_validation_enabled = os.getenv("URI_VALIDATION_ENABLED", "true").lower() == "true"
    header_validation_enabled = os.getenv("HEADER_VALIDATION_ENABLED", "true").lower() == "true"
    rate_limiting_enabled = os.getenv("RATE_LIMITING_ENABLED", "true").lower() == "true"
    payload_limiting_enabled = os.getenv("PAYLOAD_LIMITING_ENABLED", "true").lower() == "true"

    # Create validators and pass the app logger
    validate_method = create_method_validator(rules_config, app.logger) if method_validation_enabled else lambda: (True, None)
    validate_json = create_json_validator(rules_config, app.logger) if json_validation_enabled else lambda: (True, None)
    validate_path = create_path_validator(rules_config, app.logger) if uri_validation_enabled else lambda: (True, None)
    validate_payload_size = create_payload_size_limiter(rules_config, app.logger) if payload_limiting_enabled else lambda: (True, None)
    validate_headers = create_header_validator(rules_config, app.logger) if header_validation_enabled else lambda: (True, None)

    # Apply rate limiter if enabled
    if rate_limiting_enabled:
        create_limiter(app, rules_config)

    # Route handling
    @app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy_route_without_sub():
        app.logger.info(f"Proxying request without sub-path")

       # Validate path before handling proxy
        is_valid, validation_response = validate_path()
        if not is_valid:
            return validation_response

        # Call handle_proxy without sub
        return handle_proxy(proxy_config, validate_method, validate_json, validate_headers, validate_payload_size)

    @app.route('/<path:sub>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy_route(sub):
        app.logger.info(f"Proxying request to sub-path: {sub}")

       # Validate path before handling proxy
        is_valid, validation_response = validate_path()
        if not is_valid:
            return validation_response

        # Call handle_proxy with sub as a keyword argument
        return handle_proxy(proxy_config, validate_method, validate_json, validate_headers, validate_payload_size, sub=sub)

    return app

def setup_logging(app):
    """
    Set up logging for the Flask app.
    """
    # Set the log level (can be adjusted as needed)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Configure logging for the application
    import logging
    logging.basicConfig(
        level=log_level,  # Set the logging level
        format="%(asctime)s [%(levelname)s] %(message)s",  # Log format
        handlers=[
            logging.StreamHandler(),  # Log to console
            #logging.FileHandler("app.log", mode='a')  # Optionally log to a file
        ]
    )

    # Override Flask's default logger with the configured one
    app.logger.setLevel(log_level)
    app.logger.info("Logger setup complete.")
