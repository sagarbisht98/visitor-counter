#!/usr/bin/env bash
# Creates two Minikube clusters (private-cluster + simulated public-cluster) and deploys the app on both.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== Building Docker image =="
docker build -t visitor-counter:1.0 ./app

echo "== Starting Minikube clusters =="
minikube start -p private-cluster
minikube start -p public-cluster

for env in private-cluster public-cluster; do
  echo "== Deploying to $env =="
  minikube image load visitor-counter:1.0 -p "$env"
  kubectl --context "$env" apply -f k8s/redis.yaml -f k8s/web.yaml
  kubectl --context "$env" set env deployment/web CLUSTER_NAME="$env"
  kubectl --context "$env" rollout status deployment/web
done

# Get service URLs
PRIVATE_IP=$(minikube ip -p private-cluster)
PUBLIC_IP=$(minikube ip -p public-cluster)
echo "Private cluster web service available at: http://$PRIVATE_IP:30080"
echo "Public cluster web service available at: http://$PUBLIC_IP:30080"
