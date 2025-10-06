import requests
import time
import statistics
import json
import concurrent.futures
from datetime import datetime
from typing import List, Dict, Tuple
import sys

BASE_URL = "http://localhost:8000"

class PerformanceMetrics:
    def __init__(self):
        self.response_times = []
        self.status_codes = []
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def add_result(self, response_time: float, status_code: int, error: str = None):
        self.response_times.append(response_time)
        self.status_codes.append(status_code)
        if error:
            self.errors.append(error)
    
    def get_stats(self) -> Dict:
        if not self.response_times:
            return {}
        
        sorted_times = sorted(self.response_times)
        total_requests = len(self.response_times)
        successful_requests = sum(1 for code in self.status_codes if 200 <= code < 300)
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': total_requests - successful_requests,
            'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            'min_response_time': min(self.response_times),
            'max_response_time': max(self.response_times),
            'avg_response_time': statistics.mean(self.response_times),
            'median_response_time': statistics.median(self.response_times),
            'p95_response_time': sorted_times[int(len(sorted_times) * 0.95)] if len(sorted_times) > 0 else 0,
            'p99_response_time': sorted_times[int(len(sorted_times) * 0.99)] if len(sorted_times) > 0 else 0,
            'std_dev': statistics.stdev(self.response_times) if len(self.response_times) > 1 else 0,
            'total_duration': self.end_time - self.start_time if self.end_time and self.start_time else 0,
            'requests_per_second': total_requests / (self.end_time - self.start_time) if self.end_time and self.start_time and (self.end_time - self.start_time) > 0 else 0,
            'errors': len(self.errors),
            'error_details': self.errors[:10]
        }

def make_request(url: str, method: str = "GET", headers: Dict = None, json_data: Dict = None) -> Tuple[float, int, str]:
    try:
        start = time.time()
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json_data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        end = time.time()
        
        return (end - start) * 1000, response.status_code, None
    except Exception as e:
        return 0, 0, str(e)

def setup_test_user() -> str:
    """Create a test user and return auth token"""
    timestamp = int(time.time())
    signup_data = {
        "user_name": f"PerfTest User {timestamp}",
        "user_email": f"perftest{timestamp}@example.com",
        "password": "testpass123"
    }
    
    try:
        requests.post(f"{BASE_URL}/auth/signup", json=signup_data, timeout=10)
    except:
        pass
    
    signin_data = {
        "user_email": signup_data["user_email"],
        "password": signup_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data, timeout=10)
    return response.json()["access_token"]

def test_health_endpoint(num_requests: int = 100) -> PerformanceMetrics:
    print(f"\nTesting Health Endpoint ({num_requests} requests)...")
    metrics = PerformanceMetrics()
    metrics.start_time = time.time()
    
    for i in range(num_requests):
        response_time, status_code, error = make_request(f"{BASE_URL}/health")
        metrics.add_result(response_time, status_code, error)
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    metrics.end_time = time.time()
    return metrics

def test_auth_signup(num_requests: int = 50) -> PerformanceMetrics:
    print(f"\nTesting User Signup ({num_requests} requests)...")
    metrics = PerformanceMetrics()
    metrics.start_time = time.time()
    
    for i in range(num_requests):
        timestamp = int(time.time() * 1000000) + i
        signup_data = {
            "user_name": f"User {timestamp}",
            "user_email": f"user{timestamp}@test.com",
            "password": "password123"
        }
        response_time, status_code, error = make_request(
            f"{BASE_URL}/auth/signup", 
            method="POST", 
            json_data=signup_data
        )
        metrics.add_result(response_time, status_code, error)
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    metrics.end_time = time.time()
    return metrics

def test_auth_signin(num_requests: int = 100) -> PerformanceMetrics:
    print(f"\nTesting User Signin ({num_requests} requests)...")
    
    # Create test user first
    timestamp = int(time.time())
    signup_data = {
        "user_name": f"SigninTest User",
        "user_email": f"signintest{timestamp}@example.com",
        "password": "testpass123"
    }
    requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    metrics = PerformanceMetrics()
    metrics.start_time = time.time()
    
    signin_data = {
        "user_email": signup_data["user_email"],
        "password": signup_data["password"]
    }
    
    for i in range(num_requests):
        response_time, status_code, error = make_request(
            f"{BASE_URL}/auth/signin", 
            method="POST", 
            json_data=signin_data
        )
        metrics.add_result(response_time, status_code, error)
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    metrics.end_time = time.time()
    return metrics

def test_notes_create(num_requests: int = 100, token: str = None) -> PerformanceMetrics:
    print(f"\nTesting Notes Creation ({num_requests} requests)...")
    
    if not token:
        token = setup_test_user()
    
    headers = {"Authorization": f"Bearer {token}"}
    metrics = PerformanceMetrics()
    metrics.start_time = time.time()
    
    for i in range(num_requests):
        note_data = {
            "note_title": f"Performance Test Note {i}",
            "note_content": f"This is test note number {i} created for performance testing."
        }
        response_time, status_code, error = make_request(
            f"{BASE_URL}/notes", 
            method="POST", 
            headers=headers,
            json_data=note_data
        )
        metrics.add_result(response_time, status_code, error)
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    metrics.end_time = time.time()
    return metrics

def test_notes_read(num_requests: int = 100, token: str = None) -> PerformanceMetrics:
    print(f"\nTesting Notes Read ({num_requests} requests)...")
    
    if not token:
        token = setup_test_user()
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create some notes first
    for i in range(5):
        note_data = {
            "note_title": f"Read Test Note {i}",
            "note_content": f"Content for read test {i}"
        }
        requests.post(f"{BASE_URL}/notes", headers=headers, json=note_data)
    
    metrics = PerformanceMetrics()
    metrics.start_time = time.time()
    
    for i in range(num_requests):
        response_time, status_code, error = make_request(
            f"{BASE_URL}/notes", 
            method="GET", 
            headers=headers
        )
        metrics.add_result(response_time, status_code, error)
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    metrics.end_time = time.time()
    return metrics

def test_concurrent_requests(num_concurrent: int = 20, requests_per_thread: int = 10) -> PerformanceMetrics:
    print(f"\nTesting Concurrent Requests ({num_concurrent} threads, {requests_per_thread} requests each)...")
    
    token = setup_test_user()
    headers = {"Authorization": f"Bearer {token}"}
    
    metrics = PerformanceMetrics()
    metrics.start_time = time.time()
    
    def worker(thread_id):
        results = []
        for i in range(requests_per_thread):
            note_data = {
                "note_title": f"Concurrent Test {thread_id}-{i}",
                "note_content": f"Thread {thread_id}, Request {i}"
            }
            result = make_request(
                f"{BASE_URL}/notes", 
                method="POST", 
                headers=headers,
                json_data=note_data
            )
            results.append(result)
        return results
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(worker, i) for i in range(num_concurrent)]
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            results = future.result()
            for response_time, status_code, error in results:
                metrics.add_result(response_time, status_code, error)
            completed += 1
            print(f"  Completed threads: {completed}/{num_concurrent}")
    
    metrics.end_time = time.time()
    return metrics

def print_stats(test_name: str, metrics: PerformanceMetrics):
    stats = metrics.get_stats()
    
    print(f"\n{'='*70}")
    print(f"  {test_name}")
    print(f"{'='*70}")
    print(f"Total Requests:        {stats['total_requests']}")
    print(f"Successful:            {stats['successful_requests']} ({stats['success_rate']:.2f}%)")
    print(f"Failed:                {stats['failed_requests']}")
    print(f"Errors:                {stats['errors']}")
    print(f"\nResponse Times (ms):")
    print(f"  Min:                 {stats['min_response_time']:.2f}")
    print(f"  Max:                 {stats['max_response_time']:.2f}")
    print(f"  Average:             {stats['avg_response_time']:.2f}")
    print(f"  Median:              {stats['median_response_time']:.2f}")
    print(f"  95th Percentile:     {stats['p95_response_time']:.2f}")
    print(f"  99th Percentile:     {stats['p99_response_time']:.2f}")
    print(f"  Std Deviation:       {stats['std_dev']:.2f}")
    print(f"\nThroughput:")
    print(f"  Total Duration:      {stats['total_duration']:.2f}s")
    print(f"  Requests/Second:     {stats['requests_per_second']:.2f}")
    
    if stats['error_details']:
        print(f"\nError Samples:")
        for error in stats['error_details'][:3]:
            print(f"  - {error}")

def save_results(results: Dict):
    import os
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, f"performance_results_{timestamp}.json")
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {filename}")
    return filename

def main():
    print("\n" + "*"*35)
    print("  NOTES API - PERFORMANCE TEST SUITE")
    print("*"*35)
    
    try:
        # Check if server is running
        print("\nChecking server availability...")
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Server is running (Status: {response.status_code})")
    except:
        print("\nERROR: Cannot connect to server")
        print("Make sure the server is running on http://localhost:8000")
        print("\nStart with: docker-compose up")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("  STARTING PERFORMANCE TESTS")
    print("="*70)
    
    results = {}
    
    # Run tests
    token = setup_test_user()
    
    metrics_health = test_health_endpoint(100)
    print_stats("Health Endpoint Performance", metrics_health)
    results['health_endpoint'] = metrics_health.get_stats()
    
    metrics_signup = test_auth_signup(50)
    print_stats("User Signup Performance", metrics_signup)
    results['user_signup'] = metrics_signup.get_stats()
    
    metrics_signin = test_auth_signin(100)
    print_stats("User Signin Performance", metrics_signin)
    results['user_signin'] = metrics_signin.get_stats()
    
    metrics_create = test_notes_create(100, token)
    print_stats("Notes Creation Performance", metrics_create)
    results['notes_create'] = metrics_create.get_stats()
    
    metrics_read = test_notes_read(100, token)
    print_stats("Notes Read Performance", metrics_read)
    results['notes_read'] = metrics_read.get_stats()
    
    metrics_concurrent = test_concurrent_requests(20, 10)
    print_stats("Concurrent Requests Performance", metrics_concurrent)
    results['concurrent_requests'] = metrics_concurrent.get_stats()
    
    # Save results
    results['test_timestamp'] = datetime.now().isoformat()
    results['test_configuration'] = {
        'base_url': BASE_URL,
        'health_requests': 100,
        'signup_requests': 50,
        'signin_requests': 100,
        'notes_create_requests': 100,
        'notes_read_requests': 100,
        'concurrent_threads': 20,
        'requests_per_thread': 10
    }
    
    filename = save_results(results)
    
    print("\n" + "="*70)
    print("ALL PERFORMANCE TESTS COMPLETED!")
    print("="*70)
    print(f"\nResults file: {filename}")
    print("\nNext step: Run 'python generate_report.py {filename}' to create HTML report")

if __name__ == "__main__":
    main()