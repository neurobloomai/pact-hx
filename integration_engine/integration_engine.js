#!/usr/bin/env node

/**
 * PACT Integration Engine
 * =======================
 * 
 * Node.js server for real-time component coordination:
 * - WebSocket-based communication between Python and JavaScript
 * - Unified session management and data synchronization  
 * - Real-time adaptation engine with intelligent triggers
 * - Orchestrates Creative Synthesis API, Teacher Dashboard, and Student Interface
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const axios = require('axios');
const EventEmitter = require('events');
const path = require('path');

// ============================================================================
// Configuration
// ============================================================================

const CONFIG = {
    PORT: 3000,
    CREATIVE_SYNTHESIS_API: 'http://localhost:8000',
    DEMO_SERVER: 'http://localhost:5000',
    
    // Adaptation thresholds
    ENGAGEMENT_LOW_THRESHOLD: 0.3,
    ENGAGEMENT_HIGH_THRESHOLD: 0.8,
    CONFUSION_THRESHOLD: 3,
    MASTERY_THRESHOLD: 2,
    
    // Update intervals
    HEALTH_CHECK_INTERVAL: 30000,  // 30 seconds
    SESSION_CLEANUP_INTERVAL: 300000, // 5 minutes
    ANALYTICS_UPDATE_INTERVAL: 5000,  // 5 seconds
};

// ============================================================================
// Application Setup
// ============================================================================

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Event system for internal communication
const orchestrator = new EventEmitter();

// ============================================================================
// Data Models & State Management  
// ============================================================================

class SessionManager {
    constructor() {
        this.sessions = new Map();
        this.teachers = new Map();
        this.classrooms = new Map();
        this.analytics = new Map();
    }
    
    createStudentSession(studentData) {
        const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
        
        const session = {
            sessionId,
            studentId: studentData.student_id,
            name: studentData.name,
            learningStyle: studentData.learning_style,
            gradeLevel: studentData.grade_level,
            classroomId: studentData.classroom_id || 'default',
            
            // Learning state
            currentExperienceId: null,
            engagementLevel: 0.5,
            knowledgeLevel: studentData.knowledge_level || 0.5,
            adaptationCount: 0,
            
            // Session tracking
            startTime: new Date(),
            lastActivity: new Date(),
            socketId: null,
            isActive: true,
            
            // Metrics
            metrics: {
                mouseMovements: 0,
                clicks: 0,
                timeOnPage: 0,
                focusTime: 0,
                interactions: 0,
                confusionSignals: 0,
                masterySignals: 0
            }
        };
        
        this.sessions.set(sessionId, session);
        this.addToClassroom(session);
        
        console.log(`📝 Student session created: ${session.name} (${sessionId})`);
        return session;
    }
    
    addToClassroom(session) {
        const classroomId = session.classroomId;
        
        if (!this.classrooms.has(classroomId)) {
            this.classrooms.set(classroomId, {
                classroomId,
                sessions: new Set(),
                teacher: null,
                subject: 'Mathematics',
                topic: 'Fractions',
                startTime: new Date(),
                totalAdaptations: 0,
                analytics: {
                    averageEngagement: 0.5,
                    totalInteractions: 0,
                    adaptationRate: 0
                }
            });
        }
        
        this.classrooms.get(classroomId).sessions.add(session.sessionId);
    }
    
    updateSessionMetrics(sessionId, metricsData) {
        const session = this.sessions.get(sessionId);
        if (!session) return false;
        
        // Update metrics
        Object.assign(session.metrics, metricsData.metrics || {});
        session.engagementLevel = metricsData.engagement_level || session.engagementLevel;
        session.lastActivity = new Date();
        
        // Trigger adaptation analysis
        this.analyzeForAdaptations(session);
        
        // Update classroom analytics
        this.updateClassroomAnalytics(session.classroomId);
        
        return true;
    }
    
    analyzeForAdaptations(session) {
        const triggers = [];
        
        // Engagement-based triggers
        if (session.engagementLevel < CONFIG.ENGAGEMENT_LOW_THRESHOLD) {
            triggers.push({
                type: 'engagement_drop',
                confidence: 1 - session.engagementLevel,
                reason: `Engagement dropped to ${Math.round(session.engagementLevel * 100)}%`
            });
        }
        
        // Confusion detection
        if (session.metrics.confusionSignals >= CONFIG.CONFUSION_THRESHOLD) {
            triggers.push({
                type: 'confusion_detected', 
                confidence: Math.min(1, session.metrics.confusionSignals / 5),
                reason: `Multiple confusion signals detected`
            });
        }
        
        // Mastery detection
        if (session.metrics.masterySignals >= CONFIG.MASTERY_THRESHOLD && 
            session.engagementLevel > CONFIG.ENGAGEMENT_HIGH_THRESHOLD) {
            triggers.push({
                type: 'mastery_achieved',
                confidence: session.engagementLevel,
                reason: `High engagement with mastery signals`
            });
        }
        
        // Trigger adaptations
        triggers.forEach(trigger => {
            this.triggerAdaptation(session, trigger);
        });
    }
    
    async triggerAdaptation(session, trigger) {
        if (!session.currentExperienceId) return;
        
        try {
            console.log(`⚡ Triggering adaptation for ${session.name}: ${trigger.type}`);
            
            const response = await axios.post(
                `${CONFIG.CREATIVE_SYNTHESIS_API}/adapt/${session.currentExperienceId}`,
                {
                    trigger_type: trigger.type,
                    confidence: trigger.confidence,
                    context: {
                        student_id: session.studentId,
                        current_engagement: session.engagementLevel,
                        learning_style: session.learningStyle,
                        reason: trigger.reason
                    },
                    timestamp: new Date().toISOString()
                }
            );
            
            if (response.status === 200) {
                const adaptation = response.data;
                session.adaptationCount++;
                
                // Update classroom totals
                const classroom = this.classrooms.get(session.classroomId);
                if (classroom) {
                    classroom.totalAdaptations++;
                }
                
                // Broadcast adaptation to all connected clients
                orchestrator.emit('adaptation_triggered', {
                    session,
                    adaptation,
                    trigger
                });
                
                console.log(`✅ Adaptation applied: ${adaptation.reasoning}`);
                return adaptation;
            }
        } catch (error) {
            console.error(`❌ Adaptation failed for ${session.name}:`, error.message);
        }
        
        return null;
    }
    
    updateClassroomAnalytics(classroomId) {
        const classroom = this.classrooms.get(classroomId);
        if (!classroom) return;
        
        const sessions = Array.from(classroom.sessions)
            .map(id => this.sessions.get(id))
            .filter(s => s && s.isActive);
        
        if (sessions.length === 0) return;
        
        // Calculate analytics
        const totalEngagement = sessions.reduce((sum, s) => sum + s.engagementLevel, 0);
        const averageEngagement = totalEngagement / sessions.length;
        
        const totalInteractions = sessions.reduce((sum, s) => 
            sum + s.metrics.clicks + s.metrics.mouseMovements, 0);
        
        classroom.analytics = {
            averageEngagement,
            totalInteractions,
            adaptationRate: classroom.totalAdaptations / sessions.length,
            activeStudents: sessions.length,
            strugglingStudents: sessions.filter(s => s.engagementLevel < 0.5).length,
            excellingStudents: sessions.filter(s => s.engagementLevel > 0.8).length
        };
        
        // Broadcast to teachers
        orchestrator.emit('classroom_analytics_updated', {
            classroomId,
            analytics: classroom.analytics,
            sessions: sessions.map(s => ({
                sessionId: s.sessionId,
                name: s.name,
                engagementLevel: s.engagementLevel,
                adaptationCount: s.adaptationCount
            }))
        });
    }
    
    getClassroomData(classroomId) {
        const classroom = this.classrooms.get(classroomId);
        if (!classroom) return null;
        
        const sessions = Array.from(classroom.sessions)
            .map(id => this.sessions.get(id))
            .filter(s => s && s.isActive);
        
        return {
            classroom,
            sessions,
            analytics: classroom.analytics
        };
    }
    
    cleanupInactiveSessions() {
        const now = new Date();
        const TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes
        
        for (const [sessionId, session] of this.sessions) {
            if (now - session.lastActivity > TIMEOUT_MS) {
                console.log(`🧹 Cleaning up inactive session: ${session.name}`);
                this.sessions.delete(sessionId);
                
                // Remove from classroom
                const classroom = this.classrooms.get(session.classroomId);
                if (classroom) {
                    classroom.sessions.delete(sessionId);
                }
            }
        }
    }
}

// ============================================================================
// API Integration Layer
// ============================================================================

class APIIntegrator {
    constructor() {
        this.healthStatus = {
            creativeSynthesis: false,
            demoServer: false,
            lastCheck: null
        };
    }
    
    async checkHealth() {
        console.log('🔍 Checking API health...');
        
        // Check Creative Synthesis API
        try {
            const response = await axios.get(`${CONFIG.CREATIVE_SYNTHESIS_API}/health`, { timeout: 5000 });
            this.healthStatus.creativeSynthesis = response.status === 200;
        } catch (error) {
            this.healthStatus.creativeSynthesis = false;
            console.warn('⚠️  Creative Synthesis API not responding');
        }
        
        // Check Demo Server
        try {
            const response = await axios.get(`${CONFIG.DEMO_SERVER}/api/health`, { timeout: 5000 });
            this.healthStatus.demoServer = response.status === 200;
        } catch (error) {
            this.healthStatus.demoServer = false;
            console.warn('⚠️  Demo Server not responding');
        }
        
        this.healthStatus.lastCheck = new Date();
        
        // Broadcast health status
        orchestrator.emit('health_status_updated', this.healthStatus);
        
        return this.healthStatus;
    }
    
    async generateExperience(session, subject, topic) {
        try {
            const response = await axios.post(`${CONFIG.CREATIVE_SYNTHESIS_API}/generate`, {
                context: {
                    student_id: session.studentId,
                    session_id: session.sessionId,
                    subject: subject,
                    grade_level: session.gradeLevel,
                    learning_style: session.learningStyle,
                    difficulty_preference: 'medium',
                    interests: [],
                    current_knowledge_level: session.knowledgeLevel,
                    engagement_score: session.engagementLevel,
                    attention_span: 15
                },
                content_type: 'lesson',
                topic: topic,
                duration_minutes: 15,
                adaptation_enabled: true,
                real_time_feedback: true
            });
            
            if (response.status === 200) {
                const experience = response.data;
                session.currentExperienceId = experience.experience_id;
                console.log(`📚 Experience generated for ${session.name}: ${experience.experience_id}`);
                return experience;
            }
        } catch (error) {
            console.error(`❌ Failed to generate experience for ${session.name}:`, error.message);
        }
        
        return null;
    }
}

// ============================================================================
// Global Instances
// ============================================================================

const sessionManager = new SessionManager();
const apiIntegrator = new APIIntegrator();

// ============================================================================
// WebSocket Event Handlers
// ============================================================================

io.on('connection', (socket) => {
    console.log(`🔗 Client connected: ${socket.id}`);
    
    // Send initial health status
    socket.emit('health_status', apiIntegrator.healthStatus);
    
    // Student session management
    socket.on('create_student_session', async (data) => {
        try {
            const session = sessionManager.createStudentSession(data);
            session.socketId = socket.id;
            
            socket.join(`classroom_${session.classroomId}`);
            socket.join(`session_${session.sessionId}`);
            
            socket.emit('session_created', {
                success: true,
                session: {
                    sessionId: session.sessionId,
                    name: session.name,
                    classroomId: session.classroomId
                }
            });
            
            // Notify teachers
            socket.to(`classroom_${session.classroomId}`).emit('student_joined', {
                sessionId: session.sessionId,
                studentName: session.name,
                learningStyle: session.learningStyle
            });
            
            console.log(`👋 ${session.name} joined classroom ${session.classroomId}`);
        } catch (error) {
            socket.emit('session_created', { success: false, error: error.message });
        }
    });
    
    // Experience generation
    socket.on('generate_experience', async (data) => {
        try {
            const session = sessionManager.sessions.get(data.sessionId);
            if (!session) {
                socket.emit('experience_generated', { success: false, error: 'Session not found' });
                return;
            }
            
            const experience = await apiIntegrator.generateExperience(
                session, 
                data.subject || 'Mathematics', 
                data.topic || 'Fractions'
            );
            
            if (experience) {
                socket.emit('experience_generated', {
                    success: true,
                    experience
                });
                
                // Notify teachers
                socket.to(`classroom_${session.classroomId}`).emit('experience_created', {
                    studentName: session.name,
                    experienceId: experience.experience_id,
                    topic: data.topic
                });
            } else {
                socket.emit('experience_generated', { 
                    success: false, 
                    error: 'Failed to generate experience' 
                });
            }
        } catch (error) {
            socket.emit('experience_generated', { success: false, error: error.message });
        }
    });
    
    // Real-time engagement updates
    socket.on('engagement_update', (data) => {
        const success = sessionManager.updateSessionMetrics(data.sessionId, data);
        
        if (success) {
            const session = sessionManager.sessions.get(data.sessionId);
            
            // Broadcast to classroom
            socket.to(`classroom_${session.classroomId}`).emit('student_engagement_updated', {
                sessionId: session.sessionId,
                studentName: session.name,
                engagementLevel: session.engagementLevel,
                metrics: session.metrics
            });
        }
    });
    
    // Teacher dashboard connections
    socket.on('join_teacher_dashboard', (data) => {
        const classroomId = data.classroomId || 'default';
        socket.join(`teacher_${classroomId}`);
        
        // Send current classroom data
        const classroomData = sessionManager.getClassroomData(classroomId);
        socket.emit('classroom_data', classroomData);
        
        console.log(`👩‍🏫 Teacher joined dashboard for classroom ${classroomId}`);
    });
    
    // Manual adaptation triggers
    socket.on('trigger_adaptation', async (data) => {
        try {
            const session = sessionManager.sessions.get(data.sessionId);
            if (!session) {
                socket.emit('adaptation_result', { success: false, error: 'Session not found' });
                return;
            }
            
            const trigger = {
                type: data.triggerType,
                confidence: data.confidence || 0.8,
                reason: `Manual trigger: ${data.triggerType}`
            };
            
            const adaptation = await sessionManager.triggerAdaptation(session, trigger);
            
            socket.emit('adaptation_result', {
                success: !!adaptation,
                adaptation
            });
        } catch (error) {
            socket.emit('adaptation_result', { success: false, error: error.message });
        }
    });
    
    // Disconnect handling
    socket.on('disconnect', () => {
        console.log(`🔌 Client disconnected: ${socket.id}`);
        
        // Find and deactivate session
        for (const [sessionId, session] of sessionManager.sessions) {
            if (session.socketId === socket.id) {
                session.isActive = false;
                console.log(`👋 ${session.name} disconnected`);
                
                // Notify classroom
                socket.to(`classroom_${session.classroomId}`).emit('student_left', {
                    sessionId: session.sessionId,
                    studentName: session.name
                });
                break;
            }
        }
    });
});

// ============================================================================
// Orchestrator Event Handlers
// ============================================================================

orchestrator.on('adaptation_triggered', (data) => {
    const { session, adaptation, trigger } = data;
    
    // Notify student
    io.to(`session_${session.sessionId}`).emit('adaptation_applied', {
        adaptation,
        trigger,
        reasoning: adaptation.reasoning
    });
    
    // Notify teachers
    io.to(`teacher_${session.classroomId}`).emit('adaptation_event', {
        studentName: session.name,
        adaptationType: trigger.type,
        reasoning: adaptation.reasoning,
        timestamp: new Date().toISOString()
    });
    
    console.log(`📢 Adaptation broadcasted for ${session.name}`);
});

orchestrator.on('classroom_analytics_updated', (data) => {
    // Broadcast to teachers
    io.to(`teacher_${data.classroomId}`).emit('analytics_update', data);
});

orchestrator.on('health_status_updated', (healthStatus) => {
    // Broadcast to all clients
    io.emit('health_status', healthStatus);
});

// ============================================================================
// REST API Endpoints
// ============================================================================

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        activeSessions: sessionManager.sessions.size,
        activeClassrooms: sessionManager.classrooms.size,
        connectedClients: io.engine.clientsCount,
        apis: apiIntegrator.healthStatus
    });
});

app.get('/api/sessions', (req, res) => {
    const sessions = Array.from(sessionManager.sessions.values());
    res.json({ sessions });
});

app.get('/api/classrooms/:classroomId', (req, res) => {
    const classroomData = sessionManager.getClassroomData(req.params.classroomId);
    if (classroomData) {
        res.json(classroomData);
    } else {
        res.status(404).json({ error: 'Classroom not found' });
    }
});

app.post('/api/broadcast/:classroomId', (req, res) => {
    const { classroomId } = req.params;
    const { message, type } = req.body;
    
    io.to(`classroom_${classroomId}`).emit('broadcast_message', {
        message,
        type,
        timestamp: new Date().toISOString()
    });
    
    res.json({ success: true });
});

// Serve static files
app.get('/', (req, res) => {
    res.send(`
        <html>
            <head><title>PACT Integration Engine</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px;">
                <h1>🔧 PACT Integration Engine</h1>
                <p>Real-time orchestration layer for PACT educational system</p>
                <h2>Status:</h2>
                <ul>
                    <li>Server: Running on port ${CONFIG.PORT}</li>
                    <li>WebSocket: Active</li>
                    <li>Sessions: ${sessionManager.sessions.size} active</li>
                    <li>Classrooms: ${sessionManager.classrooms.size} active</li>
                </ul>
                <h2>Endpoints:</h2>
                <ul>
                    <li><a href="/health">Health Check</a></li>
                    <li><a href="/api/sessions">Active Sessions</a></li>
                </ul>
                <p><strong>Connected Components:</strong></p>
                <ul>
                    <li>Creative Synthesis API: ${CONFIG.CREATIVE_SYNTHESIS_API}</li>
                    <li>Demo Server: ${CONFIG.DEMO_SERVER}</li>
                </ul>
            </body>
        </html>
    `);
});

// ============================================================================
// Background Tasks
// ============================================================================

// Periodic health checks
setInterval(() => {
    apiIntegrator.checkHealth();
}, CONFIG.HEALTH_CHECK_INTERVAL);

// Session cleanup
setInterval(() => {
    sessionManager.cleanupInactiveSessions();
}, CONFIG.SESSION_CLEANUP_INTERVAL);

// Analytics updates
setInterval(() => {
    for (const classroomId of sessionManager.classrooms.keys()) {
        sessionManager.updateClassroomAnalytics(classroomId);
    }
}, CONFIG.ANALYTICS_UPDATE_INTERVAL);

// ============================================================================
// Server Startup
// ============================================================================

async function startServer() {
    console.log('🚀 PACT Integration Engine starting...');
    console.log('=' .repeat(50));
    
    // Initial health check
    await apiIntegrator.checkHealth();
    
    server.listen(CONFIG.PORT, () => {
        console.log(`✅ Integration Engine running on port ${CONFIG.PORT}`);
        console.log(`🔗 WebSocket server active`);
        console.log(`🌐 Dashboard: http://localhost:${CONFIG.PORT}`);
        console.log(`📊 Health check: http://localhost:${CONFIG.PORT}/health`);
        console.log('');
        console.log('🔧 Component Integration:');
        console.log(`   Creative Synthesis API: ${apiIntegrator.healthStatus.creativeSynthesis ? '✅' : '❌'}`);
        console.log(`   Demo Server: ${apiIntegrator.healthStatus.demoServer ? '✅' : '❌'}`);
        console.log('');
        console.log('🎯 Ready for PACT demo coordination!');
        console.log('=' .repeat(50));
    });
}

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Integration Engine...');
    sessionManager.cleanupInactiveSessions();
    server.close(() => {
        console.log('✅ Server closed gracefully');
        process.exit(0);
    });
});

// Start the server
if (require.main === module) {
    startServer().catch(error => {
        console.error('❌ Failed to start Integration Engine:', error);
        process.exit(1);
    });
}

module.exports = { app, server, io, sessionManager, apiIntegrator };
