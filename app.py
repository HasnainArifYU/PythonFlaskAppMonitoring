from flask import Flask, render_template, Response
import time, random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total requests", ["endpoint"])
ERROR_COUNT = Counter("error_count", "Total 5xx errors", ["endpoint"])
LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])

@app.route("/")
def index():
    REQUEST_COUNT.labels("/").inc()
    return render_template("index.html")

@app.route("/status")
@LATENCY.labels("/status").time()
def status():
    REQUEST_COUNT.labels("/status").inc()
    if random.random() < 0.1:  # 10% chance of failure
        ERROR_COUNT.labels("/status").inc()
        return "Internal Server Error", 500
    return "All systems operational", 200

@app.route("/order")
@LATENCY.labels("/order").time()
def order():
    REQUEST_COUNT.labels("/order").inc()
    time.sleep(random.uniform(0, 2))  # random latency
    if random.random() < 0.15:  # 15% chance of failure
        ERROR_COUNT.labels("/order").inc()
        return "Order failed", 500
    return "Order placed!", 200

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

