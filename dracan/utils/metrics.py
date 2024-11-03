import time
from threading import Thread
from prometheus_client import start_http_server, Counter, Histogram, Gauge
from flask import request, g

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency', ['method', 'endpoint'])
REQUEST_IN_PROGRESS = Gauge('http_requests_in_progress', 'Number of HTTP requests in progress')
REQUEST_SIZE = Histogram('http_request_size_bytes', 'Size of HTTP requests', ['method', 'endpoint'])
RESPONSE_SIZE = Histogram('http_response_size_bytes', 'Size of HTTP responses', ['method', 'endpoint'])

def start_metrics_server(port=9100):
    """
    Start an independent HTTP server for Prometheus metrics on the specified port.
    """
    def metrics_thread():
        start_http_server(port)
        while True:
            time.sleep(1)  # Keeps the thread alive

    # Start the metrics server in a background thread
    thread = Thread(target=metrics_thread, daemon=True)
    thread.start()

def start_request_metrics():
    """
    Track start time and initial data for each request.
    """
    g.start_time = time.time()
    g.request_size = request.content_length or 0  # Get request size if available
    REQUEST_IN_PROGRESS.inc()  # Increment the in-progress request gauge

def finalize_request_metrics(response):
    """
    Finalize metrics recording after each request.
    """
    method = request.method
    endpoint = request.path
    status = response.status_code
    latency = time.time() - g.start_time
    request_size = g.request_size
    response_size = len(response.data) if response.data else 0

    # Record metrics for this request
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
    REQUEST_SIZE.labels(method=method, endpoint=endpoint).observe(request_size)
    RESPONSE_SIZE.labels(method=method, endpoint=endpoint).observe(response_size)
    REQUEST_IN_PROGRESS.dec()  # Decrease the in-progress count after the request

    return response

def register_metrics(app):
    """
    Register metrics hooks with the Flask app.
    """
    app.before_request(start_request_metrics)
    app.after_request(finalize_request_metrics)
