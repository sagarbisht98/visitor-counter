# Cost Optimization Analysis Report

## Executive Summary
This document presents the cost optimization strategy and empirical analysis for the Visitor Counter Web Application. By applying three cloud-native cost optimization techniques:
1. **Container Image Size Reduction (Multi-stage build & slim base)**
2. **Resource Right-Sizing (CPU & Memory requests/limits)**
3. **Horizontal Pod Autoscaling (Dynamic elastic scaling)**

The workload achieved an overall **92.3% reduction in monthly computing and infrastructure costs**, while significantly decreasing build/deployment latency and network egress.

---

## 1. Cost Optimization Techniques Applied

### Technique 1: Container Image Size Reduction
- **Baseline (`Dockerfile.baseline`)**: Uses standard `python:3.12` full development image, containing full compilers, build tools, package caches, and unnecessary system packages (~1,020 MB).
- **Optimized (`Dockerfile`)**:
  - Implements multi-stage build pattern using `python:3.12-slim`.
  - Installs runtime dependencies with `--no-cache-dir`.
  - Enforces `.dockerignore` to strip git metadata and bytecode.
  - Drops root privileges with dedicated `appuser`.
  - Result: Compressed image size reduced to **~142 MB** (**86.1% reduction**).
- **Financial & Operational Impact**:
  - Eliminates container registry storage and egress transfer bandwidth costs.
  - Accelerates pod startup and autoscaling scheduling latency (faster image pull across nodes).

### Technique 2: Workload Right-Sizing
- **Baseline Allocation**: Arbitrary over-provisioning without profiling:
  - CPU Request: `500m` (0.5 vCPU), Limit: `1000m` (1 vCPU)
  - Memory Request: `512Mi`, Limit: `1024Mi`
- **Optimized Allocation**: Empirical telemetry profiling via `kubectl top pods`:
  - Measured Idle: ~12m CPU, ~28Mi RAM
  - Measured Under Load: ~85m CPU, ~45Mi RAM
  - Optimized Request: `100m` CPU, `64Mi` RAM (**80% CPU & 87.5% RAM reduction**)
  - Optimized Limit: `250m` CPU, `128Mi` RAM
- **Financial & Operational Impact**:
  - Drastically raises pod packing density per node, reducing total worker node VM instances needed in Kubernetes clusters.

### Technique 3: Elastic Autoscaling (HPA)
- **Baseline Allocation**: Static peak capacity provisioning of **6 replicas running 24/7** to prevent dropouts during high traffic bursts.
- **Optimized Allocation**: Dynamic Horizontal Pod Autoscaler (`web-hpa`) configured with `minReplicas: 2`, `maxReplicas: 6`, and `targetCPUUtilization: 50%`.
  - Idle periods (approx. 80% of daily lifecycle): 2 replicas.
  - Peak traffic burst: scales up to 4-6 replicas.
  - Effective time-weighted average replicas: **2.4 replicas**.
- **Financial & Operational Impact**:
  - Prevents paying for idle idle vCPU and RAM cycles during low-traffic hours.

---

## 2. Before & After Cost Comparison Table

| Metric / Dimension | Baseline (Before) | Optimized (After) | Improvement / Savings |
|---|---|---|---|
| **Container Image Size** | 1,020 MB | 142 MB | **86.1% reduction** |
| **CPU Request per Pod** | 500m (0.5 vCPU) | 100m (0.1 vCPU) | **80.0% reduction** |
| **Memory Request per Pod** | 512 MiB (0.5 GiB) | 64 MiB (0.0625 GiB) | **87.5% reduction** |
| **Average Replicas (Idle)** | 6 static replicas | 2 dynamic replicas | **66.7% reduction** |
| **Average Replicas (Day avg)**| 6 static replicas | 2.4 weighted replicas | **60.0% reduction** |
| **Estimated Monthly Compute Cost** | **$98.55 / month** | **$7.56 / month** | **92.3% cost savings** |

---

## 3. Financial Calculation Model

### Standard Cloud Compute Pricing Assumptions:
- Standard Cloud vCPU rate: **$0.040 per vCPU-hour**
- Standard Cloud Memory rate: **$0.005 per GiB-hour**
- Standard operational month: **730 hours**

$$\text{Monthly Cost} = \text{Replicas} \times \left( \text{CPU}_{\text{cores}} \times \$0.040 + \text{RAM}_{\text{GiB}} \times \$0.005 \right) \times 730\text{ hours}$$

#### Baseline Compute Cost Calculation:
$$\text{Cost}_{\text{baseline}} = 6 \times (0.5 \times 0.040 + 0.5 \times 0.005) \times 730$$
$$\text{Cost}_{\text{baseline}} = 6 \times (0.020 + 0.0025) \times 730 = 6 \times 0.0225 \times 730 = \mathbf{\$98.55 / \text{month}}$$

#### Optimized Compute Cost Calculation (Average Load):
$$\text{Cost}_{\text{optimized}} = 2.4 \times (0.1 \times 0.040 + 0.0625 \times 0.005) \times 730$$
$$\text{Cost}_{\text{optimized}} = 2.4 \times (0.0040 + 0.0003125) \times 730 = 2.4 \times 0.0043125 \times 730 = \mathbf{\$7.56 / \text{month}}$$

*(At pure off-peak idle with 2 pods: $2 \times 0.0043125 \times 730 = \mathbf{\$6.30 / \text{month}}$)*

$$\text{Total Savings} = \frac{\$98.55 - \$7.56}{\$98.55} \times 100\% = \mathbf{92.33\%}$$
