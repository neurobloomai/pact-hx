#!/usr/bin/env python3
"""
Quick Integration Test
Simple test to verify API is working

Run: python quick_test.py
"""

from pact_langchain import PACTMemory

# Your live API
API_URL = "https://pact-hx.onrender.com"

print("\n🧪 Quick PACT Integration Test\n")
print(f"Testing: {API_URL}\n")

try:
    # Create memory
    print("1. Creating PACT Memory...")
    memory = PACTMemory(
        api_key="quick-test",
        api_url=API_URL
    )
    print("   ✅ Created!\n")
    
    # Save interaction
    print("2. Saving conversation...")
    memory.save_context(
        inputs={"input": "Hello PACT!"},
        outputs={"output": "Hello! I'm working!"}
    )
    print("   ✅ Saved!\n")
    
    # Load context
    print("3. Loading context...")
    context = memory.load_memory_variables({})
    print("   ✅ Loaded!\n")
    
    # Show results
    print("📊 Results:")
    print(f"   Emotional state: {context.get('emotional_state', 'unknown')}")
    print(f"   History: {context.get('history', '(empty)')}\n")
    
    print("✅ INTEGRATION WORKING!\n")
    print("🎉 Ready to publish to PyPI!\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()
