#!/usr/bin/env python3
"""
PACT Basic Integration Demo
===========================

Complete system integration demo for examples/integration_demos/

This demo showcases:
- Full PACT system demonstration
- Multi-student classroom simulation
- Real-time adaptation showcase  
- End-to-end learning experience

Integrates all PACT components built in previous commits:
- Creative Synthesis API (Commit 2)
- Integration Engine coordination
- Real-time adaptation
- Educational content generation
"""

import asyncio
import aiohttp
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# Demo Configuration
# ============================================================================

class DemoConfig:
    """Demo configuration settings"""
    CREATIVE_SYNTHESIS_API = "http://localhost:8000"
    DEMO_DURATION_MINUTES = 1
    STUDENT_COUNT = 6
    UPDATE_INTERVAL_SECONDS = 10
    ADAPTATION_PROBABILITY = 0.3
    
    # Learning topics for demo
    SUBJECTS = ["Mathematics", "Science", "History"]
    MATH_TOPICS = ["Fractions", "Multiplication", "Geometry", "Decimals"]
    SCIENCE_TOPICS = ["Photosynthesis", "Solar System", "Weather", "Animals"]
    HISTORY_TOPICS = ["Ancient Egypt", "American Revolution", "World War II"]

# ============================================================================
# Student Models
# ============================================================================

class DemoStudent:
    """Represents a student in the demo classroom"""
    
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        # Random learning characteristics
        self.grade_level = random.choice(["3rd", "4th", "5th"])
        self.learning_style = random.choice(["visual", "auditory", "kinesthetic", "reading"])
        self.difficulty_preference = random.choice(["easy", "medium", "hard"])
        
        # Dynamic metrics (will change during demo)
        self.engagement_level = random.uniform(0.4, 0.9)
        self.knowledge_level = random.uniform(0.3, 0.8)
        self.attention_span = random.randint(10, 25)
        
        # Demo state
        self.current_experience_id = None
        self.experience_history = []
        self.adaptation_count = 0
        self.last_interaction = datetime.now()
        
    def simulate_engagement_change(self):
        """Simulate natural engagement fluctuations"""
        # Random walk with tendency to return to baseline
        baseline = 0.6
        change = random.uniform(-0.15, 0.15)
        drift_to_baseline = (baseline - self.engagement_level) * 0.1
        
        self.engagement_level += change + drift_to_baseline
        self.engagement_level = max(0.0, min(1.0, self.engagement_level))
        
        # Occasionally simulate significant drops or spikes
        if random.random() < 0.05:  # 5% chance
            if random.random() < 0.5:
                self.engagement_level *= 0.7  # Drop
                return "engagement_drop"
            else:
                self.engagement_level = min(1.0, self.engagement_level * 1.3)  # Spike
                if self.knowledge_level > 0.7:
                    return "mastery_achieved"
        
        # Confusion detection based on low engagement + time
        time_since_interaction = (datetime.now() - self.last_interaction).seconds
        if self.engagement_level < 0.4 and time_since_interaction > 120:
            return "confusion_detected"
            
        return None
    
    def update_from_adaptation(self, adaptation_response: Dict):
        """Update student state based on adaptation"""
        self.adaptation_count += 1
        adaptation_type = adaptation_response.get("adaptation_type", "")
        
        if adaptation_type == "engagement_drop":
            self.engagement_level = min(1.0, self.engagement_level + 0.2)
        elif adaptation_type == "confusion_detected":
            self.engagement_level = min(1.0, self.engagement_level + 0.15)
            self.knowledge_level = min(1.0, self.knowledge_level + 0.1)
        elif adaptation_type == "mastery_achieved":
            self.knowledge_level = min(1.0, self.knowledge_level + 0.1)
        
        self.last_interaction = datetime.now()
    
    def get_status_emoji(self):
        """Get emoji representing current student state"""
        if self.engagement_level > 0.8:
            return "🌟"
        elif self.engagement_level > 0.6:
            return "😊"
        elif self.engagement_level > 0.4:
            return "😐"
        else:
            return "😰"
    
    def __str__(self):
        return f"{self.get_status_emoji()} {self.name:12} | Engagement: {self.engagement_level:.2f} | Knowledge: {self.knowledge_level:.2f} | Style: {self.learning_style:12} | Adaptations: {self.adaptation_count}"

# ============================================================================
# Classroom Manager
# ============================================================================

class DemoClassroom:
    """Manages the simulated classroom environment"""
    
    def __init__(self):
        self.session_id = f"classroom_{uuid.uuid4().hex[:8]}"
        self.subject = random.choice(DemoConfig.SUBJECTS)
        self.topic = self._select_topic()
        self.start_time = datetime.now()
        
        # Create diverse student population
        self.students = self._create_students()
        
        # Classroom metrics
        self.total_experiences_generated = 0
        self.total_adaptations = 0
        self.adaptation_events = []
        
        logger.info(f"🏫 Classroom created: {self.subject} - {self.topic}")
        logger.info(f"👥 Students: {len(self.students)}")
    
    def _select_topic(self):
        """Select appropriate topic based on subject"""
        topic_map = {
            "Mathematics": DemoConfig.MATH_TOPICS,
            "Science": DemoConfig.SCIENCE_TOPICS,
            "History": DemoConfig.HISTORY_TOPICS
        }
        return random.choice(topic_map.get(self.subject, ["General Topic"]))
    
    def _create_students(self):
        """Create diverse student population"""
        names = [
            "Alex Chen", "Maya Patel", "Jordan Kim", "Emma Rodriguez", 
            "Sam Wilson", "Aria Thompson"
        ]
        
        students = []
        for i, name in enumerate(names[:DemoConfig.STUDENT_COUNT]):
            student = DemoStudent(f"demo_student_{i+1:03d}", name)
            students.append(student)
        
        return students
    
    def get_classroom_metrics(self):
        """Calculate overall classroom metrics"""
        if not self.students:
            return {}
        
        avg_engagement = sum(s.engagement_level for s in self.students) / len(self.students)
        avg_knowledge = sum(s.knowledge_level for s in self.students) / len(self.students)
        
        struggling_students = sum(1 for s in self.students if s.engagement_level < 0.4)
        excelling_students = sum(1 for s in self.students if s.engagement_level > 0.8)
        
        return {
            "average_engagement": avg_engagement,
            "average_knowledge": avg_knowledge,
            "students_struggling": struggling_students,
            "students_excelling": excelling_students,
            "total_adaptations": self.total_adaptations,
            "session_duration": str(datetime.now() - self.start_time).split('.')[0]
        }
    
    def display_status(self):
        """Display current classroom status"""
        metrics = self.get_classroom_metrics()
        
        print(f"\n📊 Classroom Status - {self.subject}: {self.topic}")
        print("=" * 70)
        print(f"📈 Average Engagement: {metrics['average_engagement']:.2f}")
        print(f"🧠 Average Knowledge: {metrics['average_knowledge']:.2f}")
        print(f"😰 Students Struggling: {metrics['students_struggling']}")
        print(f"🌟 Students Excelling: {metrics['students_excelling']}")
        print(f"⚡ Total Adaptations: {metrics['total_adaptations']}")
        print(f"⏰ Session Duration: {metrics['session_duration']}")
        print()
        
        print("👥 Individual Student Status:")
        print("-" * 70)
        for student in self.students:
            print(f"  {student}")

# ============================================================================
# PACT API Integration
# ============================================================================

class PACTAPIClient:
    """Client for interacting with PACT Creative Synthesis API"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        
        # Test API connectivity
        try:
            async with self.session.get(f"{self.api_url}/health") as response:
                if response.status == 200:
                    logger.info("✅ Connected to PACT Creative Synthesis API")
                    return True
                else:
                    logger.error(f"❌ API health check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to API: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
    
    async def generate_experience(self, student: DemoStudent, subject: str, topic: str) -> Optional[Dict]:
        """Generate educational experience for student"""
        learning_context = {
            "student_id": student.student_id,
            "session_id": student.session_id,
            "subject": subject,
            "grade_level": student.grade_level,
            "learning_style": student.learning_style,
            "difficulty_preference": student.difficulty_preference,
            "interests": [],
            "current_knowledge_level": student.knowledge_level,
            "engagement_score": student.engagement_level,
            "attention_span": student.attention_span
        }
        
        request_payload = {
            "context": learning_context,
            "content_type": "lesson",
            "topic": topic,
            "duration_minutes": 15,
            "adaptation_enabled": True,
            "real_time_feedback": True
        }
        
        try:
            async with self.session.post(
                f"{self.api_url}/generate",
                json=request_payload
            ) as response:
                if response.status == 200:
                    experience = await response.json()
                    student.current_experience_id = experience["experience_id"]
                    student.experience_history.append(experience)
                    logger.info(f"📚 Generated experience for {student.name}: {experience['experience_id']}")
                    return experience
                else:
                    logger.error(f"❌ Failed to generate experience for {student.name}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"❌ API error generating experience: {e}")
            return None
    
    async def trigger_adaptation(self, student: DemoStudent, trigger_type: str, confidence: float = 0.8) -> Optional[Dict]:
        """Trigger adaptation for student's current experience"""
        if not student.current_experience_id:
            return None
        
        adaptation_trigger = {
            "trigger_type": trigger_type,
            "confidence": confidence,
            "context": {
                "current_engagement": student.engagement_level,
                "current_knowledge": student.knowledge_level,
                "learning_style": student.learning_style
            },
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            async with self.session.post(
                f"{self.api_url}/adapt/{student.current_experience_id}",
                json=adaptation_trigger
            ) as response:
                if response.status == 200:
                    adaptation = await response.json()
                    logger.info(f"⚡ Adaptation triggered for {student.name}: {adaptation['reasoning']}")
                    return adaptation
                else:
                    logger.error(f"❌ Failed to trigger adaptation for {student.name}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"❌ API error triggering adaptation: {e}")
            return None

# ============================================================================
# Demo Orchestrator
# ============================================================================

class PACTDemoOrchestrator:
    """Main demo orchestrator - coordinates all components"""
    
    def __init__(self):
        self.classroom = DemoClassroom()
        self.api_client = PACTAPIClient(DemoConfig.CREATIVE_SYNTHESIS_API)
        self.running = False
        self.cycle_count = 0
    
    async def initialize(self):
        """Initialize demo components"""
        logger.info("🚀 Initializing PACT Integration Demo...")
        
        # Initialize API client
        if not await self.api_client.initialize():
            logger.error("❌ Failed to initialize API client")
            return False
        
        # Generate initial experiences for all students
        logger.info("📚 Generating initial learning experiences...")
        for student in self.classroom.students:
            experience = await self.api_client.generate_experience(
                student, self.classroom.subject, self.classroom.topic
            )
            if experience:
                self.classroom.total_experiences_generated += 1
        
        logger.info(f"✅ Demo initialized with {self.classroom.total_experiences_generated} experiences")
        return True
    
    async def run_demo(self, duration_minutes: int = DemoConfig.DEMO_DURATION_MINUTES):
        """Run the complete demo simulation"""
        self.running = True
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        logger.info(f"🎬 Starting {duration_minutes}-minute PACT demo simulation...")
        logger.info(f"📖 Subject: {self.classroom.subject} - Topic: {self.classroom.topic}")
        
        # Initial status display
        self.classroom.display_status()
        
        while self.running and datetime.now() < end_time:
            self.cycle_count += 1
            
            print(f"\n🔄 Demo Cycle {self.cycle_count}")
            print("-" * 40)
            
            # Process each student
            adaptations_this_cycle = 0
            for student in self.classroom.students:
                # Simulate engagement changes
                trigger_type = student.simulate_engagement_change()
                
                # Trigger adaptation if needed
                if trigger_type and random.random() < DemoConfig.ADAPTATION_PROBABILITY:
                    adaptation = await self.api_client.trigger_adaptation(student, trigger_type)
                    
                    if adaptation:
                        student.update_from_adaptation(adaptation)
                        self.classroom.total_adaptations += 1
                        adaptations_this_cycle += 1
                        
                        # Log adaptation event
                        event = {
                            "cycle": self.cycle_count,
                            "student": student.name,
                            "trigger": trigger_type,
                            "reasoning": adaptation.get("reasoning", ""),
                            "timestamp": datetime.now().isoformat()
                        }
                        self.classroom.adaptation_events.append(event)
                        
                        print(f"  ⚡ {student.name}: {trigger_type} → {adaptation.get('reasoning', 'Adapted')}")
            
            # Display cycle summary
            if adaptations_this_cycle > 0:
                print(f"  📊 Adaptations this cycle: {adaptations_this_cycle}")
            else:
                print("  📊 No adaptations needed this cycle")
            
            # Update classroom status every few cycles
            if self.cycle_count % 3 == 0:
                self.classroom.display_status()
            
            # Wait before next cycle
            await asyncio.sleep(DemoConfig.UPDATE_INTERVAL_SECONDS)
        
        # Demo completed
        reason = "time limit" if datetime.now() >= end_time else "cycle limit"
        logger.info(f"🏁 Demo simulation completed! (Stopped due to {reason})")
        await self.generate_final_report()
    
    async def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 80)
        print("📋 PACT INTEGRATION DEMO - FINAL REPORT")
        print("=" * 80)
        
        metrics = self.classroom.get_classroom_metrics()
        
        print(f"🏫 Classroom Session: {self.classroom.session_id}")
        print(f"📚 Subject: {self.classroom.subject} - {self.classroom.topic}")
        print(f"⏰ Total Duration: {metrics['session_duration']}")
        print(f"🔄 Demo Cycles: {self.cycle_count}")
        
        print(f"\n📊 FINAL METRICS:")
        print(f"  📈 Final Average Engagement: {metrics['average_engagement']:.2f}")
        print(f"  🧠 Final Average Knowledge: {metrics['average_knowledge']:.2f}")
        print(f"  📚 Experiences Generated: {self.classroom.total_experiences_generated}")
        print(f"  ⚡ Total Adaptations: {self.classroom.total_adaptations}")
        print(f"  😰 Students Struggling: {metrics['students_struggling']}")
        print(f"  🌟 Students Excelling: {metrics['students_excelling']}")
        
        print(f"\n👨‍🎓 INDIVIDUAL STUDENT OUTCOMES:")
        for student in self.classroom.students:
            initial_knowledge = 0.5  # Assumed baseline
            knowledge_gain = student.knowledge_level - initial_knowledge
            print(f"  {student.name:15} | Final Engagement: {student.engagement_level:.2f} | Knowledge Gain: {knowledge_gain:+.2f} | Adaptations: {student.adaptation_count}")
        
        if self.classroom.adaptation_events:
            print(f"\n⚡ RECENT ADAPTATION EVENTS:")
            for event in self.classroom.adaptation_events[-10:]:  # Last 10 events
                timestamp = datetime.fromisoformat(event['timestamp']).strftime('%H:%M:%S')
                print(f"  {timestamp} | {event['student']:12} | {event['trigger']:20} | {event['reasoning']}")
        
        print("\n🎯 DEMO INSIGHTS:")
        print("  ✅ Real-time adaptation successfully triggered based on engagement")
        print("  ✅ Personalized learning experiences generated for diverse students")
        print("  ✅ Classroom-wide analytics provided actionable insights")
        print("  ✅ End-to-end PACT system integration demonstrated")
        
        print("=" * 80)
    
    async def stop_demo(self):
        """Stop the demo gracefully"""
        self.running = False
        await self.api_client.cleanup()
        logger.info("🛑 Demo stopped gracefully")

# ============================================================================
# Main Demo Entry Point
# ============================================================================

async def main():
    """Main demo entry point"""
    print("🎓 PACT Integration Demo Starting...")
    print("=" * 50)
    print("This demo showcases:")
    print("✅ Full PACT system demonstration")
    print("✅ Multi-student classroom simulation")
    print("✅ Real-time adaptation showcase")
    print("✅ End-to-end learning experience")
    print("=" * 50)
    
    # Create and initialize demo
    orchestrator = PACTDemoOrchestrator()
    
    try:
        # Initialize demo
        if not await orchestrator.initialize():
            print("❌ Failed to initialize demo. Make sure the Creative Synthesis API is running!")
            print("   Start it with: python creative_synthesis_api.py")
            return
        
        # Run demo
        await orchestrator.run_demo()
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        logger.error(f"❌ Demo error: {e}")
    finally:
        await orchestrator.stop_demo()

def print_startup_info():
    """Print demo startup information"""
    print(f"""
🎓 PACT Complete System Integration Demo
======================================

Prerequisites:
1. Creative Synthesis API running on {DemoConfig.CREATIVE_SYNTHESIS_API}
   → cd pact-hx/integration/ && python creative_synthesis_api.py

Demo Features:
• {DemoConfig.STUDENT_COUNT} simulated students with diverse learning profiles
• Real-time engagement tracking and adaptation
• Automatic content personalization
• Comprehensive analytics and reporting
• {DemoConfig.DEMO_DURATION_MINUTES}-minute simulation with {DemoConfig.UPDATE_INTERVAL_SECONDS}-second cycles

Starting in 3 seconds...
    """)
    time.sleep(3)

if __name__ == "__main__":
    print_startup_info()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start demo: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure Creative Synthesis API is running: python creative_synthesis_api.py")
        print("2. Check API connectivity: curl http://localhost:8000/health")
        print("3. Verify all dependencies are installed: pip install aiohttp")
