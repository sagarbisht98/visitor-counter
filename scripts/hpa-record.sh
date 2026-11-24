#!/usr/bin/env bash
# Records replica count + CPU every 10s into docs/hpa-log.csv (use for your scaling graph/table).
mkdir -p docs
echo "time,cpu_percent,replicas" > docs/hpa-log.csv
while true; do
  line=$(kubectl get hpa web-hpa --no-headers)
  cpu=$(echo "$line" | awk '{print $3}' | cut -d/ -f1)
  rep=$(echo "$line" | awk '{print $7}')
  echo "$(date +%H:%M:%S),$cpu,$rep" | tee -a docs/hpa-log.csv
  sleep 10
done
