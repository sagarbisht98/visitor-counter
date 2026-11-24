# Creates two kind clusters (private + simulated public) and deploys the app on both.
$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker build -t visitor-counter:1.0 ./app

$environments = @("private", "public")
foreach ($env in $environments) {
    Write-Host "Setting up $env cluster..." -ForegroundColor Cyan
    kind create cluster --name $env --config "hybrid/kind-$env.yaml"
    kind load docker-image visitor-counter:1.0 --name $env
    kubectl --context "kind-$env" apply -f k8s/redis.yaml -f k8s/web.yaml
    kubectl --context "kind-$env" set env deployment/web CLUSTER_NAME="$env-cluster"
    kubectl --context "kind-$env" rollout status deployment/web
}

# nginx front door: primary = private (8081), backup = public (8082)
docker rm -f lb 2>$null
$nginxConfPath = Resolve-Path "hybrid/nginx.conf"
docker run -d --name lb --network host -v "${nginxConfPath}:/etc/nginx/nginx.conf:ro" nginx:alpine

Write-Host "Front door is live at: http://localhost:8080 (private: :8081, public: :8082)" -ForegroundColor Green
