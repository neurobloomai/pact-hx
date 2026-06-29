/**
 * PACT WebSocket Client
 * =====================
 * 
 * Standardized WebSocket communication layer for all PACT frontend components.
 * Provides reliable real-time communication with automatic reconnection and event handling.
 */

class PACTWebSocketClient {
    constructor(endpoint, options = {}) {
        this.endpoint = endpoint;
        this.options = {
            maxReconnectAttempts: options.maxReconnectAttempts || 5,
            reconnectDelay: options.reconnectDelay || 1000,
            heartbeatInterval: options.heartbeatInterval || 30000,
            debugMode: options.debugMode || false,
            ...options
        };
        
        // Connection state
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.heartbeatTimer = null;
        
        // Event handling
        this.eventListeners = new Map();
        this.messageQueue = [];
        
        // Session data
        this.sessionId = null;
        this.userId = null;
        this.userType = null; // 'participant' or 'operator'
        
        this.log('🔧 WebSocket client initialized');
    }
    
    // Connection Management
    connect(sessionData = {}) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.log('⚠️ Already connected');
            return Promise.resolve();
        }
        
        return new Promise((resolve, reject) => {
            try {
                this.log(`🔗 Connecting to ${this.endpoint}...`);
                
                // Store session data
                this.sessionId = sessionData.sessionId;
                this.userId = sessionData.userId;
                this.userType = sessionData.userType;
                
                // Create WebSocket connection
                this.socket = new WebSocket(this.endpoint);
                
                // Set up event handlers
                this.socket.onopen = (event) => {
                    this.handleOpen(event);
                    resolve(this.socket);
                };
                
                this.socket.onmessage = (event) => {
                    this.handleMessage(event);
                };
                
                this.socket.onclose = (event) => {
                    this.handleClose(event);
                };
                
                this.socket.onerror = (event) => {
                    this.handleError(event);
                    reject(event);
                };
                
                // Set connection timeout
                setTimeout(() => {
                    if (this.socket.readyState !== WebSocket.OPEN) {
                        reject(new Error('Connection timeout'));
                    }
                }, 10000);
                
            } catch (error) {
                this.log('❌ Connection error:', error);
                reject(error);
            }
        });
    }
    
    disconnect() {
        this.log('🔌 Disconnecting...');
        
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
        
        if (this.socket) {
            this.socket.close(1000, 'Client disconnect');
            this.socket = null;
        }
        
        this.isConnected = false;
        this.reconnectAttempts = 0;
    }
    
    // Event Handlers
    handleOpen(event) {
        this.log('✅ Connected to PACT system');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        
        // Start heartbeat
        this.startHeartbeat();
        
        // Send any queued messages
        this.flushMessageQueue();
        
        // Send initial session data if available
        if (this.sessionId) {
            this.send('session_join', {
                sessionId: this.sessionId,
                userId: this.userId,
                userType: this.userType,
                timestamp: new Date().toISOString()
            });
        }
        
        // Emit connection event
        this.emit('connected', { timestamp: Date.now() });
    }
    
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            this.log('📨 Message received:', data.type);
            
            // Handle system messages
            if (data.type === 'heartbeat') {
                this.send('heartbeat_ack');
                return;
            }
            
            if (data.type === 'error') {
                this.log('❌ Server error:', data.message);
                this.emit('error', data);
                return;
            }
            
            // Emit the message to listeners
            this.emit(data.type, data.payload || data);
            
        } catch (error) {
            this.log('❌ Failed to parse message:', error);
        }
    }
    
    handleClose(event) {
        this.log(`🔌 Connection closed: ${event.code} ${event.reason}`);
        this.isConnected = false;
        
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
        
        // Emit disconnection event
        this.emit('disconnected', { code: event.code, reason: event.reason });
        
        // Attempt reconnection if not intentional disconnect
        if (event.code !== 1000 && this.reconnectAttempts < this.options.maxReconnectAttempts) {
            this.attemptReconnect();
        }
    }
    
    handleError(event) {
        this.log('❌ WebSocket error:', event);
        this.emit('error', { type: 'websocket_error', event });
    }
    
    // Reconnection Logic
    attemptReconnect() {
        if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
            this.log('❌ Max reconnection attempts reached');
            this.emit('reconnection_failed');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = this.options.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        this.log(`🔄 Reconnection attempt ${this.reconnectAttempts} in ${delay}ms`);
        this.emit('reconnecting', { attempt: this.reconnectAttempts, delay });
        
        setTimeout(() => {
            this.connect({
                sessionId: this.sessionId,
                userId: this.userId,
                userType: this.userType
            }).catch(error => {
                this.log('❌ Reconnection failed:', error);
            });
        }, delay);
    }
    
    // Heartbeat System
    startHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
        }
        
        this.heartbeatTimer = setInterval(() => {
            if (this.isConnected) {
                this.send('heartbeat', { timestamp: Date.now() });
            }
        }, this.options.heartbeatInterval);
    }
    
    // Message Handling
    send(type, payload = {}) {
        const message = {
            type,
            payload,
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId
        };
        
        if (this.isConnected && this.socket.readyState === WebSocket.OPEN) {
            try {
                this.socket.send(JSON.stringify(message));
                this.log(`📤 Sent: ${type}`);
                return true;
            } catch (error) {
                this.log('❌ Send failed:', error);
                this.queueMessage(message);
                return false;
            }
        } else {
            this.log(`📋 Queued: ${type} (not connected)`);
            this.queueMessage(message);
            return false;
        }
    }
    
    queueMessage(message) {
        this.messageQueue.push(message);
        
        // Limit queue size
        if (this.messageQueue.length > 50) {
            this.messageQueue.shift();
            this.log('⚠️ Message queue overflow, oldest message dropped');
        }
    }
    
    flushMessageQueue() {
        this.log(`📤 Flushing ${this.messageQueue.length} queued messages`);
        
        while (this.messageQueue.length > 0 && this.isConnected) {
            const message = this.messageQueue.shift();
            try {
                this.socket.send(JSON.stringify(message));
                this.log(`📤 Queued message sent: ${message.type}`);
            } catch (error) {
                this.log('❌ Failed to send queued message:', error);
                // Put it back at the front
                this.messageQueue.unshift(message);
                break;
            }
        }
    }
    
    // Event System
    on(eventType, callback) {
        if (!this.eventListeners.has(eventType)) {
            this.eventListeners.set(eventType, []);
        }
        this.eventListeners.get(eventType).push(callback);
        
        return () => this.off(eventType, callback);
    }
    
    off(eventType, callback) {
        if (this.eventListeners.has(eventType)) {
            const listeners = this.eventListeners.get(eventType);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }
    
    emit(eventType, data = {}) {
        if (this.eventListeners.has(eventType)) {
            this.eventListeners.get(eventType).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    this.log('❌ Event callback error:', error);
                }
            });
        }
    }
    
    // High-level API Methods
    
    // Participant Methods
    createParticipantSession(participantData) {
        return this.send('create_participant_session', participantData);
    }
    
    generateExperience(experienceData) {
        return this.send('generate_experience', experienceData);
    }
    
    updateEngagement(engagementData) {
        return this.send('engagement_update', engagementData);
    }
    
    triggerAdaptation(adaptationData) {
        return this.send('trigger_adaptation', adaptationData);
    }
    
    // Operator Methods
    joinOperatorDashboard(classroomData) {
        return this.send('join_operator_dashboard', classroomData);
    }
    
    broadcastToClassroom(message) {
        return this.send('classroom_broadcast', message);
    }
    
    assistParticipant(participantData) {
        return this.send('assist_participant', participantData);
    }
    
    // Utility Methods
    getConnectionState() {
        return {
            isConnected: this.isConnected,
            readyState: this.socket ? this.socket.readyState : null,
            reconnectAttempts: this.reconnectAttempts,
            queuedMessages: this.messageQueue.length,
            sessionId: this.sessionId
        };
    }
    
    log(...args) {
        if (this.options.debugMode) {
            console.log('[PACT WebSocket]', ...args);
        }
    }
}

// Specialized WebSocket Clients

class ParticipantWebSocketClient extends PACTWebSocketClient {
    constructor(endpoint, options = {}) {
        super(endpoint, { ...options, userType: 'participant' });
        this.participantProfile = null;
        this.currentExperience = null;
    }
    
    setParticipantProfile(profile) {
        this.participantProfile = profile;
        this.userId = profile.participant_id;
        
        // Send profile to server
        if (this.isConnected) {
            this.send('participant_profile_update', profile);
        }
    }
    
    startLearningSession() {
        if (!this.participantProfile) {
            throw new Error('Participant profile must be set before starting session');
        }
        
        return this.createParticipantSession({
            participant_id: this.participantProfile.participant_id,
            name: this.participantProfile.name,
            learning_style: this.participantProfile.learning_style,
            grade_level: this.participantProfile.grade_level,
            preferences: this.participantProfile.preferences
        });
    }
    
    requestContent(subject, topic) {
        return this.generateExperience({
            sessionId: this.sessionId,
            subject,
            topic,
            preferences: this.participantProfile?.preferences
        });
    }
    
    reportEngagement(metrics) {
        return this.updateEngagement({
            sessionId: this.sessionId,
            ...metrics
        });
    }
}

class OperatorWebSocketClient extends PACTWebSocketClient {
    constructor(endpoint, options = {}) {
        super(endpoint, { ...options, userType: 'operator' });
        this.classroomId = null;
        this.participants = new Map();
    }
    
    joinClassroom(classroomId, operatorData = {}) {
        this.classroomId = classroomId;
        this.userId = operatorData.operator_id || 'operator_default';
        
        return this.joinOperatorDashboard({
            classroomId,
            operatorId: this.userId,
            ...operatorData
        });
    }
    
    monitorParticipant(participantId) {
        // Request specific participant updates
        return this.send('monitor_participant', {
            participantId,
            classroomId: this.classroomId
        });
    }
    
    helpParticipant(participantId, interventionType = 'general_assistance') {
        return this.assistParticipant({
            participantId,
            classroomId: this.classroomId,
            interventionType,
            timestamp: new Date().toISOString()
        });
    }
    
    sendClassroomMessage(message, messageType = 'announcement') {
        return this.broadcastToClassroom({
            classroomId: this.classroomId,
            message,
            messageType,
            senderId: this.userId
        });
    }
}

// Connection Factory
class PACTWebSocketFactory {
    static createParticipantClient(endpoint, options = {}) {
        return new ParticipantWebSocketClient(endpoint, options);
    }
    
    static createOperatorClient(endpoint, options = {}) {
        return new OperatorWebSocketClient(endpoint, options);
    }
    
    static createGenericClient(endpoint, options = {}) {
        return new PACTWebSocketClient(endpoint, options);
    }
}

// Auto-connection utilities
class PACTConnectionManager {
    constructor() {
        this.clients = new Map();
        this.defaultEndpoint = 'ws://localhost:3000';
    }
    
    getOrCreateClient(clientId, type = 'generic', endpoint = null, options = {}) {
        if (this.clients.has(clientId)) {
            return this.clients.get(clientId);
        }
        
        const wsEndpoint = endpoint || this.defaultEndpoint;
        let client;
        
        switch (type) {
            case 'participant':
                client = PACTWebSocketFactory.createParticipantClient(wsEndpoint, options);
                break;
            case 'operator':
                client = PACTWebSocketFactory.createOperatorClient(wsEndpoint, options);
                break;
            default:
                client = PACTWebSocketFactory.createGenericClient(wsEndpoint, options);
        }
        
        this.clients.set(clientId, client);
        return client;
    }
    
    removeClient(clientId) {
        if (this.clients.has(clientId)) {
            const client = this.clients.get(clientId);
            client.disconnect();
            this.clients.delete(clientId);
        }
    }
    
    disconnectAll() {
        this.clients.forEach(client => client.disconnect());
        this.clients.clear();
    }
}

// Global connection manager instance
const pactConnectionManager = new PACTConnectionManager();

// Convenience functions for common usage
function connectAsParticipant(participantProfile, endpoint = null, options = {}) {
    const client = pactConnectionManager.getOrCreateClient(
        participantProfile.participant_id, 
        'participant', 
        endpoint, 
        { ...options, debugMode: true }
    );
    
    client.setParticipantProfile(participantProfile);
    return client.connect({ 
        sessionId: `session_${participantProfile.participant_id}_${Date.now()}`,
        userId: participantProfile.participant_id,
        userType: 'participant'
    }).then(() => client);
}

function connectAsOperator(operatorData, classroomId, endpoint = null, options = {}) {
    const client = pactConnectionManager.getOrCreateClient(
        operatorData.operator_id || 'operator_default', 
        'operator', 
        endpoint, 
        { ...options, debugMode: true }
    );
    
    return client.connect({
        sessionId: `operator_${classroomId}_${Date.now()}`,
        userId: operatorData.operator_id,
        userType: 'operator'
    }).then(() => {
        return client.joinClassroom(classroomId, operatorData);
    }).then(() => client);
}

// Export for different environments
if (typeof window !== 'undefined') {
    // Browser environment
    window.PACTWebSocketClient = PACTWebSocketClient;
    window.ParticipantWebSocketClient = ParticipantWebSocketClient;
    window.OperatorWebSocketClient = OperatorWebSocketClient;
    window.PACTWebSocketFactory = PACTWebSocketFactory;
    window.pactConnectionManager = pactConnectionManager;
    window.connectAsParticipant = connectAsParticipant;
    window.connectAsOperator = connectAsOperator;
}

if (typeof module !== 'undefined' && module.exports) {
    // Node.js environment
    module.exports = {
        PACTWebSocketClient,
        ParticipantWebSocketClient,
        OperatorWebSocketClient,
        PACTWebSocketFactory,
        PACTConnectionManager,
        connectAsParticipant,
        connectAsOperator
    };
}
