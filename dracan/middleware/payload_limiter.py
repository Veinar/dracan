from flask import request, jsonify

def create_payload_size_limiter(rules_config, logger):
    """
    Creates a function that validates the request payload size based on the provided rules_config.
    
    :param rules_config: The configuration that contains payload size limitations.
    :param logger: The logger from the Flask app to use for logging.
    :return: A validation function for payload size.
    """
    payload_limiting_enabled = rules_config.get("payload_limiting_enabled", False)
    max_payload_size = rules_config.get("max_payload_size", 1024)  # Default to 1KB if not specified

    def validate_payload_size():
        """
        Validates the request payload size if payload limiting is enabled.
        :return: Tuple (is_valid, response) - is_valid is True if valid, False otherwise.
        """
        if not payload_limiting_enabled:
            logger.info("Payload size limiting is disabled.")
            return True, None

        # Get the payload size or let know that there is no payload to check
        payload_size = request.content_length
        if payload_size is None:
            logger.info("No payload to validate.")
            return True, None

        logger.info(f"Validating payload size: {payload_size} bytes (Max allowed: {max_payload_size} bytes)")

        if payload_size > max_payload_size:
            logger.warning(f"Payload size {payload_size} exceeds the limit of {max_payload_size} bytes.")
            return False, (jsonify({'error': f"Payload size exceeds the limit of {max_payload_size} bytes"}), 413)

        logger.info(f"Payload size {payload_size} is within the allowed limit.")
        return True, None

    if payload_limiting_enabled:
        logger.info(f"Payload size limiting is enabled with max size: {max_payload_size} bytes.")
    else:
        logger.info("Payload size limiting is disabled.")

    return validate_payload_size
