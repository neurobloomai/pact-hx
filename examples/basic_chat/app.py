"""
Simple chat agent with PACT-HX emotional memory
Demonstrates attention + memory working together
"""

import asyncio
import httpx
from datetime import datetime

class PACTChatAgent:
    def __init__(self, agent_id: str, pact_api_url: str = "http://localhost:8000"):
        self.agent_id = agent_id
        self.api_url = pact_api_url
    
    async def process_message(self, user_message: str) -> str:
        """Process a user message with PACT primitives"""
        
        # Extract entities (simple keyword extraction for demo)
        entities = [word for word in user_message.lower().split() 
                   if len(word) > 4 and word.isalpha()]
        
        async with httpx.AsyncClient() as client:
            # Update attention
            attention_response = await client.post(
                f"{self.api_url}/attention/update",
                json={
                    "agent_id": self.agent_id,
                    "entities": entities,
                    "context": user_message
                }
            )
            
            attention_data = attention_response.json()
            current_focus = attention_data["current_focus"]
            
            # Store in memory (would implement similar API)
            # memory_response = await client.post(...)
            
            # Generate response based on attention
            if current_focus:
                focus_context = f"I notice you're focusing on: {', '.join(current_focus[:3])}"
                response = f"{focus_context}. How can I help you with that?"
            else:
                response = "I'm here to help. What would you like to discuss?"
            
            return response

async def main():
    agent = PACTChatAgent("demo-agent-001")
    
    print("PACT Chat Agent Demo")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = await agent.process_message(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
