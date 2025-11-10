"""
Basic PACT Memory Example
========================
Simple chatbot showing drop-in replacement for ConversationBufferMemory.

Part of PACT by NeurobloomAI
https://github.com/neurobloomai/pact-hx

Run:
    python examples/basic_usage.py

Set your API keys:
    export OPENAI_API_KEY="sk-..."
    export PACT_API_KEY="sk_test_..."
"""

import os
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from pact_langchain import PACTMemory


def main():
    # Setup
    pact_api_key = os.getenv("PACT_API_KEY")
    if not pact_api_key:
        print("❌ Error: Set PACT_API_KEY environment variable")
        print("   Get your key at: https://neurobloom.ai")
        return
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ Error: Set OPENAI_API_KEY environment variable")
        return
    
    print("🧠 PACT Memory - Basic Example")
    print("=" * 50)
    print("Type 'quit' to exit, 'state' to see emotional state\n")
    
    # Initialize PACT memory
    memory = PACTMemory(
        api_key=pact_api_key,
        emotional_tracking=True,
        return_emotional_context=True
    )
    
    # Create LangChain conversation
    llm = OpenAI(temperature=0.7)
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False  # Set to True to see LangChain internals
    )
    
    # Chat loop
    message_count = 0
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == "state":
                # Show emotional state
                state = memory.get_emotional_state()
                print(f"\n📊 Emotional State:")
                print(f"   Current: {state.get('current_emotion', 'neutral')}")
                print(f"   Valence: {state.get('valence', 0.5):.2f}")
                print(f"   Trend: {state.get('trend', 'stable')}")
                continue
            
            # Get response
            response = conversation.predict(input=user_input)
            print(f"\n🤖 Bot: {response}")
            
            message_count += 1
            
            # Show emotional indicator every few messages
            if message_count % 3 == 0:
                state = memory.get_emotional_state()
                emotion = state.get('current_emotion', 'neutral')
                print(f"\n   [Detected emotion: {emotion}]")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
