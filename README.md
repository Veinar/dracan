<center>
<img src="https://veinar.pl/dracan.png" alt="drawing" width="300"/>

![GitHub License](https://img.shields.io/github/license/Veinar/dracan?style=flat)
![Contrib Welcome](https://img.shields.io/badge/contributions-welcome-blue)
![Code style](https://img.shields.io/badge/code%20style-black-black)
<p></p>
<br>
</center>

# What is `Dracan`?

**Dracan** is a specialized software solution designed to enhance filtering and validation capabilities within Kubernetes (k8s) environments. It aims to be lightweight middleware between ingress and applications. This tool focuses on several key functionalities:

- **HTTP Method Filtering**: Dracan allows you to filter specific HTTP methods, ensuring that only allowed request types can interact with your applications.

- **JSON Validation**: It provides robust JSON validation to verify that incoming data meets predefined formats and standards, helping to prevent malformed data from causing issues in your applications.

- **Request Limiting**: Dracan enables you to set limits on the number of requests processed, helping to mitigate overload and protect application performance.

- **Payload Limitation**: Dracan supports payload limitation by allowing you to specify size limits for incoming request bodies. This feature helps prevent overly large requests that could impact application performance and stability.

- **URI Filtering**: Dracan supports filtering of incoming request URIs by allowing you to specify exact allowed URIs or use regular expressions for pattern matching. This ensures that only requests with valid URIs are processed, adding an extra layer of security and control.

- **Header Validation**: Dracan allows for comprehensive validation of HTTP headers in incoming requests. This functionality adds another level of control, ensuring that only requests with appropriate headers are processed, which can be crucial for maintaining application security and integrity. You can specify:
  - **Required Headers**: Ensure that specific headers must be present in the request.
  - **Prohibited Headers**: Specify headers that should not be included in the request.
  - **Header Matching**: Use regular expressions to validate header values or check for the presence of a header using a wildcard (`*`).

- **More filtering/validation underway...**


Dracan is intended to serve as a gatekeeper for your applications, protecting them from erroneous or redundant queries. By ensuring the integrity of incoming requests, it contributes to operational continuity and safeguards against disruptive events.

## How to use it ?

Dracan is designed to be implemented as middleware in Kubernetes (k8s) environments, functioning as a gatekeeper for your applications. Follow these steps to integrate Dracan into your system:

**Example deployment can be seen [in example subdirectory](./example/README.md).**

1. **Deployment**: Deploy Dracan in your Kubernetes cluster. It should be configured to replace the default application entry point in the Ingress controller.

2. **Ingress Configuration**: Set up Dracan as the primary Ingress resource. This will allow it to proxy requests to the designated services defined in your configuration file. Ensure that Dracan is correctly routed to the appropriate application services.

3. **Configuration Files**:
   - **Proxy Configuration File** `proxy_config.json`: This file should declare the services to which Dracan will proxy requests. It essentially tells Dracan how to route traffic.
   - **Rules Configuration File** `rules_config.json`: Use this file to specify the filtering, validation, and request limit rules that Dracan will enforce. You can define what types of HTTP methods to allow, set JSON validation schemas, and establish limits on the number of requests.

4. **Deploy Changes**: Apply the configuration changes and redeploy your Ingress resource. Dracan will now process incoming requests according to the defined rules, ensuring that only valid requests reach your application.

5. **Monitor and Adjust**: After deployment, monitor the traffic and performance. You may need to adjust the filtering and validation rules in the secondary configuration file based on your application's needs.

By following these steps, you can effectively integrate Dracan into your Kubernetes environment, enhancing the security and reliability of your applications.

## Local development

To start developing Dracan on your local machine, you can set up a mock service for live debugging. Follow these steps to get started:

1. **Clone the Repository**: First, clone the Dracan repository to your local machine if you haven't done so already.
   ```bash
   git clone https://github.com/Veinar/dracan.git
   cd dracan
   ```
2. Set Up a Virtual Environment: It’s recommended to create a virtual environment for your development work to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\Activate.ps1`
    ```
3. Install Required Dependencies: Install the necessary Python packages using pip. Ensure you have Flask installed, as it is used for the mock service.
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Mock Service: Start the mock service provided in the Dracan package. This service is located in `tests/destination_mock.py` and simulates the application your Dracan middleware will be interfacing with.
    ```bash
    python tests/destination_mock.py
    ```
5. Live Debugging: With the mock service running, you can now run Dracan in your local environment. This allows you to test and debug how Dracan interacts with the mock service in real-time.
6. Modify and Test: Make changes to Dracan's code as needed, and observe the interactions with the mock service. This setup enables you to develop efficiently and troubleshoot any issues in real-time.

## Building Docker image

In order to prepare Docker image inside root directory of project execute:
```bash
docker build . -t dracan:latest
```
> You may want to change name or tag for this build command

### Docker environmental variables

In order to enable/disable validation, filtering or limiting use env variables that should be passed to container.

> Dracan by default disables filtering/limiting/validation if entry is not present in `rules_config.json` file.

but additional global disable/enable by env variables is implemented as **stub**.

```bash
# Should be always set to true/false
METHOD_VALIDATION_ENABLED=true
JSON_VALIDATION_ENABLED=true
RATE_LIMITING_ENABLED=true
PAYLOAD_LIMITING_ENABLED=true
URI_VALIDATION_ENABLED=true
HEADER_VALIDATION_ENABLED=true
# Optional
LOG_LEVEL=INFO
```


## Configuration Files

To set up Dracan effectively, you need to create two configuration files: `proxy_config.json` and `rules_config.json`. These files determine how Dracan will handle incoming traffic and define the rules for validating, filtering, and limiting requests.

### 1. Creating `proxy_config.json`

The `proxy_config.json` file specifies where Dracan should proxy incoming traffic. Here’s a sample configuration:

```json
{
    "destination": {
        "host": "127.0.0.1",
        "port": 8080,
        "path": "/"
    }
}
```

* **host**: The address of the destination service where Dracan will forward the requests. This can be an IP address or a domain name.
> Make sure of correct DNS settings!
* **port**: The port on which the destination service is running.
* **path**: The path that will be appended to the host when forwarding requests.

Ensure this configuration accurately points to your application or mock service.

### 2. Creating `rules_config.json`

The `rules_config.json` file contains rules for validating, filtering, and limiting incoming requests. Below is an example configuration:

```json
{
  "limiting_enabled": true,
  "rate_limit": "10 per minute",
  "method_validation_enabled": true,
  "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
  "json_validation_enabled": true,
  "detailed_errors_enabled": false,
  "json_schema": {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "age": { "type": "number" }
    },
    "required": ["name", "age"]
  },  
  "uri_validation_enabled": true,
  "allowed_uris": [
    "/health",
    "/data",
    "/update",
    "/delete"
  ],
  "allowed_uri_patterns": [
    "^/api/.*",               
    "^/public/[A-Za-z0-9_-]+"
  ],
  "payload_limiting_enabled": true,
  "max_payload_size": 1024,
  "header_validation_enabled": true,
  "required_headers": {
    "Content-Type": "application/json",
    "X-API-KEY": "*",
    "Authorization": "regex:^Bearer\\s[A-Za-z0-9\\-_]+\\.[A-Za-z0-9\\-_]+\\.[A-Za-z0-9\\-_]+$"
  },
  "prohibited_headers": [
    "X-Internal-Header",
    "X-Debug-Token"
  ]
}
```

* **limiting_enabled**: A boolean value that enables or disables rate limiting for incoming requests.
* **rate_limit**: Specifies the allowed rate of requests (e.g., "10 per minute"), how to check possible rates is described [here](https://github.com/alisaifee/flask-limiter?tab=readme-ov-file#inspect-the-limits-using-the-command-line-interface).
* **allowed_methods**: An array of HTTP methods that are permitted for incoming requests (e.g., ["GET", "POST", "PUT", "DELETE"]).
* **method_validation_enabled**: A boolean flag to enable or disable validation of HTTP methods.
* **json_validation_enabled**: A boolean flag to enable or disable JSON body validation.
* **detailed_errors_enabled**: When set to true, Dracan provides more detailed error messages for validation failures as HTTP response.
* **json_schema**: A JSON schema defining the expected structure of the incoming request body. This schema outlines the required properties and their types (in this case, name as a string and age as a number).    
* **uri_validation_enabled**: A boolean flag that enables or disables URI validation for incoming requests.
* **allowed_uris**: An array of exact URIs that are permitted. Requests that do not match these URIs will be rejected.
* **allowed_uri_patterns**: An array of regular expressions for URI pattern matching. This allows more flexible matching of URIs that follow certain patterns (e.g., `^/api/.*` will match any URI starting with `/api/`).
* **payload_limiting_enabled**: A boolean flag to enable or disable payload size validation
* **max_payload_size**: Specifies maximal size of payload in `bytes`.
* **required_headers**: An object that defines the headers that must be present in the request. You can specify:
  * *Exact header values* (e.g., "Content-Type": "application/json").
  * *Wildcards* (e.g., "X-API-KEY": "*"), indicating the header must be present regardless of its value.
  * *Regular expressions* for validating specific header values. _Must comply with [re](https://docs.python.org/3/library/re.html)_.
* **prohibited_headers**: An array of headers that should not be included in the request. If these headers are present, the request will be rejected.

> **In real case scenario those two JSON config files should be mounted (from config map or secret) in deployment of Dracan on k8s alike systems.**

## Contributing

We warmly welcome contributions to Dracan! Whether you're a seasoned developer or just starting out, your input is invaluable in making this project better. Here are a few ways you can contribute:

- **Report Issues**: If you encounter bugs or have suggestions for improvements, please open an issue. Your feedback helps us identify areas for enhancement.
  
- **Submit Pull Requests**: If you have a feature in mind or a fix for an existing issue, feel free to fork the repository and submit a pull request. We encourage collaboration and will review your contributions promptly.

- **Documentation**: Help us improve our documentation! If you find any unclear sections or if you think additional information could benefit users, your contributions are welcome.

- **Share Your Ideas**: Have a great idea for a feature or enhancement? We’d love to hear it! Start a discussion, and let's explore it together.

By contributing, you’re not only helping to improve Dracan but also make one man happier. Thank you for your interest and support—together, we can make Dracan even better!
