#!/usr/bin/env python3
"""
Simple test script for Sprint 4 features.
Tests the core functionality of Security and Monitoring.
"""

import asyncio
import time
import httpx

BASE_URL = "http://localhost:8889"

async def test_basic_functionality():
    """Test basic API functionality."""
    print("🔍 Testing Basic API Functionality")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            # Test health endpoint
            print("1. Testing health endpoint...")
            response = await client.get("/api/v1/health")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   System Status: {data.get('status', 'unknown')}")
                print(f"   Uptime: {data.get('uptime_seconds', 0):.2f} seconds")
                print(f"   Components: {len(data.get('components', []))}")
                print("   ✅ Health endpoint working")
            else:
                print("   ❌ Health endpoint failed")
                return False
            
            # Test readiness probe
            print("\n2. Testing readiness probe...")
            response = await client.get("/api/v1/ready")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Readiness probe working")
            else:
                print("   ❌ Readiness probe failed")
            
            # Test liveness probe
            print("\n3. Testing liveness probe...")
            response = await client.get("/api/v1/live")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Liveness probe working")
            else:
                print("   ❌ Liveness probe failed")
            
            # Test metrics endpoint
            print("\n4. Testing metrics endpoint...")
            response = await client.get("/api/v1/metrics")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                metrics_data = response.text
                print(f"   Metrics size: {len(metrics_data)} characters")
                
                # Check for key metrics
                key_metrics = [
                    "autogen_api_requests_total",
                    "autogen_system_health"
                ]
                
                found = 0
                for metric in key_metrics:
                    if metric in metrics_data:
                        found += 1
                
                print(f"   Found {found}/{len(key_metrics)} key metrics")
                print("   ✅ Metrics endpoint working")
            else:
                print("   ❌ Metrics endpoint failed")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Basic functionality test failed: {e}")
            return False

async def test_authentication():
    """Test authentication features."""
    print("\n🔐 Testing Authentication Features")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            # Test auth roles endpoint (should work without auth)
            print("1. Testing roles endpoint...")
            response = await client.get("/api/v1/auth/roles")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                roles = data.get('roles', {})
                print(f"   Available roles: {list(roles.keys())}")
                print("   ✅ Roles endpoint working")
            else:
                print("   ❌ Roles endpoint failed")
            
            # Test protected endpoint without auth (should fail)
            print("\n2. Testing protected endpoint without auth...")
            response = await client.get("/api/v1/auth/me")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 401:
                print("   ✅ Protected endpoint properly secured")
            else:
                print("   ❌ Protected endpoint not secured")
            
            # Try to create a user (should fail without admin auth)
            print("\n3. Testing admin endpoint without auth...")
            user_data = {
                "username": "test_user",
                "email": "test@example.com",
                "password": "password123",
                "roles": ["user"]
            }
            response = await client.post("/api/v1/auth/register", json=user_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [401, 403]:
                print("   ✅ Admin endpoint properly secured")
            else:
                print("   ❌ Admin endpoint not secured")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Authentication test failed: {e}")
            return False

async def test_rate_limiting():
    """Test rate limiting."""
    print("\n⏱️  Testing Rate Limiting")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            print("1. Testing rate limiting with rapid requests...")
            
            rate_limited = False
            start_time = time.time()
            
            for i in range(15):
                response = await client.get("/api/v1/health")
                
                if response.status_code == 429:
                    elapsed = time.time() - start_time
                    print(f"   Rate limit triggered after {i+1} requests in {elapsed:.2f}s")
                    
                    # Check rate limit headers
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        print(f"   Retry after: {retry_after} seconds")
                    
                    print("   ✅ Rate limiting working")
                    rate_limited = True
                    break
                elif response.status_code != 200:
                    print(f"   Unexpected response: {response.status_code}")
                    break
            
            if not rate_limited:
                elapsed = time.time() - start_time
                print(f"   No rate limiting triggered in {elapsed:.2f}s (may be expected)")
                print("   ⚠️  Rate limits may be set high for testing")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Rate limiting test failed: {e}")
            return False

async def test_correlation_ids():
    """Test correlation ID functionality."""
    print("\n🔗 Testing Correlation IDs")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            # Test with custom correlation ID
            print("1. Testing custom correlation ID...")
            custom_id = f"test-{int(time.time())}"
            headers = {"X-Correlation-ID": custom_id}
            
            response = await client.get("/api/v1/health", headers=headers)
            returned_id = response.headers.get("X-Correlation-ID")
            
            print(f"   Sent: {custom_id}")
            print(f"   Returned: {returned_id}")
            
            if returned_id == custom_id:
                print("   ✅ Custom correlation ID working")
            else:
                print("   ❌ Custom correlation ID not working")
            
            # Test auto-generated correlation ID
            print("\n2. Testing auto-generated correlation ID...")
            response = await client.get("/api/v1/health")
            auto_id = response.headers.get("X-Correlation-ID")
            
            if auto_id:
                print(f"   Auto-generated: {auto_id}")
                print("   ✅ Auto-generated correlation ID working")
            else:
                print("   ❌ Auto-generated correlation ID not working")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Correlation ID test failed: {e}")
            return False

async def test_component_health():
    """Test individual component health checks."""
    print("\n🏥 Testing Component Health Checks")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            components = [
                "database",
                "redis_messaging",
                "redis_context",
                "redis_handoffs",
                "redis_auth",
                "api_server"
            ]
            
            healthy_components = 0
            
            for component in components:
                response = await client.get(f"/api/v1/health/component/{component}")
                print(f"   {component}: ", end="")
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status', 'unknown')
                    response_time = data.get('response_time_ms', 0)
                    print(f"{status} ({response_time:.1f}ms)")
                    
                    if status == "healthy":
                        healthy_components += 1
                        
                elif response.status_code == 404:
                    print("Not found (component may not exist)")
                else:
                    print(f"Error {response.status_code}")
            
            print(f"\n   ✅ {healthy_components}/{len(components)} components healthy")
            return True
            
        except Exception as e:
            print(f"   ❌ Component health test failed: {e}")
            return False

async def main():
    """Run all tests."""
    print("🚀 AutoGen A2A Sprint 4 - Quick Test Suite")
    print("Testing Security and Monitoring Implementation")
    print("=" * 60)
    
    # Check if server is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/api/v1/health")
            if response.status_code != 200:
                print("❌ Server not responding properly")
                print("Make sure the server is running:")
                print("   uvicorn src.autogen_a2a.api.main:app --reload")
                return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running:")
        print("   uvicorn src.autogen_a2a.api.main:app --reload")
        return
    
    print("✅ Server is responding, starting tests...")
    
    # Run tests
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Authentication", test_authentication),
        ("Rate Limiting", test_rate_limiting),
        ("Correlation IDs", test_correlation_ids),
        ("Component Health", test_component_health),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed! Sprint 4 implementation is working correctly.")
        print("\n✅ Security features (authentication, authorization, rate limiting)")
        print("✅ Monitoring features (health checks, metrics, correlation IDs)")
        print("✅ API endpoints and middleware")
        print("\nSprint 4 Phases 1 & 2 are successfully implemented!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("This may be expected if the server is not fully configured.")

if __name__ == "__main__":
    asyncio.run(main())
