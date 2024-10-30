# `rules_config.json` Configuration Guide

This short doc will explain how to set properly proxy config file.

**Note:** By default if  `*_enabled` is not specified inside configuration file validation/limiting will be **disabled**.

**Table of contents:**

1. Time limits (rate limits)
2. HTTP Method validation
3. URI Path validation
4. Payload size limiting
5. JSON schema validation
6. Header validation

## 1. Time limits (rate limits)

`limiting_enabled` 

Description: *Enables or disables rate limiting.*   
Possible values: *`true` or `false`*

Example:
```json
...
    "limiting_enabled": true
...
```

`rate_limit`

Description: *Specifies the allowed rate of requests*   
Possible values: *[LINK](https://github.com/alisaifee/flask-limiter?tab=readme-ov-file#inspect-the-limits-using-the-command-line-interface)*

Example:
```json
...
    "rate_limit": "20 per minute"
...
```
or
```json
...
    "rate_limit": "10 per second"
...
```

## 2. HTTP Method validation

`method_validation_enabled` 

Description: *Enables validation of HTTP request methods.*   
Possible values: *`true` or `false`*

Example:
```json
...
    "method_validation_enabled": true
...
```
> If not set tp `true`, Dracan will allow only `["GET", "OPTION", "POST", "PUT", "DELETE"]` methods.

`rate_limit`

Description: *Specifies HTTP methods allowed for incoming requests.*   
Possible values: *array of methods (even single method should be passed as an array)*

Example:
```json
...
    "allowed_methods": ["GET", "UPDATE", "POST", "PUT", "DELETE"]
...
```
or
```json
...
    "allowed_methods": ["GET", "POST"]
...
```

## 3. URI Path validation

`method_validation_enabled` 

Description: *Enables validation of URI paths for incoming requests.*   
Possible values: *`true` or `false`*

Example:
```json
...
    "uri_validation_enabled": true
...
```

`allowed_uris`

Description: *Specifies **exact** URIs that are allowed.*   
Possible values: *array of exact allowed URIs (even single URI should be passed as an array)*

Example:
```json
...
    "allowed_uris": ["/health", "/data", "/update", "/delete"]
...
```
or
```json
...
    "allowed_uris": ["/", "/person"]
...
```

`allowed_uri_patterns`   

Description: *Uses regular expressions to allow URIs matching specific patterns.*   
Possible values: *array of allowed URIs patterns (even single URI should be passed as an array)*

Example:
```json
...
    "allowed_uri_patterns": ["^/api/.*", "^/public/[A-Za-z0-9_-]+"]
...
```
or
```json
...
    "allowed_uri_patterns": ["^/[A-Za-z0-9_-]+"]
...
```

> Regexp must comply with python `re`.

## 4. Payload limiting

`payload_limiting_enabled` 

Description: *Enables size limitations for request payloads.*   
Possible values: *`true` or `false`*

Example:
```json
...
    "payload_limiting_enabled": true
...
```

`max_payload_size`

Description: *Sets the maximum size (in bytes) allowed for a request payload.*   
Possible values: *any integer value*

Example:
```json
...
    "max_payload_size": 1024
...
```
or
```json
...
    "max_payload_size": 8388608  //This will be 8 MB
...
```

## 5. JSON Schema Validation

`json_validation_enabled` 

Description: *Enables validation for JSON bodies in requests.*   
Possible values: *`true` or `false`*

Example:
```json
...
    "json_validation_enabled": true
...
```

`json_schema`

Description: *Defines the expected JSON structure using a JSON schema, enforcing data types and required fields.*   
Possible values: *constructed JSON schema*

Example:
```json
...
    "json_schema": {
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "age": { "type": "number" }
    },
    "required": ["name", "age"]
    }
...
```
Explanation: *Schema requires name as a string and age as a number. Any JSON payload not meeting these criteria will be rejected.*

or

```json
...
    "json_schema": {
    "type": "object",
    "properties": {
        "user": {
        "type": "object",
        "properties": {
            "name": {
            "type": "string"
            },
            "address": {
            "type": "object",
            "properties": {
                "street": {
                "type": "string"
                },
                "city": {
                "type": "string"
                },
                "zip": {
                "type": "integer"
                }
            },
            "required": [
                "street",
                "city"
            ]
            }
        },
        "required": [
            "name",
            "address"
        ]
        }
    }
    }
...
```

Explanation: *Allows for nested properties, enforcing that user has name and an address object.*

or 

```json
    "json_schema" = {
    "type": "object",
    "properties": {
        "products": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
            "id": {
                "type": "integer"
            },
            "name": {
                "type": "string"
            },
            "price": {
                "type": "number"
            }
            },
            "required": [
            "id",
            "name",
            "price"
            ]
        }
        }
    }
    }
```

Explanation: Requires a list of products, each with specific properties.

## 6. Header validation

`header_validation_enabled` 

Description: *Enables validation of HTTP request headers.*   
Possible values: *`true` or `false`*

Example:
```json
...
    "header_validation_enabled": true
...
```

`required_headers`

Description: *Defines headers that must be included in the request. Supports exact matches, wildcard (just checking if present), and regular expressions.*   
Possible values: *array of exact allowed headers (even single header should be passed as an array)*

Example:
```json
...
    "required_headers": {
      "Content-Type": "application/json",
      "X-API-KEY": "*", //This is wildcard (so, Dracan will check only if header is present)
      "Authorization": "regex:^Bearer\\s[A-Za-z0-9\\-_]+\\.[A-Za-z0-9\\-_]+\\.[A-Za-z0-9\\-_]+$"
    },
...
```
> Make note, that `regex:` keyword is used for validating against regular expression. Do not omit this keyword in order to use functionality.

`prohibited_headers`   

Description: *Defines headers that should not be included in requests.*   
Possible values: *array of allowed URIs patterns (even single URI should be passed as an array)*

Example:
```json
...
      "prohibited_headers": [
        "X-Internal-Header",
        "X-Debug-Token"
      ]
...
```
