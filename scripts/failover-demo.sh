#!/usr/bin/env bash
# Demonstrates failover: stop the private cluster, traffic moves to the public one.
set -u
hit() { curl -s --max-time 3 http://localhost:8080/ || echo '{"error":"no response"}'; }

echo "== BEFORE: private cluster up =="
for i in 1 2 3; do hit; echo; done

echo "== Stopping private cluster =="
docker stop private-control-plane
sleep 3

echo "== AFTER: served by public cluster =="
for i in 1 2 3; do hit; echo; done

echo "== Restoring private cluster =="
docker start private-control-plane
