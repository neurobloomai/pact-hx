# PACT Integration Demos

Complete system demonstration showcasing real-time adaptive educational experiences.

## 🎯 Overview

This demo integrates all PACT components to showcase:

- **Multi-student classroom simulation** with diverse learning profiles
- **Real-time adaptation** based on engagement and learning patterns  
- **End-to-end learning experience** from content generation to completion
- **Live monitoring dashboard** with analytics and insights
- **Browser-based engagement tracking** with intelligent triggers

## 🏗️ Architecture

```
examples/integration_demos/
├── basic_pact_demo.py      # Complete system orchestrator
├── engagement_tracker.js   # Browser-based tracking
├── demo.html              # Student learning interface
└── README.md              # This guide
```

### Component Integration:
- **Creative Synthesis API** (localhost:8000) - Content generation
- **Classroom Orchestrator** (Python) - Multi-student simulation  
- **Web Dashboard** (localhost:5000) - Real-time monitoring
- **Student Interface** (HTML/JS) - Interactive learning experience

## 🚀 Quick Start

### Prerequisites

1. **Python Dependencies:**
   ```bash
   pip install fastapi uvicorn websockets aiohttp flask flask-socketio
   ```

2. **Start Creative Synthesis API:**
   ```bash
   cd pact-hx/integration/
   python creative_synthesis_api.py
   ```
   ✅ API running on http://localhost:8000

### Demo Options

#### Option 1: Complete Classroom Simulation
```bash
cd examples/integration_demos/
python basic_pact_demo.py
```

**Features:**
- 8 simulated students with diverse profiles
- Real-time engagement monitoring  
- Automatic adaptation triggers
- Comprehensive analytics dashboard
- Final performance reports

**What you'll see:**
```
🎓 Classroom initialized: Fractions
👥 Students: 8

📚 Starting lesson: Fractions
🔔 Maya Patel: engagement_drop (engagement: 0.28)
  ⚡ Adaptation applied: Adding interactive elements
📊 Average Engagement: 0.67 | Adaptations: 15
```

#### Option 2: Interactive Student Experience
```bash
# Open demo.html in your browser
open demo.html
# or
python -m http.server 8080
```

**Features:**
- Student profile selection
- Real-time engagement tracking
- Manual adaptation triggers
- Live metrics dashboard
- Interactive learning content

#### Option 3: Monitoring Dashboard Only
```bash
python basic_pact_demo.py --dashboard
```
📊 Dashboard: http://localhost:5000

## 🎮 Demo Workflows

### 1. Student Learning Experience

1. **Select Profile:** Choose from 4 diverse student profiles
2. **Start Learning:** Generate personalized fraction lesson
3. **Interact:** Engage with visual, audio, or kinesthetic content
4. **Monitor:** Watch real-time engagement metrics
5. **Adapt:** Trigger manual adaptations or let auto-detection work

### 2. Classroom Simulation

1. **Initialize:** Creates 8 students with varied learning styles
2. **Generate:** API creates personalized experiences for each
3. **Monitor:** Tracks engagement patterns in real-time
4. **Adapt:** Automatically triggers content modifications
5. **Report:** Comprehensive analytics and insights

### 3. Teacher Dashboard

1. **Overview:** Classroom metrics and student status
2. **Real-time:** Live engagement tracking and alerts
3. **Analytics:** Performance trends and adaptation history
4. **Insights:** Identification of struggling/excelling students

## 📊 Key Metrics Tracked

### Engagement Indicators
- **Mouse movements** and interaction patterns
- **Time on page** vs focused attention
- **Scroll behavior** and content consumption
- **Click patterns** and user intent signals

### Learning Signals
- **Confusion indicators:** Rapid clicking, excessive seeking
- **Mastery signals:** Steady progress, successful interactions
- **Engagement drops:** Lack of interaction, page blur events

### Adaptation Triggers
- **engagement_drop:** < 30% engagement level
- **confusion_detected:** Multiple confusion signals
- **mastery_achieved:** High engagement + performance

## 🔧 Configuration

### Student Profiles (demo.html)
```javascript
const STUDENT_PROFILES = [
    {
        id: 'student_001',
        name: 'Alex Chen',
        style: 'Visual Learner',
        preferences: {
            learning_style: 'visual',
            difficulty_preference: 'medium',
            knowledge_level: 0.6
        }
    }
    // ... more profiles
];
```

### Engagement Tracking (engagement_tracker.js)
```javascript
const tracker = new PACTEngagementTracker({
    studentId: 'student_123',
    apiEndpoint: 'http://localhost:8000',
    trackingInterval: 5000,        // 5 second updates
    adaptationThreshold: 0.3,      // 30% engagement trigger
    debugMode: true
});
```

### Classroom Simulation (basic_pact_demo.py)
```python
CLASSROOM_SIZE = 8                    # Number of students
DEMO_PORT = 5000                     # Dashboard port
CREATIVE_SYNTHESIS_API_URL = "http://localhost:8000"
```

## 🧪 Testing Scenarios

### Scenario 1: Engagement Drop Response
1. Start student experience
2. Click "Simulate Low Engagement"
3. Observe adaptation: simplified content, interactive elements
4. Monitor recovery in engagement metrics

### Scenario 2: Confusion Detection
1. Rapid clicking on multiple elements
2. Excessive scrolling behavior  
3. Automatic trigger: confusion_detected
4. Response: additional examples, slower pacing

### Scenario 3: Mastery Achievement
1. Steady, purposeful interactions
2. Successful quiz completion
3. High engagement maintenance
4. Response: advanced content, challenge mode

## 📈 Expected Outcomes

### Individual Student Experience
- **Personalized content** based on learning style
- **Real-time adaptations** to maintain engagement
- **Improved learning outcomes** through optimization
- **Detailed progress tracking** and analytics

### Classroom Simulation  
- **Diverse learning patterns** across 8 students
- **Automated intervention** for struggling learners
- **Advanced challenges** for excelling students
- **Comprehensive reporting** on classroom dynamics

## 🐛 Troubleshooting

### Common Issues

**API Connection Failed:**
```bash
# Ensure Creative Synthesis API is running
curl http://localhost:8000/health
```

**WebSocket Connection Error:**
```javascript
// Check browser console for WebSocket errors
// Ensure both API and demo are running
```

**No Adaptations Triggered:**
```python
# Lower adaptation threshold for testing
adaptationThreshold: 0.5  # Easier to trigger
```

**Dashboard Not Loading:**
```bash
# Check if port 5000 is available
lsof -i :5000
```

### Debug Mode

Enable detailed logging:
```javascript
// In demo.html
const DEMO_CONFIG = {
    debugMode: true  // Enables console logging
};
```

```python
# In basic_pact_demo.py
logger.setLevel(logging.DEBUG)
```

## 🔮 Next Steps

### Enhancements
- **Multi-subject support** beyond mathematics
- **Advanced analytics** with ML insights  
- **Teacher intervention tools** for manual guidance
- **Student progress persistence** across sessions

### Integration
- **LMS integration** with Canvas, Blackboard
- **Assessment tools** with automatic grading
- **Parent/guardian dashboards** for home monitoring
- **Mobile apps** for tablet-based learning

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API logs: `tail -f creative_synthesis_api.log`
3. Inspect browser console for frontend errors
4. Verify all prerequisites are installed

---

🎓 **Happy Learning with PACT!** 🚀
