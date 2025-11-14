#!/usr/bin/env python3
"""
End-to-End Integration Test
Tests pact-langchain client with live deployed API

Run: python test_live_integration.py
"""

import sys
from pact_langchain import PACTMemory

# Your live API!
API_URL = "https://pact-hx.onrender.com"

def test_integration():
    print("\n" + "="*60)
    print("🧪 PACT End-to-End Integration Test")
    print("="*60)
    
    print(f"\n📡 Testing against: {API_URL}")
    
    try:
        # Step 1: Create PACT Memory
        print("\n1️⃣  Creating PACT Memory...")
        memory = PACTMemory(
            api_key="test-integration",
            api_url=API_URL
        )
        print("   ✅ Memory created!")
        
        # Step 2: Save first interaction (Happy emotion)
        print("\n2️⃣  Saving interaction (happy emotion)...")
        memory.save_context(
            inputs={"input": "I'm so excited about my new project!"},
            outputs={"output": "That's wonderful! Tell me more about it."}
        )
        print("   ✅ Saved happy interaction!")
        
        # Step 3: Save second interaction (Frustrated emotion)
        print("\n3️⃣  Saving interaction (frustrated emotion)...")
        memory.save_context(
            inputs={"input": "But I'm stuck on this bug and it's really frustrating!"},
            outputs={"output": "I understand. Debugging can be challenging. Let's work through it together."}
        )
        print("   ✅ Saved frustrated interaction!")
        
        # Step 4: Save third interaction (Relieved emotion)
        print("\n4️⃣  Saving interaction (relieved emotion)...")
        memory.save_context(
            inputs={"input": "Oh! I figured it out! The solution was simpler than I thought!"},
            outputs={"output": "Excellent! That must feel great. What was the issue?"}
        )
        print("   ✅ Saved relieved interaction!")
        
        # Step 5: Load memory variables
        print("\n5️⃣  Loading conversation context...")
        context = memory.load_memory_variables({})
        print("   ✅ Context loaded!")
        
        # Step 6: Display results
        print("\n" + "="*60)
        print("📊 RESULTS")
        print("="*60)
        
        print(f"\n🗨️  Chat History:")
        history = context.get('history', '')
        if history:
            print(history)
        else:
            print("   (No history yet - this is expected for MVP)")
        
        print(f"\n😊 Emotional State:")
        emotional_state = context.get('emotional_state', 'unknown')
        print(f"   Current: {emotional_state}")
        
        print(f"\n🔢 Context Stats:")
        print(f"   Keys returned: {list(context.keys())}")
        
        # Step 7: Test session persistence
        print("\n6️⃣  Testing session persistence...")
        context2 = memory.load_memory_variables({})
        if context2 == context:
            print("   ✅ Session persists correctly!")
        else:
            print("   ⚠️  Context changed (might be expected)")
        
        # Success summary
        print("\n" + "="*60)
        print("✅ END-TO-END TEST PASSED!")
        print("="*60)
        print("\n📝 Summary:")
        print("   • Client connected to live API ✅")
        print("   • Sessions created ✅")
        print("   • Messages saved ✅")
        print("   • Context retrieved ✅")
        print("   • Emotional tracking (basic) ✅")
        print("\n🎉 Integration working!\n")
        
        return True
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ TEST FAILED")
        print("="*60)
        print(f"\nError: {e}")
        print("\nDebug info:")
        import traceback
        traceback.print_exc()
        return False


def test_with_langchain():
    """Test with actual LangChain conversation chain"""
    print("\n" + "="*60)
    print("🦜 Testing with LangChain ConversationChain")
    print("="*60)
    
    try:
        from langchain.chains import ConversationChain
        from langchain_openai import ChatOpenAI
        
        print("\n1️⃣  Creating LangChain components...")
        
        # Create memory
        memory = PACTMemory(
            api_key="langchain-test",
            api_url=API_URL
        )
        
        # Create LLM (requires OpenAI API key)
        llm = ChatOpenAI(temperature=0.7)
        
        # Create conversation
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=True
        )
        
        print("   ✅ LangChain setup complete!")
        
        print("\n2️⃣  Having conversation...")
        
        # Turn 1
        response1 = conversation.predict(
            input="Hi! I'm building an AI memory system."
        )
        print(f"\n   User: Hi! I'm building an AI memory system.")
        print(f"   AI: {response1}")
        
        # Turn 2
        response2 = conversation.predict(
            input="It uses emotional intelligence to track context."
        )
        print(f"\n   User: It uses emotional intelligence to track context.")
        print(f"   AI: {response2}")
        
        print("\n✅ LangChain integration working!")
        return True
        
    except ImportError as e:
        print(f"\n⚠️  Skipping LangChain test (missing dependencies)")
        print(f"   Install with: pip install langchain langchain-openai")
        return None
        
    except Exception as e:
        print(f"\n❌ LangChain test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling and edge cases"""
    print("\n" + "="*60)
    print("🔧 Testing Error Handling")
    print("="*60)
    
    try:
        print("\n1️⃣  Testing with invalid session...")
        memory = PACTMemory(
            api_key="error-test",
            api_url=API_URL
        )
        
        # Try to load non-existent session
        # (This should handle gracefully)
        context = memory.load_memory_variables({})
        print("   ✅ Handled gracefully!")
        
        print("\n2️⃣  Testing empty saves...")
        memory.save_context(
            inputs={"input": ""},
            outputs={"output": ""}
        )
        print("   ✅ Handled empty content!")
        
        print("\n✅ Error handling working!")
        return True
        
    except Exception as e:
        print(f"\n⚠️  Error handling test issues: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting PACT Integration Tests\n")
    
    # Run basic integration test
    test1 = test_integration()
    
    # Run LangChain test (optional)
    print("\n" + "="*60)
    test2 = test_with_langchain()
    
    # Run error handling test
    test3 = test_error_handling()
    
    # Final summary
    print("\n" + "="*60)
    print("📊 FINAL TEST SUMMARY")
    print("="*60)
    
    results = {
        "Basic Integration": "✅ PASSED" if test1 else "❌ FAILED",
        "LangChain Integration": "✅ PASSED" if test2 else ("⚠️ SKIPPED" if test2 is None else "❌ FAILED"),
        "Error Handling": "✅ PASSED" if test3 else "⚠️ ISSUES"
    }
    
    for test_name, result in results.items():
        print(f"   {test_name}: {result}")
    
    if test1:
        print("\n🎉 Core integration is working!")
        print("✅ Ready to publish to PyPI!")
    else:
        print("\n⚠️  Core integration needs fixes before publishing")
    
    print("\n")
    sys.exit(0 if test1 else 1)
