#!/usr/bin/env bash
# Measures the "before" vs "after" values for the cost table.
set -euo pipefail
cd "$(dirname "$0")/.."

docker build -q -f app/Dockerfile.baseline -t visitor-counter:baseline ./app >/dev/null
docker build -q -f app/Dockerfile          -t visitor-counter:1.0      ./app >/dev/null

echo "== Image sizes =="
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep visitor-counter

echo
echo "== Live pod usage (after load / at idle) =="
kubectl top pods 2>/dev/null || echo "metrics-server not ready (see README step 5)"

echo
echo "== Current replicas =="
kubectl get deploy web
