from flask import request, jsonify
from jsonschema import validate, ValidationError

def validate_json(data, schema):
    """
    Validate the given JSON data against the provided schema.
    
    :param data: The JSON data to validate.
    :param schema: The schema to validate against.
    :return: Tuple (is_valid, error_message).
    """
    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)


def create_json_validator(rules_config):
    """
    Creates a function that validates the request JSON based on the provided rules_config.
    
    :param rules_config: The configuration that contains validation rules.
    :return: A validation function or None if validation is disabled.
    """
    validation_enabled = rules_config.get("validation_enabled", False)
    json_schema = rules_config.get("json_schema", {})
    
    def validate_request():
        """
        Validates the request JSON against the schema if validation is enabled.
        :return: Tuple (is_valid, response) - is_valid is True if valid, False otherwise.
        """
        if validation_enabled and request.method in ['POST', 'PUT']:
            is_valid, error_message = validate_json(request.get_json(), json_schema)
            if not is_valid:
                return False, jsonify({'error': f"Invalid JSON: {error_message}"}), 400
        return True, None

    if validation_enabled:
        print("JSON validation is enabled")
    else:
        print("JSON validation is disabled")

    return validate_request
