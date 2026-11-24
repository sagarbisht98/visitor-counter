# Demonstrates failover: stop the private cluster, traffic moves to the public one.
function Hit-Endpoint {
    try {
        $res = Invoke-RestMethod -Uri "http://localhost:8080/" -TimeoutSec 3
        $res | ConvertTo-Json -Compress
    } catch {
        '{"error":"no response"}'
    }
}

Write-Host "== BEFORE: private cluster up ==" -ForegroundColor Cyan
1..3 | ForEach-Object { Hit-Endpoint; Start-Sleep -Milliseconds 500 }

Write-Host "`n== Stopping private cluster ==" -ForegroundColor Yellow
docker stop private-control-plane
Start-Sleep -Seconds 3

Write-Host "`n== AFTER: served by public cluster ==" -ForegroundColor Cyan
1..3 | ForEach-Object { Hit-Endpoint; Start-Sleep -Milliseconds 500 }

Write-Host "`n== Restoring private cluster ==" -ForegroundColor Green
docker start private-control-plane
