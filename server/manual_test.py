#!/usr/bin/env python3
"""
Simple manual test for PACT API
Run this while server is running in another terminal

Usage:
  Terminal 1: uvicorn src.main:app --reload
  Terminal 2: python manual_test.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("\n" + "="*60)
    print("🧪 PACT API Manual Test")
    print("="*60)
    
    # 1. Health Check
    print("\n1️⃣  Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   ✅ Health check passed!")
    
    # 2. Create Session
    print("\n2️⃣  Creating Session...")
    response = requests.post(f"{BASE_URL}/sessions")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {data}")
    session_id = data["session_id"]
    print(f"   ✅ Created session: {session_id}")
    
    # 3. Get Context (empty)
    print("\n3️⃣  Getting Context (should be empty)...")
    response = requests.get(f"{BASE_URL}/sessions/{session_id}/context")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✅ Got empty context!")
    
    # 4. Save Interaction
    print("\n4️⃣  Saving Interaction...")
    response = requests.post(
        f"{BASE_URL}/sessions/{session_id}/interactions",
        params={
            "user_message": "Hello! I'm testing PACT API.",
            "ai_message": "Great! The API is working."
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✅ Saved interaction!")
    
    # 5. Get Context (with data)
    print("\n5️⃣  Getting Context (should have data)...")
    response = requests.get(f"{BASE_URL}/sessions/{session_id}/context")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    print("   ✅ Got context with data!")
    
    # 6. Test Not Found
    print("\n6️⃣  Testing Non-existent Session...")
    response = requests.get(f"{BASE_URL}/sessions/fake-id/context")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✅ Correctly handled missing session!")
    
    print("\n" + "="*60)
    print("✅ ALL MANUAL TESTS PASSED!")
    print("="*60)
    print("\nYour API is working! 🎉")
    print(f"\nSession ID for further testing: {session_id}")
    print("\nYou can test in browser:")
    print(f"  - Health: {BASE_URL}/health")
    print(f"  - Context: {BASE_URL}/sessions/{session_id}/context")
    print(f"  - Docs: {BASE_URL}/docs (FastAPI auto-docs)")
    print()

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("   Make sure server is running:")
        print("   uvicorn src.main:app --reload")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
