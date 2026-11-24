#!/usr/bin/env bash
# Creates two kind clusters (private + simulated public) and deploys the app on both.
set -euo pipefail
cd "$(dirname "$0")/.."

docker build -t visitor-counter:1.0 ./app

for env in private public; do
  kind create cluster --name "$env" --config "hybrid/kind-$env.yaml"
  kind load docker-image visitor-counter:1.0 --name "$env"
  kubectl --context "kind-$env" apply -f k8s/redis.yaml -f k8s/web.yaml
  kubectl --context "kind-$env" set env deployment/web CLUSTER_NAME="$env-cluster"
  kubectl --context "kind-$env" rollout status deployment/web
done

# nginx front door: primary = private (8081), backup = public (8082)
docker rm -f lb 2>/dev/null || true
docker run -d --name lb --network host \
  -v "$PWD/hybrid/nginx.conf:/etc/nginx/nginx.conf:ro" nginx:alpine

echo "Front door: http://localhost:8080   (private: :8081, public: :8082)"
