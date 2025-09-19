#!/usr/bin/env python3
"""
Simple test script to verify FastAPI + LLM endpoints are working
"""
import requests
import json
import time

def test_endpoint(url, method="GET", data=None, description=""):
    """Test an API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"📍 {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            result = response.json()
            print(f"📝 Response: {json.dumps(result, indent=2)}")
        else:
            print("❌ Error!")
            print(f"📝 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error! Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run API tests"""
    base_url = "http://localhost:8000"
    
    print("🚀 FastAPI + LLM API Testing")
    print("=" * 50)
    
    # Test health endpoints
    test_endpoint(f"{base_url}/", "GET", description="Root health check")
    test_endpoint(f"{base_url}/health", "GET", description="Health check endpoint")
    
    # Test advanced endpoints that don't require API key
    test_endpoint(f"{base_url}/advanced/models", "GET", description="List available models")
    
    # Test chat endpoint (will show error without API key, but proves validation works)
    chat_data = {
        "message": "Hello! This is a test message.",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 50
    }
    test_endpoint(f"{base_url}/chat", "POST", chat_data, description="Chat completion (without API key)")
    
    print("\n" + "=" * 50)
    print("🎯 Testing Complete!")
    print("\nNOTE: To test LLM features, add your OpenAI API key to the .env file:")
    print("OPENAI_API_KEY=your_actual_api_key_here")

if __name__ == "__main__":
    main()