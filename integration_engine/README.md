# PACT Integration Engine

Node.js server for real-time component coordination and orchestration.

## 🎯 Purpose

The Integration Engine serves as the **central orchestration layer** for the PACT system, coordinating real-time communication between:

- **Creative Synthesis API** (Python/FastAPI)
- **Participant Interfaces** (Browser/JavaScript) 
- **Operator Dashboard** (Browser/JavaScript)
- **Demo Server** (Python/Flask)

## 🏗️ Architecture

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│ Participant Browser │◄──────────────►│                 │
└─────────────────┘                 │                 │
                                    │  Integration    │    HTTP
┌─────────────────┐    WebSocket    │     Engine      │◄─────────►┌──────────────────┐
│Operator Dashboard│◄──────────────►│   (Node.js)     │           │Creative Synthesis│
└─────────────────┘                 │                 │           │   API (Python)   │
                                    │  Port: 3000     │           └──────────────────┘
┌─────────────────┐    WebSocket    │                 │
│   Demo Server   │◄──────────────►│                 │
└─────────────────┘                 └─────────────────┘
```

## 🚀 Quick Start

### **Installation**
```bash
cd integration_engine/
npm install
```

### **Start Server**
```bash
node integration_engine.js
```

### **Verify Running**
```bash
curl http://localhost:3000/health
```

Expected response:
```json
{
  "status": "healthy",
  "activeSessions": 0,
  "activeClassrooms": 0,
  "connectedClients": 0,
  "apis": {
    "creativeSynthesis": true,
    "demoServer": true
  }
}
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Optional: Create .env file
PORT=3000
CREATIVE_SYNTHESIS_API=http://localhost:8000
DEMO_SERVER=http://localhost:5000
DEBUG=true
```

### **Default Configuration**
```javascript
const CONFIG = {
    PORT: 3000,
    CREATIVE_SYNTHESIS_API: 'http://localhost:8000',
    DEMO_SERVER: 'http://localhost:5000',
    
    // Adaptation thresholds
    ENGAGEMENT_LOW_THRESHOLD: 0.3,
    ENGAGEMENT_HIGH_THRESHOLD: 0.8,
    CONFUSION_THRESHOLD: 3,
    MASTERY_THRESHOLD: 2
};
```

## 📡 WebSocket API

### **Client Connection**
```javascript
const socket = io('http://localhost:3000');

socket.on('connect', () => {
    console.log('Connected to Integration Engine');
});
```

### **Participant Session Events**

**Create Session:**
```javascript
socket.emit('create_participant_session', {
    participant_id: 'participant_123',
    name: 'Alex Chen',
    learning_style: 'visual',
    grade_level: '5th',
    classroom_id: 'classroom_001'
});

socket.on('session_created', (data) => {
    console.log('Session created:', data.session);
});
```

**Generate Experience:**
```javascript
socket.emit('generate_experience', {
    sessionId: 'session_abc123',
    subject: 'Mathematics',
    topic: 'Fractions'
});

socket.on('experience_generated', (data) => {
    console.log('Experience:', data.experience);
});
```

**Update Engagement:**
```javascript
socket.emit('engagement_update', {
    sessionId: 'session_abc123',
    engagement_level: 0.75,
    metrics: {
        mouseMovements: 45,
        clicks: 12,
        timeOnPage: 180000,
        focusTime: 150000
    }
});
```

### **Operator Dashboard Events**

**Join Dashboard:**
```javascript
socket.emit('join_operator_dashboard', {
    classroomId: 'classroom_001'
});

socket.on('classroom_data', (data) => {
    console.log('Classroom:', data);
});
```

**Listen for Updates:**
```javascript
socket.on('participant_engagement_updated', (data) => {
    console.log(`${data.participantName}: ${data.engagementLevel}`);
});

socket.on('adaptation_event', (data) => {
    console.log(`Adaptation: ${data.adaptationType}`);
});

socket.on('analytics_update', (data) => {
    console.log('Analytics:', data.analytics);
});
```

### **Manual Triggers**

**Trigger Adaptation:**
```javascript
socket.emit('trigger_adaptation', {
    sessionId: 'session_abc123',
    triggerType: 'engagement_drop',
    confidence: 0.8
});

socket.on('adaptation_result', (data) => {
    console.log('Adaptation result:', data);
});
```

## 🔄 REST API Endpoints

### **Health Check**
```bash
GET /health
```
Response:
```json
{
    "status": "healthy",
    "timestamp": "2025-01-15T10:30:00.000Z",
    "activeSessions": 3,
    "activeClassrooms": 1,
    "connectedClients": 5,
    "apis": {
        "creativeSynthesis": true,
        "demoServer": true
    }
}
```

### **Session Management**
```bash
GET /api/sessions
```
Returns all active sessions.

### **Classroom Data**
```bash
GET /api/classrooms/:classroomId
```
Returns classroom data and analytics.

### **Broadcast Messages**
```bash
POST /api/broadcast/:classroomId
Content-Type: application/json

{
    "message": "Class will end in 5 minutes",
    "type": "announcement"
}
```

## 🧠 Intelligent Features

### **Automatic Adaptation Triggers**

**Engagement Drop Detection:**
- Triggers when engagement < 30%
- Confidence based on severity of drop
- Automatically requests content simplification

**Confusion Detection:**
- Monitors confusion signals (rapid clicking, seeking)
- Triggers when signals >= 3 within time window
- Requests additional examples and explanations

**Mastery Achievement:**
- Detects high engagement + mastery signals
- Triggers advanced content and challenges
- Updates difficulty preferences

### **Real-time Analytics**

**Classroom Metrics:**
- Average engagement across all participants
- Participants struggling vs excelling counts
- Adaptation rate and effectiveness
- Total interactions and time on task

**Individual Tracking:**
- Per-participant engagement trends
- Learning progress indicators  
- Adaptation history and responses
- Time-based activity patterns

## 🔧 Development

### **Debug Mode**
```bash
DEBUG=true node integration_engine.js
```

### **Development Server (Auto-reload)**
```bash
npm run dev
```

### **Testing**
```bash
npm test
```

### **Linting**
```bash
npm run lint
```

## 📊 Monitoring

### **Server Status Dashboard**
Visit: `http://localhost:3000`

Shows:
- Active sessions and classrooms
- Connected clients count
- API health status
- Recent activity logs

### **Logs**
```bash
# View real-time logs
tail -f integration_engine.log

# Key log patterns:
# 📝 Session events
# ⚡ Adaptations triggered  
# 🔗 WebSocket connections
# 📊 Analytics updates
```

### **Health Monitoring**
```bash
# Automated health checks every 30 seconds
# Manual health check:
curl http://localhost:3000/health | jq
```

## 🐛 Troubleshooting

### **Common Issues**

**Port already in use:**
```bash
# Find process using port 3000
lsof -i :3000
# Kill process
kill -9 <PID>
```

**API connection failures:**
```bash
# Verify Creative Synthesis API
curl http://localhost:8000/health

# Verify Demo Server  
curl http://localhost:5000/api/health
```

**WebSocket connection issues:**
```javascript
// Check browser console for errors
// Verify CORS settings
// Ensure proper socket.io version
```

**Memory leaks:**
```bash
# Monitor memory usage
node --inspect integration_engine.js
# Open Chrome DevTools for memory profiling
```

### **Debug Commands**
```bash
# Verbose logging
DEBUG=* node integration_engine.js

# Specific module debugging
DEBUG=socket.io:* node integration_engine.js

# Network debugging
DEBUG=axios node integration_engine.js
```

## 🚀 Production Deployment

### **Environment Setup**
```bash
# Production environment variables
NODE_ENV=production
PORT=3000
CREATIVE_SYNTHESIS_API=https://api.pact-edu.com
LOG_LEVEL=info
```

### **Process Management**
```bash
# Using PM2
npm install -g pm2
pm2 start integration_engine.js --name pact-integration
pm2 startup
pm2 save
```

### **Docker Deployment**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "integration_engine.js"]
```

### **Load Balancing**
For high-traffic deployments, use multiple instances:
```bash
pm2 start integration_engine.js -i max
```

## 📝 Dependencies

### **Production Dependencies**
- **express**: Web server framework
- **socket.io**: WebSocket communication
- **cors**: Cross-origin resource sharing
- **axios**: HTTP client for API calls
- **dotenv**: Environment variable management

### **Development Dependencies**
- **nodemon**: Auto-reload during development
- **jest**: Testing framework
- **eslint**: Code linting

## 🔗 Related Components

- **Creative Synthesis API**: `../integration/creative_synthesis_api.py`
- **Participant Interface**: `../examples/integration_demos/demo.html`
- **Operator Dashboard**: `../frontend/operator_dashboard.html`
- **Demo Server**: `../examples/integration_demos/basic_pact_demo.py`

## 🎯 Next Steps

### **Enhancements**
- Rate limiting and throttling
- Advanced analytics and ML insights
- Multi-tenant classroom support  
- Real-time collaboration features

### **Scaling**
- Redis for session storage
- Database integration
- Message queue system
- Microservices architecture

---

🔧 **Integration Engine - Powering Real-time PACT Coordination** ⚡
