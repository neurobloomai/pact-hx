#!/usr/bin/env python3
"""
PACT Basic Integration Demo - Web Server
========================================

Interactive demo server that integrates all PACT components:
- Serves demo.html interface
- Provides WebSocket real-time updates  
- Connects to Creative Synthesis API
- Manages student sessions and adaptations

This creates a complete interactive demo experience.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import asyncio
import aiohttp
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
import logging
import threading
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

class Config:
    CREATIVE_SYNTHESIS_API = "http://localhost:8000"
    DEMO_PORT = 5000
    SECRET_KEY = 'pact_demo_secret_key'
    
    # Demo settings
    SUBJECTS = ["Mathematics", "Science", "History"]
    MATH_TOPICS = ["Fractions", "Multiplication", "Geometry"]
    
# ============================================================================
# Flask App Setup
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def demo_home():
    return "<h1>🎓 PACT Demo Server is Running!</h1><p>Server is working. Open the frontend files directly in your browser.</p>"

@app.route('/student')
def student_interface():
    """Serve the actual student interface"""
    try:
        # Path to the student interface file
        file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'student_interface', 'demo.html')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f'''
            <h1>❌ Student Interface Not Found</h1>
            <p>Looking for file at: <code>{file_path}</code></p>
            <p>Please ensure the file exists and try again.</p>
            <p><a href="/">← Back</a></p>
            '''
    except Exception as e:
        return f"<h1>Error loading student interface:</h1><p>{str(e)}</p>"

@app.route('/teacher')
def teacher_interface():
    """Serve the actual teacher dashboard"""
    try:
        # Path to the teacher dashboard file
        file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'teacher_dashboard.html')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f'''
            <h1>❌ Teacher Dashboard Not Found</h1>
            <p>Looking for file at: <code>{file_path}</code></p>
            <p>Please ensure the file exists and try again.</p>
            <p><a href="/">← Back</a></p>
            '''
    except Exception as e:
        return f"<h1>Error loading teacher dashboard:</h1><p>{str(e)}</p>"

# Add support for static assets (CSS, JS, images)
@app.route('/frontend/<path:filename>')
def serve_frontend_assets(filename):
    """Serve frontend static assets"""
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, filename)

# Global state
active_sessions = {}  # session_id -> student data
api_client = None

# ============================================================================
# Student Session Management
# ============================================================================

class StudentSession:
    """Manages individual student session state"""
    
    def __init__(self, student_id: str, student_data: Dict):
        self.student_id = student_id
        self.session_id = f"session_{uuid.uuid4().hex[:8]}"
        self.name = student_data.get('name', 'Student')
        self.learning_style = student_data.get('learning_style', 'visual')
        self.grade_level = student_data.get('grade', '5th Grade')
        self.difficulty = student_data.get('difficulty_preference', 'medium')
        
        # Session state
        self.current_experience_id = None
        self.engagement_level = 0.5
        self.knowledge_level = student_data.get('knowledge_level', 0.5)
        self.adaptation_count = 0
        self.start_time = datetime.now()
        self.last_activity = datetime.now()
        
        # Real-time data
        self.metrics = {
            'mouse_movements': 0,
            'clicks': 0,
            'time_on_page': 0,
            'focus_time': 0,
            'interactions': 0
        }
        
        logger.info(f"👨‍🎓 Student session created: {self.name} ({self.student_id})")
    
    def update_engagement(self, engagement_data: Dict):
        """Update engagement based on frontend tracking"""
        self.metrics.update(engagement_data.get('metrics', {}))
        self.engagement_level = engagement_data.get('engagement_level', self.engagement_level)
        self.last_activity = datetime.now()
    
    def to_dict(self):
        """Convert session to dictionary for JSON serialization"""
        return {
            'student_id': self.student_id,
            'session_id': self.session_id,
            'name': self.name,
            'learning_style': self.learning_style,
            'grade_level': self.grade_level,
            'current_experience_id': self.current_experience_id,
            'engagement_level': self.engagement_level,
            'knowledge_level': self.knowledge_level,
            'adaptation_count': self.adaptation_count,
            'metrics': self.metrics,
            'session_duration': str(datetime.now() - self.start_time).split('.')[0]
        }

# ============================================================================
# API Client
# ============================================================================

class AsyncAPIClient:
    """Async API client for Creative Synthesis"""
    
    def __init__(self):
        self.session = None
        self.base_url = Config.CREATIVE_SYNTHESIS_API
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        
        # Test connectivity
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    logger.info("✅ Connected to Creative Synthesis API")
                    return True
                else:
                    logger.error(f"❌ API health check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to API: {e}")
            return False
    
    async def generate_experience(self, student_session: StudentSession, subject: str, topic: str):
        """Generate educational experience"""
        if not self.session:
            await self.initialize()
        
        request_data = {
            "context": {
                "student_id": student_session.student_id,
                "session_id": student_session.session_id,
                "subject": subject,
                "grade_level": student_session.grade_level,
                "learning_style": student_session.learning_style,
                "difficulty_preference": student_session.difficulty,
                "interests": [],
                "current_knowledge_level": student_session.knowledge_level,
                "engagement_score": student_session.engagement_level,
                "attention_span": 15
            },
            "content_type": "lesson",
            "topic": topic,
            "duration_minutes": 15,
            "adaptation_enabled": True,
            "real_time_feedback": True
        }
        
        try:
            async with self.session.post(f"{self.base_url}/generate", json=request_data) as response:
                if response.status == 200:
                    experience = await response.json()
                    student_session.current_experience_id = experience["experience_id"]
                    return experience
                else:
                    logger.error(f"❌ Experience generation failed: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"❌ API error: {e}")
            return None
    
    async def trigger_adaptation(self, student_session: StudentSession, trigger_type: str, confidence: float = 0.8):
        """Trigger adaptation for student experience"""
        if not student_session.current_experience_id:
            return None
        
        trigger_data = {
            "trigger_type": trigger_type,
            "confidence": confidence,
            "context": {
                "current_engagement": student_session.engagement_level,
                "learning_style": student_session.learning_style
            },
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/adapt/{student_session.current_experience_id}", 
                json=trigger_data
            ) as response:
                if response.status == 200:
                    adaptation = await response.json()
                    student_session.adaptation_count += 1
                    return adaptation
                else:
                    logger.error(f"❌ Adaptation failed: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"❌ Adaptation error: {e}")
            return None
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()

# ============================================================================
# Web Routes
# ============================================================================

@app.route('/')
def index():
    """Serve the main demo interface"""
    return send_from_directory('.', 'demo.html')

@app.route('/engagement_tracker.js')
def engagement_tracker():
    """Serve the engagement tracker JavaScript"""
    return send_from_directory('.', 'engagement_tracker.js')

@app.route('/api/health')
def health():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(active_sessions),
        'api_connected': api_client is not None
    })

@app.route('/api/students', methods=['POST'])
def create_student_session():
    """Create new student session"""
    try:
        student_data = request.json
        student_id = student_data.get('student_id') or f"student_{uuid.uuid4().hex[:6]}"
        
        # Create session
        session = StudentSession(student_id, student_data)
        active_sessions[session.session_id] = session
        
        logger.info(f"📝 Created session for {session.name}")
        
        return jsonify({
            'success': True,
            'session': session.to_dict()
        })
    except Exception as e:
        logger.error(f"❌ Failed to create session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/experiences', methods=['POST'])
def generate_experience():
    """Generate educational experience for student"""
    try:
        data = request.json
        session_id = data.get('session_id')
        subject = data.get('subject', 'Mathematics')
        topic = data.get('topic', 'Fractions')
        
        if session_id not in active_sessions:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        student_session = active_sessions[session_id]
        
        # Generate experience asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        experience = loop.run_until_complete(
            api_client.generate_experience(student_session, subject, topic)
        )
        loop.close()
        
        if experience:
            # Emit to connected clients
            socketio.emit('experience_generated', {
                'student_id': student_session.student_id,
                'experience': experience
            }, room=session_id)
            
            return jsonify({'success': True, 'experience': experience})
        else:
            return jsonify({'success': False, 'error': 'Failed to generate experience'}), 500
            
    except Exception as e:
        logger.error(f"❌ Experience generation error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/adaptations', methods=['POST'])
def trigger_adaptation():
    """Trigger adaptation for student"""
    try:
        data = request.json
        session_id = data.get('session_id')
        trigger_type = data.get('trigger_type')
        confidence = data.get('confidence', 0.8)
        
        if session_id not in active_sessions:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        student_session = active_sessions[session_id]
        
        # Trigger adaptation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        adaptation = loop.run_until_complete(
            api_client.trigger_adaptation(student_session, trigger_type, confidence)
        )
        loop.close()
        
        if adaptation:
            # Emit to connected clients
            socketio.emit('adaptation_triggered', {
                'student_id': student_session.student_id,
                'adaptation': adaptation,
                'trigger_type': trigger_type
            }, room=session_id)
            
            logger.info(f"⚡ Adaptation triggered for {student_session.name}: {trigger_type}")
            
            return jsonify({'success': True, 'adaptation': adaptation})
        else:
            return jsonify({'success': False, 'error': 'Failed to trigger adaptation'}), 500
            
    except Exception as e:
        logger.error(f"❌ Adaptation error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sessions/<session_id>')
def get_session(session_id):
    """Get student session data"""
    if session_id in active_sessions:
        return jsonify(active_sessions[session_id].to_dict())
    else:
        return jsonify({'error': 'Session not found'}), 404

@app.route('/api/dashboard')
def get_dashboard_data():
    """Get dashboard overview data"""
    sessions = [session.to_dict() for session in active_sessions.values()]
    
    total_adaptations = sum(session.adaptation_count for session in active_sessions.values())
    avg_engagement = sum(session.engagement_level for session in active_sessions.values()) / len(active_sessions) if active_sessions else 0
    
    return jsonify({
        'total_sessions': len(active_sessions),
        'total_adaptations': total_adaptations,
        'average_engagement': avg_engagement,
        'sessions': sessions
    })

# ============================================================================
# WebSocket Events
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"🔗 Client connected: {request.sid}")
    emit('connected', {'status': 'Connected to PACT Demo Server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"🔌 Client disconnected: {request.sid}")

@socketio.on('join_session')
def handle_join_session(data):
    """Join student session room"""
    session_id = data.get('session_id')
    if session_id and session_id in active_sessions:
        join_room(session_id)
        student_session = active_sessions[session_id]
        logger.info(f"👥 {student_session.name} joined session room: {session_id}")
        emit('joined_session', {'session_id': session_id, 'student_name': student_session.name})

@socketio.on('engagement_update')
def handle_engagement_update(data):
    """Handle real-time engagement updates from frontend"""
    session_id = data.get('session_id')
    if session_id and session_id in active_sessions:
        student_session = active_sessions[session_id]
        student_session.update_engagement(data)
        
        # Check for adaptation triggers
        engagement_level = data.get('engagement_level', 0.5)
        if engagement_level < 0.3:
            # Trigger low engagement adaptation
            socketio.start_background_task(trigger_background_adaptation, 
                                         session_id, 'engagement_drop', 0.9)
        elif engagement_level > 0.9:
            # Trigger mastery adaptation  
            socketio.start_background_task(trigger_background_adaptation,
                                         session_id, 'mastery_achieved', 0.8)

def trigger_background_adaptation(session_id, trigger_type, confidence):
    """Background task to trigger adaptation"""
    if session_id in active_sessions:
        student_session = active_sessions[session_id]
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            adaptation = loop.run_until_complete(
                api_client.trigger_adaptation(student_session, trigger_type, confidence)
            )
            
            if adaptation:
                socketio.emit('adaptation_triggered', {
                    'student_id': student_session.student_id,
                    'adaptation': adaptation,
                    'trigger_type': trigger_type
                }, room=session_id)
                
                logger.info(f"⚡ Background adaptation: {student_session.name} - {trigger_type}")
        except Exception as e:
            logger.error(f"❌ Background adaptation failed: {e}")
        finally:
            loop.close()

# ============================================================================
# Background Tasks
# ============================================================================

def cleanup_inactive_sessions():
    """Clean up inactive sessions periodically"""
    while True:
        try:
            current_time = datetime.now()
            inactive_sessions = []
            
            for session_id, session in active_sessions.items():
                if (current_time - session.last_activity).seconds > 1800:  # 30 minutes
                    inactive_sessions.append(session_id)
            
            for session_id in inactive_sessions:
                logger.info(f"🧹 Cleaning up inactive session: {active_sessions[session_id].name}")
                del active_sessions[session_id]
                
            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            logger.error(f"❌ Cleanup task error: {e}")
            time.sleep(60)

# ============================================================================
# Application Startup
# ============================================================================

async def initialize_api_client():
    """Initialize the API client"""
    global api_client
    api_client = AsyncAPIClient()
    success = await api_client.initialize()
    return success

def run_initialization():
    """Run async initialization in thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    success = loop.run_until_complete(initialize_api_client())
    loop.close()
    return success

# ============================================================================
# Demo Templates (Fallback if HTML files not found)
# ============================================================================

DEMO_INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PACT Integration Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 20px; }
        .demo-links { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }
        .demo-card { background: #3498db; color: white; padding: 30px; border-radius: 8px; text-decoration: none; text-align: center; transition: transform 0.2s; }
        .demo-card:hover { transform: translateY(-2px); background: #2980b9; }
        .demo-card h3 { margin: 0 0 10px 0; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 6px; border-left: 4px solid #27ae60; margin: 20px 0; }
        .api-links { margin-top: 30px; }
        .api-links a { display: inline-block; margin: 5px 10px 5px 0; padding: 8px 16px; background: #ecf0f1; border-radius: 4px; text-decoration: none; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 PACT Integration Demo</h1>
        <p>Welcome to the PACT educational system demonstration. Choose your interface:</p>
        
        <div class="demo-links">
            <a href="/student" class="demo-card">
                <h3>👨‍🎓 Student Interface</h3>
                <p>Interactive learning experience with real-time adaptation</p>
            </a>
            
            <a href="/teacher" class="demo-card">
                <h3>👩‍🏫 Teacher Dashboard</h3>
                <p>Classroom monitoring and analytics</p>
            </a>
        </div>
        
        <div class="status">
            <strong>✅ System Status:</strong> All components running and connected
        </div>
        
        <div class="api-links">
            <strong>API Endpoints:</strong>
            <a href="/api/health">Health Check</a>
            <a href="/api/dashboard">Dashboard Data</a>
            <a href="/api/sessions">Active Sessions</a>
        </div>
        
        <hr style="margin: 30px 0;">
        
        <h2>🚀 Quick Demo Steps:</h2>
        <ol>
            <li><strong>Student Experience:</strong> Click "Student Interface" → Select profile → Start learning → Watch real-time adaptation</li>
            <li><strong>Teacher Experience:</strong> Click "Teacher Dashboard" → Monitor students → Use classroom controls</li>
            <li><strong>Integration:</strong> Open both interfaces to see real-time synchronization</li>
        </ol>
        
        <p><small>💡 <strong>Tip:</strong> Open both interfaces in separate browser tabs to see the complete integration in action!</small></p>
    </div>
</body>
</html>
'''

TEACHER_FALLBACK_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PACT Teacher Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; text-align: center; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .error { background: #f8d7da; color: #721c24; padding: 20px; border-radius: 6px; margin: 20px 0; }
        .instructions { background: #e8f4f8; padding: 20px; border-radius: 6px; margin: 20px 0; text-align: left; }
        a { color: #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👩‍🏫 PACT Teacher Dashboard</h1>
        
        <div class="error">
            <strong>⚠️ Teacher Dashboard Not Found</strong><br>
            The teacher dashboard HTML file is not available at the expected location.
        </div>
        
        <div class="instructions">
            <strong>📁 Expected File Location:</strong><br>
            <code>frontend/teacher_dashboard.html</code>
            
            <p><strong>🔧 To Fix This:</strong></p>
            <ol>
                <li>Ensure the <code>frontend/</code> folder exists</li>
                <li>Create or copy the <code>teacher_dashboard.html</code> file</li>
                <li>Refresh this page</li>
            </ol>
        </div>
        
        <p><a href="/">← Back to Demo Home</a></p>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    print("🚀 PACT Integration Demo Server Starting...")
    print("=" * 50)
    
    # Initialize API client
    print("🔗 Connecting to Creative Synthesis API...")
    if run_initialization():
        print("✅ API connection successful")
    else:
        print("❌ API connection failed - some features may not work")
        print("   Make sure Creative Synthesis API is running on localhost:8000")
    
    # Start cleanup task
    cleanup_thread = threading.Thread(target=cleanup_inactive_sessions, daemon=True)
    cleanup_thread.start()
    
    print(f"\n🌐 Demo server starting on http://localhost:{Config.DEMO_PORT}")
    print("📱 Open demo.html in your browser to begin")
    print("📊 Dashboard available at /api/dashboard")
    print("\nPress Ctrl+C to stop")
    print("=" * 50)
    
    try:
        socketio.run(app, host='0.0.0.0', port=Config.DEMO_PORT, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Demo server stopped")
    finally:
        # Cleanup
        if api_client:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(api_client.cleanup())
            loop.close()
