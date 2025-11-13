# test_api.py
"""
Simple tests for PACT API server
Run with: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

# Create test client
client = TestClient(app)


def test_health_check():
    """Test that health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    print("✅ Health check passed!")


def test_create_session():
    """Test creating a new session"""
    response = client.post("/sessions")
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert len(data["session_id"]) > 0
    
    print(f"✅ Created session: {data['session_id']}")
    return data["session_id"]


def test_get_context():
    """Test retrieving context for a session"""
    # First create a session
    create_response = client.post("/sessions")
    session_id = create_response.json()["session_id"]
    
    # Get context
    response = client.get(f"/sessions/{session_id}/context")
    assert response.status_code == 200
    
    data = response.json()
    assert "messages" in data
    assert "emotional_state" in data
    assert data["emotional_state"] == "neutral"
    
    print(f"✅ Got context for session: {session_id}")


def test_get_context_not_found():
    """Test getting context for non-existent session"""
    response = client.get("/sessions/fake-session-id/context")
    assert response.status_code == 200  # Your current code returns 200
    
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"
    
    print("✅ Correctly handles missing session")


def test_save_interaction():
    """Test saving an interaction"""
    # First create a session
    create_response = client.post("/sessions")
    session_id = create_response.json()["session_id"]
    
    # Save interaction
    response = client.post(
        f"/sessions/{session_id}/interactions",
        params={
            "user_message": "Hello, I'm feeling happy!",
            "ai_message": "That's wonderful to hear!"
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "interaction_id" in data
    
    print(f"✅ Saved interaction for session: {session_id}")


def test_full_flow():
    """Test complete flow: create -> save -> retrieve"""
    # 1. Create session
    create_response = client.post("/sessions")
    assert create_response.status_code == 200
    session_id = create_response.json()["session_id"]
    print(f"  1. Created session: {session_id}")
    
    # 2. Save interaction
    save_response = client.post(
        f"/sessions/{session_id}/interactions",
        params={
            "user_message": "I'm working on PACT!",
            "ai_message": "That's exciting! Tell me more."
        }
    )
    assert save_response.status_code == 200
    print(f"  2. Saved interaction")
    
    # 3. Get context
    context_response = client.get(f"/sessions/{session_id}/context")
    assert context_response.status_code == 200
    context = context_response.json()
    print(f"  3. Retrieved context: {context}")
    
    print("✅ Full flow test passed!")


def test_multiple_sessions():
    """Test creating multiple sessions"""
    sessions = []
    
    for i in range(3):
        response = client.post("/sessions")
        assert response.status_code == 200
        session_id = response.json()["session_id"]
        sessions.append(session_id)
        print(f"  Created session {i+1}: {session_id}")
    
    # Verify all sessions are different
    assert len(set(sessions)) == 3
    print("✅ Multiple sessions test passed!")


if __name__ == "__main__":
    """Run tests manually without pytest"""
    print("\n🧪 Running PACT API Tests\n")
    print("=" * 50)
    
    try:
        print("\n1. Testing health check...")
        test_health_check()
        
        print("\n2. Testing session creation...")
        test_create_session()
        
        print("\n3. Testing context retrieval...")
        test_get_context()
        
        print("\n4. Testing missing session...")
        test_get_context_not_found()
        
        print("\n5. Testing save interaction...")
        test_save_interaction()
        
        print("\n6. Testing full flow...")
        test_full_flow()
        
        print("\n7. Testing multiple sessions...")
        test_multiple_sessions()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
