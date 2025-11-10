"""
Customer Support Bot Example
============================
Demonstrates PACT Memory in a customer support context.

Part of PACT by NeurobloomAI
https://github.com/neurobloomai/pact-hx

Features shown:
- Emotional escalation detection
- Context prioritization
- Summary generation for human handoff
- Token-efficient long conversations

Run:
    python examples/support_agent.py
"""

import os
from langchain_openai import ChatOpenAI  # Updated import
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from pact_langchain import PACTMemory


SUPPORT_PROMPT = PromptTemplate(
    input_variables=["history", "input", "emotional_state"],
    template="""You are a helpful customer support agent.

Conversation history:
{history}

Current customer emotion: {emotional_state}

Guidelines:
- Be professional and helpful
- If customer is frustrated/angry, prioritize resolution
- Acknowledge their emotions
- Provide clear, actionable solutions

Customer: {input}
Agent:"""
)


def check_escalation(state):
    """Check if conversation should be escalated to human."""
    emotion = state.get('current_emotion', 'neutral')
    valence = state.get('valence', 0.5)
    
    # Escalate if very negative emotion
    if emotion in ['angry', 'frustrated'] and valence < 0.3:
        return True
    return False


def main():
    pact_api_key = os.getenv("PACT_API_KEY")
    if not pact_api_key:
        print("❌ Set PACT_API_KEY")
        return
    
    print("🎧 Customer Support Bot with PACT Memory")
    print("=" * 50)
    
    memory = PACTMemory(
        api_key=pact_api_key,
        emotional_tracking=True,
        return_emotional_context=True,
        context_consolidation=True,
        consolidation_threshold=15
    )
    
    llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=SUPPORT_PROMPT
    )
    
    message_count = 0
    
    while True:
        try:
            user_input = input("\n👤 Customer: ").strip()
            
            if not user_input or user_input.lower() == "quit":
                break
            
            # Get response
            response = conversation.predict(input=user_input)
            print(f"\n🎧 Agent: {response}")
            
            message_count += 1
            
            # Check for escalation
            state = memory.get_emotional_state()
            if check_escalation(state):
                print("\n⚠️  ESCALATION ALERT: Customer is very upset")
                print("Generating handoff summary...")
                
                # Get context for human agent
                context = memory.load_memory_variables({})
                summary = context.get('context_summary', '')
                
                print(f"\n📋 Handoff Summary:\n{summary}")
                print(f"\n🎯 Emotional State: {state.get('current_emotion')}")
                print("\n→ Transferring to human agent...")
                break
            
            # Show emotional indicator
            if message_count % 3 == 0:
                emotion = state.get('current_emotion', 'neutral')
                print(f"\n   💭 [Customer emotion: {emotion}]")
        
        except KeyboardInterrupt:
            print("\n\nSession ended")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTip: Install dependencies:")
            print("  pip install langchain-openai langchain-community")


if __name__ == "__main__":
    main()
