#!/usr/bin/env python3
"""
Simple API connection test
"""

import requests
import json
import time

def test_backend_connection():
    """Test backend API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Backend API Connection...")
    print("=" * 50)
    
    endpoints = [
        ("/health", "GET", None),
        ("/api/v1/stocks", "GET", None),
        ("/", "GET", None)
    ]
    
    for endpoint, method, data in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🔍 Testing {method} {endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"📄 Response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"📄 Response: {response.text[:200]}...")
            else:
                print(f"❌ Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Backend not running on {base_url}")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout: Backend took too long to respond")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_market_sentiment():
    """Test market sentiment endpoint"""
    
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/v1/market-sentiment"
    
    print(f"\n🔍 Testing POST /api/v1/market-sentiment")
    
    try:
        data = {"timeframe": "current"}
        response = requests.post(url, json=data, timeout=30)
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Response: {json.dumps(result, indent=2)[:300]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting API Connection Test...")
    
    # Test basic connection
    test_backend_connection()
    
    # Test market sentiment (might take longer)
    test_market_sentiment()
    
    print("\n🎉 API Connection Test Complete!")
    print("\n📋 If all tests pass, backend is working correctly.")
    print("📋 If tests fail, check:")
    print("   1. Backend is running: uvicorn app.main:app --host 0.0.0.0 --port 8000")
    print("   2. No port conflicts")
    print("   3. Dependencies are installed")
