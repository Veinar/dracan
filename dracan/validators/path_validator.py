from flask import request, jsonify
import re

def create_path_validator(rules_config, logger):
    """
    Creates a function that validates the request URI based on the provided rules_config.
    
    :param rules_config: The configuration that contains URI validation rules.
    :param logger: The logger from the Flask app to use for logging.
    :return: A validation function for URIs.
    """
    uri_validation_enabled = rules_config.get("uri_validation_enabled", False)
    allowed_uris = rules_config.get("allowed_uris", [])
    allowed_uri_patterns = rules_config.get("allowed_uri_patterns", [])

    def validate_request_path():
        """
        Validates the request URI against the allowed URIs or patterns if URI validation is enabled.
        :return: Tuple (is_valid, response) - is_valid is True if valid, False otherwise.
        """
        if not uri_validation_enabled:
            logger.info("URI validation is disabled.")
            return True, None

        # Get the request path
        request_path = request.path
        logger.info(f"Validating URI: {request_path}")

        # Check if the request path is in the list of allowed URIs
        if request_path in allowed_uris:
            logger.info(f"URI {request_path} is allowed.")
            return True, None

        # Check if the request path matches any of the allowed URI patterns (regex)
        for pattern in allowed_uri_patterns:
            if re.match(pattern, request_path):
                logger.info(f"URI {request_path} matches pattern {pattern}.")
                return True, None

        # If the path is not allowed, return 403 Forbidden
        logger.warning(f"URI {request_path} is forbidden.")
        return False, (jsonify({'error': f"URI {request_path} is forbidden"}), 403)

    if uri_validation_enabled:
        logger.info("URI validation is enabled.")
    else:
        logger.info("URI validation is disabled.")

    return validate_request_path