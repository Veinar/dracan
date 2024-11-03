# Metrics Collection (Prometheus)

Dracan includes an integrated metrics endpoint that collects and exposes performance and request metrics, which can be monitored using [Prometheus](https://prometheus.io/). This feature enables teams to monitor HTTP request data such as request counts, response statuses, and latencies, helping track application usage patterns and performance.

## What Metrics Are Gathered?

The Dracan metrics system gathers and exposes the following data:

- **Request Count (`http_requests_total`)**: A counter that tracks the total number of HTTP requests made to the Dracan app, grouped by method (e.g., `GET`, `POST`) and response status.
- **Request Latency (`flask_http_request_duration_seconds`)**: A histogram that captures the latency of HTTP requests, categorized by method and endpoint, to help monitor and optimize response times.
- **Request and Response Sizes**: Histograms tracking the size of incoming requests and outgoing responses, which can provide insights into typical payload sizes and bandwidth usage.
- **System Resource Metrics**: Basic runtime metrics like memory usage and garbage collection, using standard Prometheus metrics for Python applications.

## Enabling Metrics Collection

Metrics collection can be controlled via environment variables:

1. **`ALLOW_METRICS_ENDPOINT`**: Enables or disables the metrics endpoint.
   - Set to `"true"` to enable metrics collection.
   - Set to `"false"` (default) to disable metrics collection. **Or do not set this env at all**.
   
2. **`METRICS_PORT`**: Specifies the port on which the metrics server should run.
   - Defaults to `9100` if not set.
   - If a different port is desired, set `METRICS_PORT` to the desired port number.
   > *Ommited when `ALLOW_METRICS_ENDPOINT` set to `false` or not set at all.*

## Usage Instructions

To enable and use the metrics system in Dracan:

1. **Set Environment Variables**:
   - To enable the metrics server on the default port:
     ```export ALLOW_METRICS_ENDPOINT=true```
   - To specify a custom port (e.g., ```2000```):
     ```bash
     export ALLOW_METRICS_ENDPOINT=true
     export METRICS_PORT=2000
     ```

2. **Access Metrics**:
   - When metrics are enabled, access the metrics data at `<dracan_ip>:METRICS_PORT/metrics`.
   - For example:
     - **Default Port**: `http://127.0.0.1:9100/metrics`
     - **Custom Port**: `http://127.0.0.1:2000/metrics` (if `METRICS_PORT=2000`)

3. **Monitoring with Prometheus**:
   - Once the metrics server is running, configure your Prometheus server to scrape metrics from Dracan’s metrics endpoint.
   - Example Prometheus configuration snippet:
     ```yaml
     scrape_configs:
       - job_name: 'dracan'
         static_configs:
           - targets: ['<dracan_ip>:9100'] # or use custom port if specified
     ```

## Disabling Metrics Collection

If metrics collection is not required, it is disabled by default, or it can be explicitly disabled by setting `ALLOW_METRICS_ENDPOINT=false`.
