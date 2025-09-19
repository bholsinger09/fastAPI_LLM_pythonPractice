#!/usr/bin/env python3
"""
Quick FastAPI test - checks if the app can be imported and basic functionality works
"""

def test_import():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from main import app
        from llm_client import llm_client
        from advanced_endpoints import router
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test FastAPI app structure"""
    print("\n🧪 Testing app structure...")
    try:
        from main import app
        
        # Check routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/chat", "/text", "/conversation"]
        
        print(f"📍 Found routes: {routes}")
        
        basic_routes_found = all(route in routes for route in expected_routes)
        advanced_routes_found = any("/advanced" in route for route in routes)
        
        if basic_routes_found and advanced_routes_found:
            print("✅ All expected routes found!")
            return True
        else:
            print("⚠️  Some routes missing")
            return False
            
    except Exception as e:
        print(f"❌ App structure error: {e}")
        return False

def test_pydantic_models():
    """Test Pydantic models"""
    print("\n🧪 Testing Pydantic models...")
    try:
        from main import ChatRequest, ChatResponse, HealthResponse
        
        # Test model creation
        health = HealthResponse(status="test", message="test message")
        print(f"✅ HealthResponse: {health}")
        
        chat_req = ChatRequest(message="test message")
        print(f"✅ ChatRequest: {chat_req}")
        
        return True
    except Exception as e:
        print(f"❌ Pydantic model error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 FastAPI + LLM Quick Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_import),
        ("App Structure", test_app_structure),
        ("Pydantic Models", test_pydantic_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Tests Complete: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Your FastAPI app is ready.")
        print("\nTo start the server manually:")
        print("uvicorn main:app --reload")
        print("\nThen visit:")
        print("• http://localhost:8000/docs (Interactive API docs)")
        print("• http://localhost:8000/health (Health check)")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()