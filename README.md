<p align="center">
<img src="https://veinar.pl/dracan.png" alt="logo" width="300"/>

![GitHub License](https://img.shields.io/github/license/Veinar/dracan?style=flat)
![GitHub Tag](https://img.shields.io/github/v/tag/Veinar/dracan?label=version)
![Code style](https://img.shields.io/badge/code%20style-black-black)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/41bf10729dcc4e209dded4c298d945d5)](https://app.codacy.com/gh/Veinar/dracan/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![codecov](https://codecov.io/github/Veinar/dracan/graph/badge.svg?token=LNPKYPY8RB)](https://codecov.io/github/Veinar/dracan)
[![Testing Report](https://github.com/Veinar/dracan/actions/workflows/code_analysis.yaml/badge.svg)](https://github.com/Veinar/dracan/actions/workflows/code_analysis.yaml)
![Docker Image Size](https://img.shields.io/docker/image-size/veinar/dracan)
![Docker Pulls](https://img.shields.io/docker/pulls/veinar/dracan?color=yellow)
![Contrib Welcome](https://img.shields.io/badge/contributions-welcome-blue)

<br>
</p>

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

- **You have another filtering/validation idea? Submit an issue! We are open for ideas :hearts:**

Dracan is intended to serve as a gatekeeper for your applications, protecting them from erroneous or redundant queries. By ensuring the integrity of incoming requests, it contributes to operational continuity and safeguards against disruptive events.

##  Why use Dracan?

Dracan is a lightweight yet powerful middleware security solution for handling requests targeted at small to mid-sized development teams and independent projects. In a simple configuration file (understandable by developers), request validation can be set up with rate limiting, payload control, and traffic filtering enabled without advanced DevOps expertise or heavy infrastructure like WAF (Web application Firewall). You focus on creating good filters in `rules_config.json`, rest is on us.

Ideal for use for applications hosted on Kubernetes or GKE, Dracan offers essential security features to protect internal requests so that teams can focus on development. Because of its modular design, you are sure to be able to customize security needs with ease and speed. Dracan is both friendly and powerful for application protection.

> Random requests performance test result of performance could be found [here](https://pastebin.com/61Fyy2Pe).   
> Powershell script used for this test can be found [here](https://gist.github.com/Veinar/bd8abc12ed3ce3367980da5a335f78f2).

## How to use it ?

<p align="center">
  <img src="https://veinar.pl/dracan_diagram.gif" width="65%">
</p>

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

## Local development, testing and quality checking

To start developing Dracan on your local machine, you can set up a mock service for live debugging. Follow steps described in [this doc](./docs/local_development.md) to get started.

## Docker

**Docker image is present at [DockerHub](https://hub.docker.com/r/veinar/dracan).** For ease of use it is shipped without config JSONs. Remember to provide them on runtime!

You can also build image from source just follow [this doc](./docs/docker_building.md).

For further details on configuration of env variables, refer to [this doc](./docs/docker_env_config.md).

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
**Expanded documentation about fields and values can be found [HERE](./docs/proxy_config.md).**

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
  "rate_limit": "20 per minute",
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

**Expanded documentation about fields and values can be found [HERE](./docs/rules_config.md).**

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

## Health check

Dracan includes a built-in health check feature to monitor the application's status. By default, health checks are enabled and the application listens on port **9000** at the root location (`/`). 

User may customize port on which Drakan listens for HC requests setting `HEALTHCHECK_PORT`env variable, or may completly disable it using `HEALTHCHECK_DISABLED` env variable.

## Metrics Collection

Dracan offers an optional metrics endpoint for tracking application performance and request data, which can be integrated with Prometheus for monitoring. :chart_with_upwards_trend:

### Key Features
- **Request Count**: Tracks the number of HTTP requests by method and status.
- **Request Latency**: Measures the response times for different endpoints.
- **Request and Response Sizes**: Analyzes data usage for incoming and outgoing requests.

### Enabling Metrics
Metrics collection is disabled by default. To enable it, set the following environment variables:

- **`ALLOW_METRICS_ENDPOINT`**: Set to `true` to enable.
- **`METRICS_PORT`**: (Optional) Specify the port for the metrics endpoint, default is `9100`.

Example:
```bash
export ALLOW_METRICS_ENDPOINT=true
export METRICS_PORT=2000
```

When enabled, the metrics endpoint can be accessed at `http://<dracan_ip?>:<METRICS_PORT>/metrics`.

For further details on configuration and integration with Prometheus, refer to [this doc](./docs/metrics.md).

## Contributing

We warmly welcome contributions to Dracan! Whether you're a seasoned developer or just starting out, your input is invaluable in making this project better. Here are a few ways you can contribute:

- **Report Issues**: If you encounter bugs or have suggestions for improvements, please open an issue. Your feedback helps us identify areas for enhancement.
  
- **Submit Pull Requests**: If you have a feature in mind or a fix for an existing issue, feel free to fork the repository and submit a pull request. We encourage collaboration and will review your contributions promptly.

- **Documentation**: Help us improve our documentation! If you find any unclear sections or if you think additional information could benefit users, your contributions are welcome.

- **Share Your Ideas**: Have a great idea for a feature or enhancement? We’d love to hear it! Start a discussion, and let's explore it together.

By contributing, you’re not only helping to improve Dracan but also make one man happier. Thank you for your interest and support—together, we can make Dracan even better!

> :hearts: We welcome contributions from everyone, especially if you’re new to open-source! Whether it’s fixing a typo, suggesting an idea, or spotting a bug, every contribution counts, and we’re here to support you along the way! :rocket:

## How to Contribute ?

Contributing to our project is a great way to learn, share, and improve your skills! We welcome contributions from everyone, whether you're a seasoned developer or a newbie. Here’s a quick guide on how to get started:

1. **Fork the Repository**: Start by forking the main repository to your GitHub account. This creates a personal copy where you can make changes.

2. **Clone Your Fork**: Clone the forked repository to your local machine. In your terminal, run:
```bash
git clone https://github.com/your_username_goes_here/dracan.git
```
3. **Make preparations of dev environment** follow instructions described [here](./docs/local_development.md).

4. **Create a New Branch:** It’s a good idea to create a new branch for each feature or bug fix. This keeps your work organized and makes it easier for others to review. Run:
```bash
git checkout -b branch-name-goes-here
```

5. **Make Changes:** Now you can start coding! Follow any project guidelines, such as coding standards or testing requirements.
6. **Commit and Push:** Once your changes are ready, commit them with a clear message explaining the work you’ve done, then push your branch to GitHub:
```bash
git add .
git commit -m "Describe your changes"
git push -u origin branch-name-goes-here
```
7. **Submit a Pull Request:** Go to the original repository on GitHub, and you’ll see an option to create a new pull request (PR) from your branch. Add a clear description of your changes and submit the PR.
8. **Engage in Review:** Be open to feedback! Project maintainers may request some changes before your code can be merged.
