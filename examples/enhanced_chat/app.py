# examples/enhanced_chat/app.py
"""
Enhanced Chat Agent with PACT-HX Attention + Memory Collaboration
Demonstrates emergent behavior when primitives work together

This example shows:
1. Individual primitive power (each works alone)
2. Collaborative enhancement (better together)
3. Emergent intelligence (behaviors neither could achieve alone)
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class PACTEnhancedAgent:
    """
    Chat agent demonstrating individualistic + collective intelligence
    """
    
    def __init__(self, agent_id: str, pact_api_url: str = "http://localhost:8000"):
        self.agent_id = agent_id
        self.api_url = pact_api_url
        self.conversation_history = []
        
        # Track collaboration effectiveness
        self.collaboration_stats = {
            "attention_only_responses": 0,
            "memory_only_responses": 0,
            "collaborative_responses": 0,
            "emergent_behaviors": 0
        }
    
    async def process_message(self, user_message: str, enable_collaboration: bool = True) -> Dict[str, Any]:
        """
        Process message with individual primitive power + optional collaboration
        """
        
        print(f"\n🔄 Processing: '{user_message}'")
        print(f"Collaboration: {'ON' if enable_collaboration else 'OFF'}")
        
        # Extract entities and topics (simple NLP for demo)
        entities = self._extract_entities(user_message)
        topics = self._extract_topics(user_message)
        
        async with httpx.AsyncClient() as client:
            
            # ========== INDIVIDUAL PRIMITIVE PROCESSING ==========
            
            # 1. Update attention (sovereign operation)
            attention_result = await self._update_attention(client, entities, user_message)
            print(f"📍 Attention Focus: {attention_result.get('current_focus', [])}")
            
            # 2. Store memory (sovereign operation)  
            memory_entry = await self._store_memory(
                client, user_message, entities, topics, 
                attention_context=attention_result if enable_collaboration else None
            )
            print(f"🧠 Memory Stored: {memory_entry.get('memory_id', 'N/A')}")
            
            # ========== COLLABORATIVE INTELLIGENCE ==========
            
            if enable_collaboration:
                # 3. Retrieve relevant memories using attention context
                relevant_memories = await self._retrieve_contextual_memories(
                    client, user_message, attention_result
                )
                print(f"💭 Relevant Memories: {len(relevant_memories)}")
                
                # 4. Generate response with emergent behavior
                response_data = await self._generate_collaborative_response(
                    user_message, attention_result, relevant_memories
                )
                self.collaboration_stats["collaborative_responses"] += 1
                
                # Check for emergent behaviors
                if self._detect_emergent_behavior(response_data):
                    self.collaboration_stats["emergent_behaviors"] += 1
                    print("✨ Emergent behavior detected!")
                
            else:
                # Generate response with individual primitives only
                response_data = await self._generate_individual_response(
                    user_message, attention_result
                )
                self.collaboration_stats["attention_only_responses"] += 1
        
        # Record conversation
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user_message": user_message,
            "response": response_data["response"],
            "collaboration_enabled": enable_collaboration,
            "attention_focus": attention_result.get("current_focus", []),
            "memory_references": len(relevant_memories) if enable_collaboration else 0
        })
        
        return response_data
    
    async def _update_attention(self, client: httpx.AsyncClient, entities: List[str], context: str) -> Dict[str, Any]:
        """Update attention - sovereign primitive operation"""
        
        try:
            response = await client.post(
                f"{self.api_url}/attention/update",
                json={
                    "agent_id": self.agent_id,
                    "entities": entities,
                    "context": context
                }
            )
            return response.json()
        except Exception as e:
            print(f"⚠️ Attention update failed: {e}")
            return {"current_focus": [], "salience_weights": {}}
    
    async def _store_memory(
        self, 
        client: httpx.AsyncClient, 
        content: str, 
        entities: List[str], 
        topics: List[str],
        attention_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Store memory - sovereign primitive with optional collaboration"""
        
        memory_request = {
            "agent_id": self.agent_id,
            "content": content,
            "entities": entities,
            "topics": topics,
            "emotional_valence": self._detect_emotional_valence(content)
        }
        
        # Optional collaboration enhancement
        if attention_context:
            memory_request["attention_context"] = attention_context
        
        try:
            response = await client.post(
                f"{self.api_url}/memory/store",
                json=memory_request
            )
            return response.json()
        except Exception as e:
            print(f"⚠️ Memory storage failed: {e}")
            return {"memory_id": None}
    
    async def _retrieve_contextual_memories(
        self, 
        client: httpx.AsyncClient, 
        query: str, 
        attention_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Retrieve memories enhanced by attention context - collaborative intelligence"""
        
        # Enhance query with attention focus
        enhanced_query = query
        if attention_context.get("current_focus"):
            focus_terms = " ".join(attention_context["current_focus"][:3])
            enhanced_query = f"{query} {focus_terms}"
        
        try:
            response = await client.post(
                f"{self.api_url}/memory/retrieve",
                json={
                    "agent_id": self.agent_id,
                    "query": enhanced_query,
                    "limit": 5,
                    "min_confidence": 0.3
                }
            )
            return response.json()
        except Exception as e:
            print(f"⚠️ Memory retrieval failed: {e}")
            return []
    
    async def _generate_collaborative_response(
        self, 
        user_message: str, 
        attention_result: Dict[str, Any], 
        relevant_memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate response using collaborative intelligence - emergent behavior"""
        
        current_focus = attention_result.get("current_focus", [])
        salience_weights = attention_result.get("salience_weights", {})
        
        # Emergent behavior: Contextual topic switching
        if len(relevant_memories) > 2 and current_focus:
            # Check if we should suggest a topic shift based on memory patterns
            memory_topics = []
            for memory in relevant_memories:
                memory_topics.extend(memory.get("topics", []))
            
            # If memories suggest a different focus than current attention
            if memory_topics and not any(topic in current_focus for topic in memory_topics[:3]):
                response_type = "topic_shift_suggestion"
                response = self._generate_topic_shift_response(user_message, current_focus, memory_topics[:3])
            else:
                response_type = "contextual_enhancement"
                response = self._generate_contextual_response(user_message, current_focus, relevant_memories)
        
        # Emergent behavior: Emotional continuity
        elif relevant_memories:
            emotional_pattern = self._analyze_emotional_pattern(relevant_memories)
            if emotional_pattern["has_pattern"]:
                response_type = "emotional_continuity"
                response = self._generate_emotional_response(user_message, emotional_pattern)
            else:
                response_type = "memory_informed"
                response = self._generate_memory_informed_response(user_message, relevant_memories)
        
        # Fallback to attention-guided response
        else:
            response_type = "attention_guided"
            response = self._generate_attention_response(user_message, current_focus)
        
        return {
            "response": response,
            "response_type": response_type,
            "collaboration_factors": {
                "attention_influence": len(current_focus),
                "memory_influence": len(relevant_memories),
                "salience_scores": salience_weights
            },
            "emergent_behavior": response_type in ["topic_shift_suggestion", "emotional_continuity"]
        }
    
    async def _generate_individual_response(
        self, 
        user_message: str, 
        attention_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response using only individual primitive power"""
        
        current_focus = attention_result.get("current_focus", [])
        
        if current_focus:
            response = f"I notice you're focusing on: {', '.join(current_focus[:3])}. How can I help you with that?"
            response_type = "attention_only"
        else:
            response = "I'm here to help. What would you like to discuss?"
            response_type = "basic"
        
        return {
            "response": response,
            "response_type": response_type,
            "collaboration_factors": {
                "attention_influence": len(current_focus),
                "memory_influence": 0
            },
            "emergent_behavior": False
        }
    
    def _generate_topic_shift_response(self, user_message: str, current_focus: List[str], suggested_topics: List[str]) -> str:
        """Emergent behavior: Intelligent topic shifting"""
        return f"Based on our previous conversations about {', '.join(suggested_topics[:2])}, I think you might also be interested in exploring how this relates to {current_focus[0] if current_focus else 'your current question'}. Would you like me to make those connections?"
    
    def _generate_contextual_response(self, user_message: str, focus: List[str], memories: List[Dict[str, Any]]) -> str:
        """Enhanced response using attention + memory context"""
        recent_topics = []
        for memory in memories[:3]:
            recent_topics.extend(memory.get("topics", []))
        
        if recent_topics and focus:
            return f"Considering our recent discussions about {', '.join(set(recent_topics[:3]))} and your current focus on {', '.join(focus[:2])}, here's what I think..."
        elif recent_topics:
            return f"Based on our previous conversations about {', '.join(set(recent_topics[:3]))}, I can help you with that."
        else:
            return "I remember our previous discussions, and I think I can help you with this."
    
    def _generate_emotional_response(self, user_message: str, emotional_pattern: Dict[str, Any]) -> str:
        """Emergent behavior: Emotional continuity"""
        trend = emotional_pattern["trend"]
        if trend == "positive":
            return "I've noticed you've been in good spirits in our recent conversations. I'm glad to continue helping you in a positive way!"
        elif trend == "negative":
            return "I sense this might be challenging for you, based on our recent conversations. I'm here to support you through this."
        else:
            return "I appreciate the trust you've shown in our conversations. How can I best help you today?"
    
    def _generate_memory_informed_response(self, user_message: str, memories: List[Dict[str, Any]]) -> str:
        """Response informed by memory but without emergent patterns"""
        return f"I recall we've discussed similar topics before. Let me help you build on what we've previously covered."
    
    def _generate_attention_response(self, user_message: str, focus: List[str]) -> str:
        """Response based purely on attention"""
        if focus:
            return f"I see you're currently focused on {', '.join(focus[:3])}. Let me address that specifically."
        else:
            return "What would you like to focus on today?"
    
    def _analyze_emotional_pattern(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze emotional patterns in memories"""
        if len(memories) < 3:
            return {"has_pattern": False}
        
        emotional_values = [m.get("emotional_valence", "neutral") for m in memories[-3:]]
        
        if emotional_values.count("positive") >= 2:
            return {"has_pattern": True, "trend": "positive"}
        elif emotional_values.count("negative") >= 2:
            return {"has_pattern": True, "trend": "negative"}
        else:
            return {"has_pattern": True, "trend": "mixed"}
    
    def _detect_emergent_behavior(self, response_data: Dict[str, Any]) -> bool:
        """Detect if response shows emergent behavior"""
        return response_data.get("emergent_behavior", False)
    
    def _extract_entities(self, text: str) -> List[str]:
        """Simple entity extraction for demo"""
        # Look for capitalized words and common entities
        words = text.split()
        entities = []
        
        for word in words:
            if word[0].isupper() and len(word) > 2:
                entities.append(word.lower())
        
        # Add some domain-specific entities
        domain_entities = ["python", "programming", "AI", "machine learning", "data", "code"]
        for entity in domain_entities:
            if entity.lower() in text.lower():
                entities.append(entity.lower())
        
        return list(set(entities))[:5]  # Limit to 5 entities
    
    def _extract_topics(self, text: str) -> List[str]:
        """Simple topic extraction for demo"""
        topic_keywords = {
            "technology": ["tech", "programming", "code", "software", "AI", "computer"],
            "learning": ["learn", "study", "education", "tutorial", "course"],
            "work": ["job", "work", "career", "professional", "business"],
            "personal": ["personal", "life", "family", "friends", "relationship"],
            "health": ["health", "exercise", "fitness", "wellness", "medical"]
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword.lower() in text.lower() for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _detect_emotional_valence(self, text: str) -> str:
        """Simple emotional valence detection"""
        positive_words = ["good", "great", "excellent", "happy", "love", "amazing", "wonderful"]
        negative_words = ["bad", "terrible", "hate", "sad", "angry", "frustrated", "awful"]
        
        positive_count = sum(1 for word in positive_words if word in text.lower())
        negative_count = sum(1 for word in negative_words if word in text.lower())
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    async def get_agent_analytics(self) -> Dict[str, Any]:
        """Get analytics about agent performance and collaboration"""
        
        async with httpx.AsyncClient() as client:
            try:
                # Get memory analytics
                memory_response = await client.get(f"{self.api_url}/memory/{self.agent_id}/analytics")
                memory_analytics = memory_response.json()
                
                # Get attention state
                attention_response = await client.get(f"{self.api_url}/attention/{self.agent_id}")
                attention_state = attention_response.json()
                
                return {
                    "agent_id": self.agent_id,
                    "conversation_count": len(self.conversation_history),
                    "collaboration_stats": self.collaboration_stats,
                    "memory_analytics": memory_analytics.get("analytics", {}),
                    "current_attention": attention_state,
                    "recent_conversations": self.conversation_history[-5:] if self.conversation_history else []
                }
            except Exception as e:
                print(f"⚠️ Analytics retrieval failed: {e}")
                return {"error": str(e)}

# ========== DEMO APPLICATION ==========

async def run_demo():
    """
    Interactive demo showing individual vs collaborative intelligence
    """
    
    print("🚀 PACT Enhanced Chat Agent Demo")
    print("=" * 50)
    print("This demo shows:")
    print("1. Individual primitive power (attention + memory work alone)")
    print("2. Collaborative enhancement (better together)")
    print("3. Emergent behaviors (impossible alone)")
    print("\nCommands:")
    print("- 'solo' - Disable collaboration")
    print("- 'collab' - Enable collaboration")
    print("- 'analytics' - Show agent analytics")
    print("- 'quit' - Exit")
    print("=" * 50)
    
    agent = PACTEnhancedAgent("enhanced-demo-agent")
    collaboration_enabled = True
    
    while True:
        user_input = input(f"\n[{'COLLAB' if collaboration_enabled else 'SOLO'}] You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'solo':
            collaboration_enabled = False
            print("🔄 Collaboration disabled - using individual primitives only")
            continue
        elif user_input.lower() == 'collab':
            collaboration_enabled = True
            print("🔄 Collaboration enabled - using collective intelligence")
            continue
        elif user_input.lower() == 'analytics':
            analytics = await agent.get_agent_analytics()
            print("\n📊 Agent Analytics:")
            print(json.dumps(analytics, indent=2, default=str))
            continue
        elif not user_input:
            continue
        
        # Process message
        response_data = await agent.process_message(user_input, collaboration_enabled)
        
        # Display response
        print(f"\nAgent: {response_data['response']}")
        
        # Show collaboration details
        if collaboration_enabled:
            factors = response_data.get("collaboration_factors", {})
            print(f"🔍 Response Type: {response_data.get('response_type', 'unknown')}")
            print(f"🎯 Attention Influence: {factors.get('attention_influence', 0)}")
            print(f"🧠 Memory Influence: {factors.get('memory_influence', 0)}")
            if response_data.get("emergent_behavior"):
                print("✨ Emergent behavior detected!")

if __name__ == "__main__":
    asyncio.run(run_demo())
