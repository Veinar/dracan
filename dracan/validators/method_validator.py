from flask import request, jsonify

def create_method_validator(rules_config):
    """
    Creates a function that validates if the request method is allowed based on the provided rules_config.
    
    :param rules_config: The configuration that contains allowed methods and whether method validation is enabled.
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
            # If method validation is disabled, always return True
            return True, None

        if request.method not in allowed_methods:
            # Return False and a validation response with a 405 status code if method is not allowed
            return False, (jsonify({'error': f"Method {request.method} not allowed"}), 405)
        
        # Return True and None if the method is allowed
        return True, None

    if method_validation_enabled:
        print("HTTP Method validation is enabled, allowed methods: " + " | ".join(allowed_methods))
    else:
        print("HTTP Method validation is disabled")


    return validate_http_method
