from flask import request, jsonify

def create_method_validator(rules_config, logger):
    """
    Creates a function that validates if the request method is allowed based on the provided rules_config.
    
    :param rules_config: The configuration that contains allowed methods and whether method validation is enabled.
    :param logger: The logger from the Flask app to use for logging.
    :return: A validation function for HTTP methods.
    """
    allowed_methods = rules_config.get("allowed_methods", ["GET", "PUT", "POST", "DELETE"])
    method_validation_enabled = rules_config.get("method_validation_enabled", False)  # Default to False

    def validate_http_method():
        """
        Validates the request method against the allowed methods if method validation is enabled.
        :return: Tuple (is_valid, response) - is_valid is True if valid, False otherwise.
        """
        if not method_validation_enabled:
            logger.info("Method validation is disabled.")
            return True, None

        if request.method not in allowed_methods:
            logger.warning(f"Method {request.method} not allowed.")  # Log disallowed method
            return False, (jsonify({'error': f"Method {request.method} not allowed"}), 405)

        logger.info(f"Method {request.method} is allowed.")  # Log allowed method
        return True, None

    if method_validation_enabled:
        logger.info("HTTP Method validation is enabled. Allowed methods: " + " | ".join(allowed_methods))
    else:
        logger.info("HTTP Method validation is disabled.")

    return validate_http_method
