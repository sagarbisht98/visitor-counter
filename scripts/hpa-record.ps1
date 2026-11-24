# Records replica count + CPU every 10s into docs/hpa-log.csv
if (!(Test-Path "docs")) {
    New-Item -ItemType Directory -Path "docs" | Out-Null
}
"time,cpu_percent,replicas" | Out-File -FilePath "docs/hpa-log.csv" -Encoding utf8

Write-Host "Recording HPA status every 10s to docs/hpa-log.csv (Press Ctrl+C to stop)..." -ForegroundColor Cyan
while ($true) {
    $line = kubectl get hpa web-hpa --no-headers 2>$null
    if ($line) {
        $parts = -split $line
        $cpu = ($parts[2] -split "/")[0]
        $rep = $parts[6]
        $timestamp = (Get-Date).ToString("HH:mm:ss")
        $entry = "$timestamp,$cpu,$rep"
        Write-Host $entry
        $entry | Out-File -FilePath "docs/hpa-log.csv" -Append -Encoding utf8
    } else {
        Write-Host "HPA web-hpa not found yet..."
    }
    Start-Sleep -Seconds 10
}
