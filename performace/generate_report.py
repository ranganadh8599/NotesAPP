import json
import sys
from datetime import datetime
import os

def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def generate_html_report(results, output_file):
    timestamp = results.get('test_timestamp', 'Unknown')
    config = results.get('test_configuration', {})
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Test Report - Notes API</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        
        .summary-card h3 {{
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }}
        
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        
        .summary-card .unit {{
            font-size: 0.9em;
            color: #666;
            margin-left: 5px;
        }}
        
        .test-section {{
            padding: 40px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .test-section:last-child {{
            border-bottom: none;
        }}
        
        .test-section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .metric {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }}
        
        .metric-label {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }}
        
        .success {{
            color: #28a745;
        }}
        
        .warning {{
            color: #ffc107;
        }}
        
        .danger {{
            color: #dc3545;
        }}
        
        .performance-bar {{
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .performance-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #ffc107 50%, #dc3545 100%);
            transition: width 0.3s ease;
        }}
        
        .config-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            margin-top: 20px;
        }}
        
        .config-section h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .config-item {{
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .config-item:last-child {{
            border-bottom: none;
        }}
        
        .config-label {{
            font-weight: bold;
            color: #666;
            display: inline-block;
            width: 250px;
        }}
        
        .config-value {{
            color: #333;
        }}
        
        .footer {{
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Performance Test Report</h1>
            <p>Notes API - Full Stack Developer Assignment</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: {timestamp}</p>
        </div>
"""
    
    # Calculate overall statistics
    all_tests = ['health_endpoint', 'user_signup', 'user_signin', 'notes_create', 'notes_read', 'concurrent_requests']
    total_requests = sum(results.get(test, {}).get('total_requests', 0) for test in all_tests)
    total_successful = sum(results.get(test, {}).get('successful_requests', 0) for test in all_tests)
    avg_response_times = [results.get(test, {}).get('avg_response_time', 0) for test in all_tests if results.get(test, {}).get('avg_response_time', 0) > 0]
    overall_avg_response = sum(avg_response_times) / len(avg_response_times) if avg_response_times else 0
    overall_success_rate = (total_successful / total_requests * 100) if total_requests > 0 else 0
    
    # Summary cards
    html += f"""
        <div class="summary">
            <div class="summary-card">
                <h3>Total Requests</h3>
                <div class="value">{total_requests}</div>
            </div>
            <div class="summary-card">
                <h3>Success Rate</h3>
                <div class="value {'success' if overall_success_rate >= 95 else 'warning' if overall_success_rate >= 80 else 'danger'}">{overall_success_rate:.2f}<span class="unit">%</span></div>
            </div>
            <div class="summary-card">
                <h3>Avg Response Time</h3>
                <div class="value">{overall_avg_response:.2f}<span class="unit">ms</span></div>
            </div>
            <div class="summary-card">
                <h3>Total Tests</h3>
                <div class="value">{len(all_tests)}</div>
            </div>
        </div>
"""
    
    # Test sections
    test_names = {
        'health_endpoint': 'Health Endpoint Performance',
        'user_signup': 'User Signup Performance',
        'user_signin': 'User Signin Performance',
        'notes_create': 'Notes Creation Performance',
        'notes_read': 'Notes Read Performance',
        'concurrent_requests': 'Concurrent Requests Performance'
    }
    
    for test_key, test_name in test_names.items():
        if test_key not in results:
            continue
        
        stats = results[test_key]
        success_rate = stats.get('success_rate', 0)
        
        html += f"""
        <div class="test-section">
            <h2>{test_name}</h2>
            
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">Total Requests</div>
                    <div class="metric-value">{stats.get('total_requests', 0)}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value {'success' if success_rate >= 95 else 'warning' if success_rate >= 80 else 'danger'}">{success_rate:.2f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Avg Response Time</div>
                    <div class="metric-value">{stats.get('avg_response_time', 0):.2f} ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Min Response Time</div>
                    <div class="metric-value">{stats.get('min_response_time', 0):.2f} ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Max Response Time</div>
                    <div class="metric-value">{stats.get('max_response_time', 0):.2f} ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Median Response Time</div>
                    <div class="metric-value">{stats.get('median_response_time', 0):.2f} ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">95th Percentile</div>
                    <div class="metric-value">{stats.get('p95_response_time', 0):.2f} ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">99th Percentile</div>
                    <div class="metric-value">{stats.get('p99_response_time', 0):.2f} ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Requests/Second</div>
                    <div class="metric-value">{stats.get('requests_per_second', 0):.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total Duration</div>
                    <div class="metric-value">{stats.get('total_duration', 0):.2f} s</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Failed Requests</div>
                    <div class="metric-value {'danger' if stats.get('failed_requests', 0) > 0 else 'success'}">{stats.get('failed_requests', 0)}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Errors</div>
                    <div class="metric-value {'danger' if stats.get('errors', 0) > 0 else 'success'}">{stats.get('errors', 0)}</div>
                </div>
            </div>
        </div>
"""
    
    # Configuration section
    html += f"""
        <div class="test-section">
            <h2>Test Configuration</h2>
            <div class="config-section">
                <div class="config-item">
                    <span class="config-label">Base URL:</span>
                    <span class="config-value">{config.get('base_url', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Health Endpoint Requests:</span>
                    <span class="config-value">{config.get('health_requests', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Signup Requests:</span>
                    <span class="config-value">{config.get('signup_requests', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Signin Requests:</span>
                    <span class="config-value">{config.get('signin_requests', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Notes Create Requests:</span>
                    <span class="config-value">{config.get('notes_create_requests', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Notes Read Requests:</span>
                    <span class="config-value">{config.get('notes_read_requests', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Concurrent Threads:</span>
                    <span class="config-value">{config.get('concurrent_threads', 'N/A')}</span>
                </div>
                <div class="config-item">
                    <span class="config-label">Requests per Thread:</span>
                    <span class="config-value">{config.get('requests_per_thread', 'N/A')}</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Full Stack Developer Assignment - Notes Taking Application</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Performance testing completed successfully</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_markdown_report(results, output_file):
    timestamp = results.get('test_timestamp', 'Unknown')
    config = results.get('test_configuration', {})
    
    md = f"""# Performance Test Report - Notes API

**Full Stack Developer Assignment**

**Generated:** {timestamp}

---

## Executive Summary

"""
    
    # Calculate overall statistics
    all_tests = ['health_endpoint', 'user_signup', 'user_signin', 'notes_create', 'notes_read', 'concurrent_requests']
    total_requests = sum(results.get(test, {}).get('total_requests', 0) for test in all_tests)
    total_successful = sum(results.get(test, {}).get('successful_requests', 0) for test in all_tests)
    avg_response_times = [results.get(test, {}).get('avg_response_time', 0) for test in all_tests if results.get(test, {}).get('avg_response_time', 0) > 0]
    overall_avg_response = sum(avg_response_times) / len(avg_response_times) if avg_response_times else 0
    overall_success_rate = (total_successful / total_requests * 100) if total_requests > 0 else 0
    
    md += f"""| Metric | Value |
|--------|-------|
| Total Requests | {total_requests} |
| Successful Requests | {total_successful} |
| Success Rate | {overall_success_rate:.2f}% |
| Average Response Time | {overall_avg_response:.2f} ms |
| Total Tests Executed | {len(all_tests)} |

---

"""
    
    # Test sections
    test_names = {
        'health_endpoint': 'Health Endpoint Performance',
        'user_signup': 'User Signup Performance',
        'user_signin': 'User Signin Performance',
        'notes_create': 'Notes Creation Performance',
        'notes_read': 'Notes Read Performance',
        'concurrent_requests': 'Concurrent Requests Performance'
    }
    
    for test_key, test_name in test_names.items():
        if test_key not in results:
            continue
        
        stats = results[test_key]
        
        md += f"""## {test_name}

### Request Statistics
- **Total Requests:** {stats.get('total_requests', 0)}
- **Successful:** {stats.get('successful_requests', 0)} ({stats.get('success_rate', 0):.2f}%)
- **Failed:** {stats.get('failed_requests', 0)}
- **Errors:** {stats.get('errors', 0)}

### Response Time Metrics (milliseconds)
| Metric | Value |
|--------|-------|
| Minimum | {stats.get('min_response_time', 0):.2f} ms |
| Maximum | {stats.get('max_response_time', 0):.2f} ms |
| Average | {stats.get('avg_response_time', 0):.2f} ms |
| Median | {stats.get('median_response_time', 0):.2f} ms |
| 95th Percentile | {stats.get('p95_response_time', 0):.2f} ms |
| 99th Percentile | {stats.get('p99_response_time', 0):.2f} ms |
| Standard Deviation | {stats.get('std_dev', 0):.2f} ms |

### Throughput
- **Total Duration:** {stats.get('total_duration', 0):.2f} seconds
- **Requests per Second:** {stats.get('requests_per_second', 0):.2f}

---

"""
    
    # Configuration
    md += f"""## Test Configuration

| Parameter | Value |
|-----------|-------|
| Base URL | {config.get('base_url', 'N/A')} |
| Health Endpoint Requests | {config.get('health_requests', 'N/A')} |
| Signup Requests | {config.get('signup_requests', 'N/A')} |
| Signin Requests | {config.get('signin_requests', 'N/A')} |
| Notes Create Requests | {config.get('notes_create_requests', 'N/A')} |
| Notes Read Requests | {config.get('notes_read_requests', 'N/A')} |
| Concurrent Threads | {config.get('concurrent_threads', 'N/A')} |
| Requests per Thread | {config.get('requests_per_thread', 'N/A')} |

---

## Performance Analysis

### Key Findings

1. **Overall Performance:** The API achieved a {overall_success_rate:.2f}% success rate across {total_requests} total requests.

2. **Response Times:** Average response time across all endpoints was {overall_avg_response:.2f}ms, indicating {'excellent' if overall_avg_response < 100 else 'good' if overall_avg_response < 300 else 'acceptable'} performance.

3. **Reliability:** {'All tests completed successfully with minimal errors.' if overall_success_rate >= 99 else 'Tests completed with some errors that should be investigated.'}

### Recommendations

- **Health Endpoint:** {'Performing optimally' if results.get('health_endpoint', {}).get('avg_response_time', 0) < 50 else 'Consider optimization'}
- **Authentication:** {'Response times are acceptable' if results.get('user_signin', {}).get('avg_response_time', 0) < 200 else 'Consider caching or optimization'}
- **Notes Operations:** {'CRUD operations are efficient' if results.get('notes_create', {}).get('avg_response_time', 0) < 300 else 'Database queries may need optimization'}
- **Concurrency:** {'Handles concurrent requests well' if results.get('concurrent_requests', {}).get('success_rate', 0) >= 95 else 'May need connection pool tuning'}

---

*Report generated automatically by Performance Test Suite*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <results_file.json>")
        print("\nAvailable result files:")
        for file in os.listdir('.'):
            if file.startswith('performance_results_') and file.endswith('.json'):
                print(f"  - {file}")
        sys.exit(1)
    
    results_file = sys.argv[1]
    
    if not os.path.exists(results_file):
        print(f"Error: File '{results_file}' not found")
        sys.exit(1)
    
    print(f"\nGenerating performance reports from: {results_file}")
    
    results = load_results(results_file)
    
    # Generate HTML report
    html_file = results_file.replace('.json', '.html')
    generate_html_report(results, html_file)
    print(f"HTML report generated: {html_file}")
    
    # Generate Markdown report
    md_file = results_file.replace('.json', '.md')
    generate_markdown_report(results, md_file)
    print(f"Markdown report generated: {md_file}")
    
    print(f"\n{'='*70}")
    print("  REPORTS GENERATED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"\nHTML Report:     {html_file}")
    print(f"Markdown Report: {md_file}")
    print(f"JSON Data:       {results_file}")
    print(f"\nOpen the HTML file in your browser to view the detailed report.")

if __name__ == "__main__":
    main()