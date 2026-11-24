#!/usr/bin/env bash
# Generates CPU load against the web service from inside the cluster (for the HPA demo).
# Watch in another terminal:  kubectl get hpa web-hpa -w
kubectl run load-generator --rm -i --restart=Never --image=busybox:1.36 -- \
  /bin/sh -c 'end=$((SECONDS+240)); while [ $SECONDS -lt $end ]; do for i in 1 2 3 4 5 6 7 8; do wget -q -O- http://web/ >/dev/null & done; wait; done'
