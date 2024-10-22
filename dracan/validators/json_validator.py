from flask import request, jsonify
from jsonschema import validate, ValidationError

def validate_json(data, schema):
    """
    Validate the given JSON data against the provided schema, including required fields.
    
    :param data: The JSON data to validate.
    :param schema: The schema to validate against, which includes 'required' fields.
    :return: Tuple (is_valid, error_message).
    """
    try:
        # Validate the data against the schema, which includes required fields
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        # Return False and a clear error message if validation fails
        return False, str(e)

def create_json_validator(rules_config):
    """
    Creates a function that validates the request JSON based on the provided rules_config.
    
    :param rules_config: The configuration that contains JSON validation rules, including the JSON schema.
    :return: A validation function or None if JSON validation is disabled.
    """
    json_validation_enabled = rules_config.get("json_validation_enabled", False) 
    json_schema = rules_config.get("json_schema", {})
    detailed_errors_enabled = rules_config.get("detailed_errors_enabled", False)  # Default to False

    def validate_json_request():
        """
        Validates the request JSON against the schema if JSON validation is enabled.
        :return: Tuple (is_valid, response) - is_valid is True if valid, False otherwise.
        """
        if json_validation_enabled and request.method in ['POST', 'PUT']:
            data = request.get_json()
            is_valid, error_message = validate_json(data, json_schema)
            if not is_valid:
                # Determine whether to include detailed error information
                error_message_to_display = error_message if detailed_errors_enabled else "Invalid JSON format"
                # Return False and a 400 Bad Request response with only two values
                return False, (jsonify({'error': f"{error_message_to_display}"}), 400)
        return True, None

    if json_validation_enabled:
        print("JSON validation is enabled")
    else:
        print("JSON validation is disabled")

    return validate_json_request
