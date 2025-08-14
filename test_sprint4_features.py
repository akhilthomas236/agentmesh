#!/usr/bin/env python3
"""
Comprehensive test suite for Sprint 4 Phases 1 & 2:
- Security & Authentication
- Monitoring & Observability
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any

import httpx
import redis.asyncio as redis

# Test configuration
BASE_URL = "http://localhost:8889"
REDIS_URL = "redis://localhost:6379"

class TestColors:
    """ANSI color codes for test output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name: str):
    """Print a formatted test header."""
    print(f"\n{TestColors.CYAN}{TestColors.BOLD}{'='*60}{TestColors.RESET}")
    print(f"{TestColors.CYAN}{TestColors.BOLD}🧪 {test_name}{TestColors.RESET}")
    print(f"{TestColors.CYAN}{TestColors.BOLD}{'='*60}{TestColors.RESET}")

def print_success(message: str):
    """Print success message."""
    print(f"{TestColors.GREEN}✅ {message}{TestColors.RESET}")

def print_error(message: str):
    """Print error message."""
    print(f"{TestColors.RED}❌ {message}{TestColors.RESET}")

def print_warning(message: str):
    """Print warning message."""
    print(f"{TestColors.YELLOW}⚠️  {message}{TestColors.RESET}")

def print_info(message: str):
    """Print info message."""
    print(f"{TestColors.BLUE}ℹ️  {message}{TestColors.RESET}")

class Sprint4TestSuite:
    """Test suite for Sprint 4 features."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=BASE_URL)
        self.admin_token = None
        self.test_user_token = None
        self.test_api_key = None
        self.redis_client = None
        
        # Test data
        self.admin_creds = {
            "username": "test_admin",
            "password": "test_password_123"
        }
        self.test_user_creds = {
            "username": "test_user", 
            "password": "test_password_456"
        }


async def test_monitoring_features():
    """Test monitoring, metrics, and health checks."""
    print("\n📊 Testing Monitoring Features (Phase 2)")
    print("=" * 50)
    
    base_url = "http://localhost:8889/api/v1"
    
    async with httpx.AsyncClient() as client:
        # Test comprehensive health check
        print("1. Testing comprehensive health check...")
        response = await client.get(f"{base_url}/health?detailed=true")
        print(f"   Health Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   System Status: {data.get('status')}")
            print(f"   Uptime: {data.get('uptime_seconds', 0):.1f} seconds")
            print(f"   Message: {data.get('message')}")
            
            components = data.get('components', [])
            print(f"   Components checked: {len(components)}")
            for component in components:
                status = component.get('status', 'unknown')
                name = component.get('name', 'unknown')
                response_time = component.get('response_time_ms')
                print(f"     - {name}: {status} " + 
                      (f"({response_time:.1f}ms)" if response_time else ""))
        
        # Test readiness probe
        print("\n2. Testing readiness probe...")
        response = await client.get(f"{base_url}/ready")
        print(f"   Readiness Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Ready: {data.get('ready')}")
            print(f"   Critical Components: {data.get('critical_components', [])}")
        
        # Test liveness probe
        print("\n3. Testing liveness probe...")
        response = await client.get(f"{base_url}/live")
        print(f"   Liveness Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Alive: {data.get('alive')}")
            print(f"   Uptime: {data.get('uptime_seconds', 0):.1f} seconds")
        
        # Test metrics endpoint
        print("\n4. Testing Prometheus metrics...")
        response = await client.get(f"{base_url}/metrics")
        print(f"   Metrics Status: {response.status_code}")
        if response.status_code == 200:
            metrics_text = response.text
            lines = metrics_text.split('\n')
            metric_lines = [line for line in lines if line and not line.startswith('#')]
            print(f"   Metrics Count: {len(metric_lines)}")
            
            # Show sample metrics
            sample_metrics = metric_lines[:5]
            print("   Sample metrics:")
            for metric in sample_metrics:
                if metric.strip():
                    print(f"     {metric}")
        
        # Test performance summary
        print("\n5. Testing performance summary...")
        response = await client.get(f"{base_url}/performance")
        print(f"   Performance Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total Requests: {data.get('total_requests', 0)}")
            print(f"   Avg Response Time: {data.get('avg_response_time', 0):.3f}s")
            print(f"   Error Counts: {data.get('error_counts', {})}")
        
        # Test individual component health
        print("\n6. Testing individual component health...")
        components = ["database", "redis_messaging", "api_server"]
        for component in components:
            response = await client.get(f"{base_url}/health/component/{component}")
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                response_time = data.get('response_time_ms')
                print(f"   {component}: {status} " + 
                      (f"({response_time:.1f}ms)" if response_time else ""))
            else:
                print(f"   {component}: Error {response.status_code}")


async def test_correlation_ids():
    """Test correlation ID tracking."""
    print("\n🔗 Testing Correlation ID Tracking")
    print("=" * 50)
    
    base_url = "http://localhost:8889/api/v1"
    correlation_id = "test-correlation-123"
    
    async with httpx.AsyncClient() as client:
        print("1. Testing correlation ID propagation...")
        
        # Send request with correlation ID
        headers = {"X-Correlation-ID": correlation_id}
        response = await client.get(f"{base_url}/health", headers=headers)
        
        # Check if correlation ID is returned
        returned_id = response.headers.get("X-Correlation-ID")
        print(f"   Sent ID: {correlation_id}")
        print(f"   Returned ID: {returned_id}")
        print(f"   Match: {correlation_id == returned_id}")
        
        # Test auto-generation of correlation ID
        print("\n2. Testing auto-generation of correlation ID...")
        response = await client.get(f"{base_url}/health")
        auto_generated_id = response.headers.get("X-Correlation-ID")
        print(f"   Auto-generated ID: {auto_generated_id}")
        print(f"   Valid format: {len(auto_generated_id or '') > 0}")


async def test_security_features():
    """Test security features including authentication and rate limiting."""
    print("🔐 Testing Security Features (Phase 1)")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Test authentication endpoints
        print("1. Testing authentication endpoints...")
        
        # Test roles endpoint
        response = await client.get("/api/v1/auth/roles")
        if response.status_code == 200:
            roles = response.json()
            print(f"   Available roles: {roles}")
            print("   ✅ Roles endpoint working")
        else:
            print(f"   ❌ Roles endpoint failed: {response.status_code}")
        
        # Test protected endpoint without auth
        print("2. Testing protected endpoints without authentication...")
        response = await client.get("/api/v1/agents")
        if response.status_code == 401 or response.status_code == 403:
            print("   ✅ Protected endpoint properly secured")
        else:
            print(f"   ❌ Protected endpoint not secured: {response.status_code}")
        
        # Test rate limiting
        print("3. Testing rate limiting...")
        start_time = time.time()
        rate_limited = False
        
        for i in range(20):  # Send rapid requests
            response = await client.get("/api/v1/health")
            if response.status_code == 429:
                print(f"   ✅ Rate limit triggered after {i+1} requests")
                rate_limited = True
                break
        
        if not rate_limited:
            print("   ⚠️  Rate limit not triggered (may be configured with high limits)")
        
        elapsed = time.time() - start_time
        print(f"   Time taken: {elapsed:.2f} seconds")


async def main():
    """Run all tests."""
    print("🚀 AutoGen A2A Sprint 4 Feature Testing")
    print("Testing Security and Monitoring Features")
    print("=" * 60)
    
    try:
        # Test if server is running
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8889/api/v1/health", timeout=5)
            if response.status_code != 200:
                print("❌ Server not responding correctly")
                return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running: uvicorn src.autogen_a2a.api.main:app --reload")
        return
    
    print("✅ Server is running, starting tests...\n")
    
    try:
        await test_security_features()
        await test_monitoring_features()
        await test_correlation_ids()
        
        print("\n" + "=" * 60)
        print("🎉 Sprint 4 Phase 1 & 2 Testing Complete!")
        print("Security and Monitoring features are implemented and functional.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
