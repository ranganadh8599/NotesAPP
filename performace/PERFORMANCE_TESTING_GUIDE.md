# Performance Testing Guide

## Overview

This guide explains how to run performance tests on the Notes API and generate comprehensive performance reports.

## Prerequisites

- Docker containers must be running (`docker-compose up -d`)
- Python 3.x installed
- `requests` library installed (`pip install requests`)

## Quick Start

### Manual Execution

```bash
# 1. Start Docker containers
docker-compose up -d

# 2. Run performance tests
python performance_test.py

# 3. Generate reports (replace with your results file)
python generate_report.py performance_results_<TIME_STAMP>.json
```

## Test Suite

The performance test suite includes the following tests:

### 1. Health Endpoint Performance
- **Requests:** 100
- **Purpose:** Test basic API responsiveness
- **Endpoint:** `GET /health`

### 2. User Signup Performance
- **Requests:** 50
- **Purpose:** Test user registration performance
- **Endpoint:** `POST /auth/signup`
- **Notes:** Creates unique users for each request

### 3. User Signin Performance
- **Requests:** 100
- **Purpose:** Test authentication performance
- **Endpoint:** `POST /auth/signin`
- **Notes:** Uses a single test user for all requests

### 4. Notes Creation Performance
- **Requests:** 100
- **Purpose:** Test note creation performance
- **Endpoint:** `POST /notes`
- **Notes:** Requires authentication

### 5. Notes Read Performance
- **Requests:** 100
- **Purpose:** Test note retrieval performance
- **Endpoint:** `GET /notes`
- **Notes:** Requires authentication

### 6. Concurrent Requests Performance
- **Threads:** 20
- **Requests per Thread:** 10
- **Total Requests:** 200
- **Purpose:** Test API performance under concurrent load
- **Endpoint:** `POST /notes`
- **Notes:** Simulates multiple users accessing the API simultaneously

## Metrics Collected

For each test, the following metrics are collected:

### Request Statistics
- Total requests
- Successful requests
- Failed requests
- Success rate (%)
- Error count

### Response Time Metrics
- Minimum response time (ms)
- Maximum response time (ms)
- Average response time (ms)
- Median response time (ms)
- 95th percentile (ms)
- 99th percentile (ms)
- Standard deviation (ms)

### Throughput Metrics
- Total duration (seconds)
- Requests per second

## Generated Reports

### 1. JSON Results File
**Filename:** `performance_results_YYYYMMDD_HHMMSS.json`

Raw test data in JSON format. Contains all metrics and configuration details.

### 2. HTML Report
**Filename:** `performance_results_YYYYMMDD_HHMMSS.html`

Beautiful, interactive HTML report with:
- Executive summary dashboard
- Detailed metrics for each test
- Color-coded performance indicators
- Test configuration details
- Performance analysis and recommendations

**Features:**
- Professional design with gradient backgrounds
- Responsive layout
- Print-friendly styling
- Easy to share with stakeholders

### 3. Markdown Report
**Filename:** `performance_results_YYYYMMDD_HHMMSS.md`

Markdown-formatted report suitable for:
- GitHub/GitLab documentation
- Technical documentation
- Version control
- Easy text editing

**Includes:**
- Executive summary table
- Detailed metrics tables
- Performance analysis
- Recommendations

## Understanding the Results

### Success Rate
- **95-100%:** Excellent - API is highly reliable
- **80-94%:** Good - Minor issues may exist
- **Below 80%:** Poor - Investigate errors immediately

### Response Times
- **< 100ms:** Excellent performance
- **100-300ms:** Good performance
- **300-1000ms:** Acceptable performance
- **> 1000ms:** Poor performance - optimization needed

### Requests per Second
- Higher is better
- Indicates API throughput capacity
- Compare across different endpoints to identify bottlenecks

### Percentiles
- **95th Percentile:** 95% of requests completed within this time
- **99th Percentile:** 99% of requests completed within this time
- Important for understanding worst-case scenarios

## Customizing Tests

You can modify test parameters in `performance_test.py`:

```python
# In the main() function, adjust these values:

metrics_health = test_health_endpoint(100)  # Change 100 to desired count
metrics_signup = test_auth_signup(50)       # Change 50 to desired count
metrics_signin = test_auth_signin(100)      # Change 100 to desired count
metrics_create = test_notes_create(100, token)  # Change 100 to desired count
metrics_read = test_notes_read(100, token)      # Change 100 to desired count
metrics_concurrent = test_concurrent_requests(20, 10)  # 20 threads, 10 requests each
```

## Troubleshooting

### Error: Cannot connect to server

**Problem:** The API server is not running or not accessible.

**Solution:**
```bash
# Check if containers are running
docker ps

# If not running, start them
docker-compose up -d

# Check logs
docker logs notes_backend
```

### Error: High failure rate

**Problem:** Many requests are failing.

**Solution:**
1. Check Docker container logs: `docker logs notes_backend`
2. Check database connection: `docker logs notes_mysql`
3. Verify database is healthy: `docker ps` (check health status)
4. Reduce concurrent load and retry

## Support

If you encounter issues:

1. Check Docker container status: `docker ps`
2. Review container logs: `docker logs notes_backend`
3. Verify API health: `curl http://localhost:8000/health`
4. Check Python version: `python --version`
5. Verify dependencies: `pip list`

## Files

- `performance_test.py` - Main performance testing script
- `generate_report.py` - Report generation script
- `performance_results_*.json` - Test results (generated)
- `performance_results_*.html` - HTML report (generated)
- `performance_results_*.md` - Markdown report (generated)

---

**Note:** Performance results may vary based on system resources, Docker configuration, and concurrent system load. For consistent results, run tests on a dedicated testing environment.
