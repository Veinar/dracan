from flask import request, jsonify

def create_method_validator(rules_config):
    """
    Creates a function that validates if the request method is allowed based on the provided rules_config.
    
    :param rules_config: The configuration that contains allowed methods.
    :return: A validation function for HTTP methods.
    """
    allowed_methods = rules_config.get("allowed_methods", ["GET", "POST", "PUT", "DELETE"])

    def validate_method():
        """
        Validates the request method against the allowed methods.
        :return: Tuple (is_valid, response) - is_valid is True if valid, False otherwise.
        """
        if request.method not in allowed_methods:
            return False, jsonify({'error': f"Method {request.method} not allowed"}), 405
        return True, None

    return validate_method