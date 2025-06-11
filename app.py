from flask import Flask, render_template, Response
import time, random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Initialize the Flask app
app = Flask(__name__)

# ----------------------------
# Prometheus Metric Definitions
# ----------------------------

# Counter: track total requests per endpoint
REQUEST_COUNT = Counter("request_count", "Total requests", ["endpoint"])

# Counter: track number of 5xx errors per endpoint
ERROR_COUNT = Counter("error_count", "Total 5xx errors", ["endpoint"])

# Histogram: track request latency per endpoint
LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])

# ----------------------------
# Application Routes
# ----------------------------

# Root route: serves the homepage template
@app.route("/")
def index():
    REQUEST_COUNT.labels("/").inc()
    return render_template("index.html")

# /status route: returns status with 10% chance of failure
@app.route("/status")
@LATENCY.labels("/status").time()
def status():
    REQUEST_COUNT.labels("/status").inc()
    if random.random() < 0.1:
        ERROR_COUNT.labels("/status").inc()
        return "Internal Server Error", 500
    return "All systems operational", 200

# /order route: simulates random latency and 15% failure
@app.route("/order")
@LATENCY.labels("/order").time()
def order():
    REQUEST_COUNT.labels("/order").inc()
    time.sleep(random.uniform(0, 2))  # simulate latency
    if random.random() < 0.15:
        ERROR_COUNT.labels("/order").inc()
        return "Order failed", 500
    return "Order placed!", 200

# /metrics route: exposes Prometheus metrics
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# ----------------------------
# Run the Flask App
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

