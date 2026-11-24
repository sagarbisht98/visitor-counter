# Creates two Minikube clusters (private-cluster + simulated public-cluster) and deploys the app on both.
$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "== Building Docker image ==" -ForegroundColor Cyan
docker build -t visitor-counter:1.0 ./app

Write-Host "== Starting Minikube clusters ==" -ForegroundColor Cyan
minikube start -p private-cluster
minikube start -p public-cluster

$clusters = @("private-cluster", "public-cluster")
foreach ($env in $clusters) {
    Write-Host "== Deploying to $env ==" -ForegroundColor Cyan
    minikube image load visitor-counter:1.0 -p $env
    kubectl --context $env apply -f k8s/redis.yaml -f k8s/web.yaml
    kubectl --context $env set env deployment/web CLUSTER_NAME="$env"
    kubectl --context $env rollout status deployment/web
}

$privateIp = (minikube ip -p private-cluster).Trim()
$publicIp = (minikube ip -p public-cluster).Trim()
Write-Host "`nPrivate cluster web service available at: http://${privateIp}:30080" -ForegroundColor Green
Write-Host "Public cluster web service available at: http://${publicIp}:30080" -ForegroundColor Green
