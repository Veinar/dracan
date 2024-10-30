import re
from flask import request, jsonify

def create_header_validator(rules_config, logger):
    """
    Creates a function that validates request headers based on the provided rules_config.

    :param rules_config: The configuration that contains header validation rules.
    :param logger: The logger from the Flask app to use for logging.
    :return: A function that validates headers.
    """
    header_validation_enabled = rules_config.get("header_validation_enabled", False)
    required_headers = rules_config.get("required_headers", {})
    prohibited_headers = rules_config.get("prohibited_headers", [])

    def validate_headers():
        """
        Validates request headers based on required and prohibited headers if header validation is enabled.
        :return: Tuple (is_valid, response) - is_valid is True if headers are valid, False otherwise.
        """
        if not header_validation_enabled:
            logger.info("Header validation is disabled.")
            return True, None

        # Required Headers Validation
        for header, expected_value in required_headers.items():
            actual_value = request.headers.get(header)

            # Check if the header is present
            if actual_value is None:
                logger.warning(f"Header validation failed: Missing required header '{header}'.")
                return False, (jsonify({'error': f"Missing required header '{header}'"}), 403)

            # Handle wildcard ("*") to allow any value
            if expected_value == "*":
                logger.info(f"Header '{header}' is present and allowed with any value.")
                continue

            # Handle regex-based validation
            if expected_value.startswith("regex:"):
                pattern = expected_value[6:]  # Remove 'regex:' prefix
                if not re.match(pattern, actual_value):
                    logger.warning(f"Header validation failed: '{header}'='{actual_value}' does not match regex '{pattern}'.")
                    return False, (jsonify({'error': f"Invalid header '{header}': Does not match required pattern"}), 403)
                logger.info(f"Header '{header}' matches the specified regex pattern.")
                continue

            # Exact match validation
            if actual_value != expected_value:
                logger.warning(f"Header validation failed: '{header}'='{actual_value}' (expected '{expected_value}').")
                return False, (jsonify({'error': f"Invalid header '{header}': Expected '{expected_value}'"}), 403)
            logger.info(f"Header '{header}' is present with the correct value '{expected_value}'.")

        # Prohibited Headers Validation
        for header in prohibited_headers:
            if header in request.headers:
                logger.warning(f"Header validation failed: Prohibited header '{header}' is present.")
                return False, (jsonify({'error': f"Prohibited header '{header}' must not be present"}), 403)

        logger.info("All required headers are valid and no prohibited headers are present.")
        return True, None

    # Logging for configuration summary
    if header_validation_enabled:
        logger.info(f"Header validation is enabled with required headers: {required_headers} and prohibited headers: {prohibited_headers}")
    else:
        logger.info("Header validation is disabled.")

    return validate_headers
