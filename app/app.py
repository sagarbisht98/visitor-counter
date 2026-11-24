import os
import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
CLUSTER_NAME = os.environ.get("CLUSTER_NAME", "local")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2, socket_timeout=2)


@app.route("/")
def index():
    count = r.incr("visits")
    return jsonify(
        message="Visitor Counter",
        visits=count,
        served_by_pod=socket.gethostname(),
        cluster=CLUSTER_NAME,
    )


@app.route("/health")
def health():
    # liveness: process is up
    return "ok", 200


@app.route("/ready")
def ready():
    # readiness: app can reach Redis
    try:
        r.ping()
        return "ready", 200
    except redis.RedisError:
        return "redis unavailable", 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
