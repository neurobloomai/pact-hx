"""
Emotional Tracking Example
==========================
Demonstrates PACT's emotional awareness in a coaching/therapy context.

Part of PACT by NeurobloomAI
https://github.com/neurobloomai/pact-hx

Run:
    python examples/emotional_tracking_complete.py
"""

import os
from langchain_openai import ChatOpenAI  # Updated import
from langchain.chains import ConversationChain
from pact_langchain import PACTMemory


def display_emotional_panel(state):
    """Display emotional state in a nice format."""
    emotion = state.get('current_emotion', 'neutral')
    valence = state.get('valence', 0.5)
    trend = state.get('trend', 'stable')
    
    # Emotion emoji mapping
    emoji_map = {
        'happy': '😊', 'excited': '🎉', 'calm': '😌', 'neutral': '😐',
        'sad': '😢', 'frustrated': '😤', 'angry': '😠', 'anxious': '😰',
        'stressed': '😓', 'confused': '😕'
    }
    
    emoji = emoji_map.get(emotion, '🙂')
    
    print("\n" + "="*50)
    print(f"{emoji} EMOTIONAL STATE")
    print("="*50)
    print(f"Emotion:  {emotion.capitalize()}")
    print(f"Valence:  {'▓' * int(valence * 10)}{'░' * (10 - int(valence * 10))} {valence:.2f}")
    print(f"Trend:    {trend.capitalize()}")
    print("="*50 + "\n")


def main():
    pact_api_key = os.getenv("PACT_API_KEY")
    if not pact_api_key:
        print("❌ Set PACT_API_KEY environment variable")
        return
    
    print("🧠 PACT Memory - Emotional Coaching Example")
    print("=" * 50)
    print("Commands: 'quit', 'state', 'graph', 'consolidate'\n")
    
    memory = PACTMemory(
        api_key=pact_api_key,
        emotional_tracking=True,
        return_emotional_context=True,
        consolidation_threshold=8
    )
    
    llm = ChatOpenAI(temperature=0.8, model="gpt-3.5-turbo")
    conversation = ConversationChain(llm=llm, memory=memory)
    
    message_count = 0
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("\n👋 Take care!")
                break
            
            if user_input.lower() == "state":
                state = memory.get_emotional_state()
                display_emotional_panel(state)
                continue
            
            if user_input.lower() == "graph":
                graph = memory.get_context_graph()
                print(f"\n📊 Memory Graph: {len(graph.get('nodes', []))} nodes")
                continue
            
            if user_input.lower() == "consolidate":
                result = memory.force_consolidation()
                print(f"\n🔄 Consolidated: {result.get('message', 'Done')}")
                continue
            
            response = conversation.predict(input=user_input)
            print(f"\n🤖 Coach: {response}")
            
            message_count += 1
            
            if message_count % 3 == 0:
                state = memory.get_emotional_state()
                emotion = state.get('current_emotion', 'neutral')
                trend = state.get('trend', 'stable')
                print(f"\n   💭 [Emotion: {emotion}, Trend: {trend}]")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTip: Install dependencies:")
            print("  pip install langchain-openai langchain-community")


if __name__ == "__main__":
    main()
