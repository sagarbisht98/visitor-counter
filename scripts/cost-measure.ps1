# Measures the "before" vs "after" values for the cost table.
$ErrorActionPreference = "Continue"

Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "Building baseline image..." -ForegroundColor Cyan
docker build -q -f app/Dockerfile.baseline -t visitor-counter:baseline ./app | Out-Null

Write-Host "Building optimized image..." -ForegroundColor Cyan
docker build -q -f app/Dockerfile -t visitor-counter:1.0 ./app | Out-Null

Write-Host "`n== Image sizes ==" -ForegroundColor Yellow
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | Select-String "visitor-counter"

Write-Host "`n== Live pod usage (after load / at idle) ==" -ForegroundColor Yellow
$top = kubectl top pods 2>&1
if ($LASTEXITCODE -eq 0) {
    $top
} else {
    Write-Host "metrics-server not ready (see README step 3)"
}

Write-Host "`n== Current replicas ==" -ForegroundColor Yellow
kubectl get deploy web
