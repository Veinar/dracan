# Dracan Environment Configuration Guide for Docker

This guide explains the purpose and usage of each environment setting for the application. Each variable controls specific functionalities, validation mechanisms, rate-limiting, health check settings, proxy timeouts, and metrics. Detailed explanations for each setting are provided below.

---

## Validation and Limiting Settings

Each of these variables can be set to `true` or `false`.
  
**The default enabling or disabling of these settings is configured in the JSON file `rules_config.json`.** However, each setting can be explicitly overridden here:
  - Setting the variable to `false` disables functionality overriding config file entry.
  
> **Note:** If a setting is set here but conflicts with the `rules_config.json`, the application will check for integrity and fail if a configuration mismatch is detected (i.e. config = disabled, env = enabled).

> **Note 2:** It is better to not set up any of `_ENABLED` env if we do not want to explicitly disable them.

### Variables

- **`METHOD_VALIDATION_ENABLED`**: When set to `false`, disables validation of HTTP methods allowed by the application.
- **`JSON_VALIDATION_ENABLED`**: When `false`, disables validation of incoming JSON payloads.
- **`RATE_LIMITING_ENABLED`**: When `false`, disables rate limiting to control the number of requests.
- **`PAYLOAD_LIMITING_ENABLED`**: When `false`, disables limiting size of incoming payloads.
- **`URI_VALIDATION_ENABLED`**: When `false`, disables validation of request URIs.
- **`HEADER_VALIDATION_ENABLED`**: When `false`, disables validation on request headers.

---

## Proxy Settings

- **`PROXY_TIMEOUT`**: Configures the timeout duration for requests that pass through a proxy. If not set, the default timeout is **180 seconds**.

Example:
```sh
PROXY_TIMEOUT=180
```
> **Note:** The proxy timeout is critical for controlling how long the application will wait for responses from proxied requests.

## Health Check Settings

These settings configure the application's health check endpoint, which is used to monitor the application's availability.

* **`HEALTHCHECK_PORT`**: Sets the port for the health check endpoint. The default is 9000, and setting this variable is optional.
* **`HEALTHCHECK_DISABLED`**: Controls whether the health check is enabled. **By default, it is set to false, which means the health check is active**. Setting this to true will disable the health check.

Example:
```sh
HEALTHCHECK_PORT=9000
HEALTHCHECK_DISABLED=false
```
> **Note:** Disabling the health check may interfere with monitoring systems expecting a health check response like k8s.

## Metrics Settings

These settings configure metrics collection, typically for monitoring and integration with tools like Prometheus.

* **`ALLOW_METRICS_ENDPOINT`**: **By default, metrics collection is disabled**. Set this to true to enable the metrics endpoint.
* **`METRICS_PORT`**: Specifies the port for the metrics endpoint. The default is `9100`, but this variable is ignored if `ALLOW_METRICS_ENDPOINT` is set to false.

Example:
```sh
ALLOW_METRICS_ENDPOINT=true
METRICS_PORT=9100
```
> **Note:** Metrics collection should be enabled only when needed, as it may introduce additional processing overhead.

## Configuration File Settings

- **`CONFIG_LOCATION`**: Sets a custom directory path for loading configuration files `proxy_config.json` and `rules_config.json`. By default, configuration files are expected in the root Dracan directory, but setting this variable allows for an alternate directory path.

Example:
```sh
CONFIG_LOCATION=/path/to/custom/config
```

> **Note:** When `CONFIG_LOCATION` is set, `dracan` will look for required files in the specified directory. If any required file is missing, the application will exit with an error.


## Logging Settings

The logging level can be configured to control the verbosity of logs generated by the application **(mainly by the proxy functionality)**. Available options are:

* **`DEBUG`**: Most verbose; shows all application details useful for development and debugging.

* **`INFO`**: General information level; includes important application events and operational information.

* **`WARNING`**: Warnings about potential issues that do not immediately impact application functionality.

* **`ERROR`**: Logs error events that may disrupt normal operation.

* **`CRITICAL`**: Most severe level, indicating critical issues that typically lead to application termination.

* **`LOG_LEVEL`**: The default is set to `INFO`, but this can be adjusted to any of the levels above based on the required verbosity.

Example:
```sh
LOG_LEVEL=INFO
```
> **Tip:** Choose a lower log level (like INFO or WARNING) in production environments to reduce log volume. Use DEBUG in development to troubleshoot specific issues.

