/*!
 * PACT Engagement Tracker
 * Browser-based real-time engagement tracking for educational content
 * 
 * Features:
 * - Mouse movement and click tracking
 * - Time on page/section monitoring
 * - Focus/blur detection
 * - Scroll behavior analysis
 * - Interaction pattern recognition
 * - Real-time API integration
 */

class PACTEngagementTracker {
    constructor(config = {}) {
        this.config = {
            studentId: config.studentId || 'anonymous',
            sessionId: config.sessionId || this.generateSessionId(),
            apiEndpoint: config.apiEndpoint || 'http://localhost:8000',
            websocketEndpoint: config.websocketEndpoint || 'ws://localhost:8000',
            trackingInterval: config.trackingInterval || 5000, // 5 seconds
            adaptationThreshold: config.adaptationThreshold || 0.3,
            debugMode: config.debugMode || false
        };
        
        // Engagement metrics
        this.metrics = {
            mouseMovements: 0,
            clicks: 0,
            scrollEvents: 0,
            timeOnPage: 0,
            focusTime: 0,
            unfocusedTime: 0,
            interactionScore: 0.5,
            engagementLevel: 0.5,
            confusionIndicators: 0,
            masteryIndicators: 0
        };
        
        // Tracking state
        this.isActive = false;
        this.startTime = Date.now();
        this.lastInteraction = Date.now();
        this.focusStartTime = Date.now();
        self.isPageFocused = true;
        this.experienceId = null;
        this.websocket = null;
        
        // Event listeners
        this.eventListeners = [];
        
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }
    
    init() {
        this.log('🚀 PACT Engagement Tracker initializing...');
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Connect to WebSocket for real-time updates
        this.connectWebSocket();
        
        // Start tracking loop
        this.startTracking();
        
        this.log('✅ Engagement tracking active');
    }
    
    setupEventListeners() {
        // Mouse movement tracking
        const mouseMoveHandler = (e) => {
            this.metrics.mouseMovements++;
            this.lastInteraction = Date.now();
            this.updateInteractionScore();
        };
        document.addEventListener('mousemove', mouseMoveHandler);
        this.eventListeners.push(['mousemove', mouseMoveHandler]);
        
        // Click tracking
        const clickHandler = (e) => {
            this.metrics.clicks++;
            this.lastInteraction = Date.now();
            this.updateInteractionScore();
            
            // Analyze click patterns for engagement signals
            this.analyzeClickPattern(e);
        };
        document.addEventListener('click', clickHandler);
        this.eventListeners.push(['click', clickHandler]);
        
        // Scroll tracking
        const scrollHandler = (e) => {
            this.metrics.scrollEvents++;
            this.lastInteraction = Date.now();
            this.analyzeScrollBehavior();
        };
        window.addEventListener('scroll', scrollHandler);
        this.eventListeners.push(['scroll', scrollHandler]);
        
        // Focus/blur detection
        const focusHandler = () => {
            this.isPageFocused = true;
            this.focusStartTime = Date.now();
            this.log('📝 Page focused');
        };
        window.addEventListener('focus', focusHandler);
        this.eventListeners.push(['focus', focusHandler]);
        
        const blurHandler = () => {
            this.isPageFocused = false;
            if (this.focusStartTime) {
                this.metrics.focusTime += Date.now() - this.focusStartTime;
            }
            this.log('😴 Page blurred');
        };
        window.addEventListener('blur', blurHandler);
        this.eventListeners.push(['blur', blurHandler]);
        
        // Keyboard interactions
        const keyHandler = (e) => {
            this.lastInteraction = Date.now();
            this.analyzeKeyboardBehavior(e);
        };
        document.addEventListener('keydown', keyHandler);
        this.eventListeners.push(['keydown', keyHandler]);
        
        // Form interactions (if present)
        this.setupFormTracking();
        
        // Video/audio interactions (if present)
        this.setupMediaTracking();
    }
    
    setupFormTracking() {
        const forms = document.querySelectorAll('form, input, textarea, select');
        forms.forEach(element => {
            const changeHandler = (e) => {
                this.lastInteraction = Date.now();
                this.analyzeFormInteraction(e);
            };
            
            element.addEventListener('change', changeHandler);
            element.addEventListener('input', changeHandler);
        });
    }
    
    setupMediaTracking() {
        const mediaElements = document.querySelectorAll('video, audio');
        mediaElements.forEach(element => {
            // Track play/pause events
            element.addEventListener('play', () => {
                this.log('▶️ Media started playing');
                this.metrics.masteryIndicators++;
            });
            
            element.addEventListener('pause', () => {
                this.log('⏸️ Media paused');
            });
            
            // Track seeking behavior (confusion indicator)
            element.addEventListener('seeking', () => {
                this.metrics.confusionIndicators++;
                this.log('🔍 Media seeking (possible confusion)');
            });
        });
    }
    
    connectWebSocket() {
        const wsUrl = `${this.config.websocketEndpoint}/ws/${this.config.studentId}/${this.config.sessionId}`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                this.log('🔗 WebSocket connected');
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.websocket.onerror = (error) => {
                this.log('❌ WebSocket error:', error);
            };
            
            this.websocket.onclose = () => {
                this.log('🔌 WebSocket disconnected');
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };
        } catch (error) {
            this.log('❌ WebSocket connection failed:', error);
        }
    }
    
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'connection_established':
                this.log('✅ Connection established with server');
                break;
                
            case 'experience_generated':
                this.experienceId = data.experience.experience_id;
                this.log(`📚 New experience assigned: ${this.experienceId}`);
                break;
                
            case 'experience_adapted':
                this.log(`⚡ Experience adapted: ${data.adaptation.reasoning}`);
                this.showAdaptationNotification(data.adaptation);
                break;
                
            case 'error':
                this.log('❌ Server error:', data.message);
                break;
        }
    }
    
    startTracking() {
        this.isActive = true;
        
        const trackingLoop = () => {
            if (!this.isActive) return;
            
            this.updateMetrics();
            this.checkForAdaptationTriggers();
            this.sendMetricsToAPI();
            
            setTimeout(trackingLoop, this.config.trackingInterval);
        };
        
        trackingLoop();
    }
    
    updateMetrics() {
        const now = Date.now();
        
        // Update time metrics
        this.metrics.timeOnPage = now - this.startTime;
        if (this.isPageFocused && this.focusStartTime) {
            this.metrics.focusTime += now - this.focusStartTime;
            this.focusStartTime = now;
        } else if (!this.isPageFocused) {
            this.metrics.unfocusedTime = this.metrics.timeOnPage - this.metrics.focusTime;
        }
        
        // Calculate engagement level
        this.calculateEngagementLevel();
        
        this.log('📊 Metrics updated:', this.getEngagementSummary());
    }
    
    updateInteractionScore() {
        const timeSinceLastInteraction = Date.now() - this.lastInteraction;
        const maxIdleTime = 30000; // 30 seconds
        
        // Decay interaction score over time
        const decayFactor = Math.max(0, 1 - (timeSinceLastInteraction / maxIdleTime));
        this.metrics.interactionScore = Math.min(1, this.metrics.interactionScore * 0.95 + 0.1 * decayFactor);
    }
    
    calculateEngagementLevel() {
        // Weighted engagement calculation
        const weights = {
            interaction: 0.3,
            focus: 0.25,
            activity: 0.25,
            time: 0.2
        };
        
        // Interaction component (mouse, clicks, keyboard)
        const interactionComponent = Math.min(1, this.metrics.interactionScore);
        
        // Focus component (time focused vs total time)
        const focusRatio = this.metrics.timeOnPage > 0 ? 
            this.metrics.focusTime / this.metrics.timeOnPage : 0;
        const focusComponent = Math.min(1, focusRatio);
        
        // Activity component (scrolls, clicks per minute)
        const minutesOnPage = this.metrics.timeOnPage / 60000;
        const activityRate = minutesOnPage > 0 ? 
            (this.metrics.clicks + this.metrics.scrollEvents) / minutesOnPage : 0;
        const activityComponent = Math.min(1, activityRate / 10); // Normalize to 10 interactions per minute
        
        // Time component (reasonable time spent)
        const timeComponent = Math.min(1, minutesOnPage / 10); // Normalize to 10 minutes
        
        // Calculate weighted engagement
        this.metrics.engagementLevel = 
            weights.interaction * interactionComponent +
            weights.focus * focusComponent +
            weights.activity * activityComponent +
            weights.time * timeComponent;
        
        // Apply confusion/mastery adjustments
        if (this.metrics.confusionIndicators > 3) {
            this.metrics.engagementLevel *= 0.8; // Reduce engagement if confused
        }
        if (this.metrics.masteryIndicators > 2) {
            this.metrics.engagementLevel = Math.min(1, this.metrics.engagementLevel * 1.2); // Boost if showing mastery
        }
        
        this.metrics.engagementLevel = Math.max(0, Math.min(1, this.metrics.engagementLevel));
    }
    
    checkForAdaptationTriggers() {
        const triggers = [];
        
        // Low engagement trigger
        if (this.metrics.engagementLevel < this.config.adaptationThreshold) {
            triggers.push({
                type: 'engagement_drop',
                confidence: 1 - this.metrics.engagementLevel,
                context: {
                    current_engagement: this.metrics.engagementLevel,
                    focus_ratio: this.metrics.focusTime / this.metrics.timeOnPage
                }
            });
        }
        
        // Confusion trigger
        if (this.metrics.confusionIndicators > 3) {
            triggers.push({
                type: 'confusion_detected',
                confidence: Math.min(1, this.metrics.confusionIndicators / 5),
                context: {
                    confusion_signals: this.metrics.confusionIndicators,
                    engagement_level: this.metrics.engagementLevel
                }
            });
        }
        
        // Mastery trigger
        if (this.metrics.masteryIndicators > 2 && this.metrics.engagementLevel > 0.8) {
            triggers.push({
                type: 'mastery_achieved',
                confidence: this.metrics.engagementLevel,
                context: {
                    mastery_signals: this.metrics.masteryIndicators,
                    high_engagement: this.metrics.engagementLevel
                }
            });
        }
        
        // Send triggers to API
        triggers.forEach(trigger => this.sendAdaptationTrigger(trigger));
    }
    
    async sendAdaptationTrigger(trigger) {
        if (!this.experienceId) return;
        
        this.log(`🔔 Sending adaptation trigger: ${trigger.type}`);
        
        // Send via WebSocket if available
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify({
                type: 'trigger_adaptation',
                experience_id: this.experienceId,
                trigger: trigger
            }));
        }
        
        // Also send via HTTP API as backup
        try {
            const response = await fetch(`${this.config.apiEndpoint}/adapt/${this.experienceId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(trigger)
            });
            
            if (response.ok) {
                const adaptation = await response.json();
                this.log(`⚡ Adaptation response: ${adaptation.reasoning}`);
            }
        } catch (error) {
            this.log('❌ Failed to send adaptation trigger:', error);
        }
    }
    
    async sendMetricsToAPI() {
        const metricsData = {
            student_id: this.config.studentId,
            session_id: this.config.sessionId,
            experience_id: this.experienceId,
            timestamp: new Date().toISOString(),
            metrics: this.metrics,
            browser_info: {
                user_agent: navigator.userAgent,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                },
                url: window.location.href
            }
        };
        
        // Only send to API, don't duplicate WebSocket traffic
        if (this.config.debugMode) {
            this.log('📊 Sending metrics:', metricsData);
        }
    }
    
    analyzeClickPattern(event) {
        // Analyze click location and frequency for engagement signals
        const target = event.target;
        
        if (target.tagName === 'A' || target.tagName === 'BUTTON') {
            this.metrics.masteryIndicators++;
            this.log('🎯 Productive click detected');
        }
        
        // Rapid clicking might indicate frustration
        const now = Date.now();
        if (!this.lastClickTime) {
            this.lastClickTime = now;
        } else if (now - this.lastClickTime < 500) {
            this.metrics.confusionIndicators++;
            this.log('😤 Rapid clicking (possible frustration)');
        }
        this.lastClickTime = now;
    }
    
    analyzeScrollBehavior() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const documentHeight = document.documentElement.scrollHeight;
        const windowHeight = window.innerHeight;
        
        const scrollPercentage = scrollTop / (documentHeight - windowHeight);
        
        if (!this.lastScrollPercentage) {
            this.lastScrollPercentage = scrollPercentage;
            return;
        }
        
        const scrollDiff = Math.abs(scrollPercentage - this.lastScrollPercentage);
        
        // Large scroll jumps might indicate seeking behavior (confusion)
        if (scrollDiff > 0.3) {
            this.metrics.confusionIndicators++;
            this.log('🔍 Large scroll jump (possible seeking)');
        }
        
        // Steady scrolling indicates engagement
        if (scrollDiff > 0.01 && scrollDiff < 0.1) {
            this.metrics.masteryIndicators++;
        }
        
        this.lastScrollPercentage = scrollPercentage;
    }
    
    analyzeKeyboardBehavior(event) {
        // Analyze keyboard patterns for engagement signals
        if (event.key === 'Tab') {
            this.metrics.masteryIndicators++; // Navigation suggests engagement
        }
        
        if (event.ctrlKey && (event.key === 'f' || event.key === 'F')) {
            this.metrics.confusionIndicators++; // Search might indicate confusion
            this.log('🔍 Search initiated (possible confusion)');
        }
        
        if (event.key === 'F5' || (event.ctrlKey && event.key === 'r')) {
            this.metrics.confusionIndicators++; // Refresh might indicate frustration
            this.log('🔄 Page refresh (possible frustration)');
        }
    }
    
    analyzeFormInteraction(event) {
        const target = event.target;
        
        if (target.type === 'text' || target.tagName === 'TEXTAREA') {
            this.metrics.masteryIndicators++; // Text input suggests engagement
        }
        
        if (target.type === 'submit') {
            this.metrics.masteryIndicators += 2; // Form submission is strong engagement signal
        }
    }
    
    showAdaptationNotification(adaptation) {
        // Create a subtle notification for adaptations
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2c3e50;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            max-width: 300px;
            animation: slideIn 0.3s ease-out;
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center;">
                <span style="margin-right: 8px;">⚡</span>
                <div>
                    <strong>Experience Adapted</strong><br>
                    <small>${adaptation.reasoning}</small>
                </div>
            </div>
        `;
        
        // Add animation styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Remove notification after 4 seconds
        setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }
    
    getEngagementSummary() {
        return {
            engagement: Math.round(this.metrics.engagementLevel * 100) + '%',
            interactions: this.metrics.clicks + this.metrics.mouseMovements,
            focus_time: Math.round(this.metrics.focusTime / 1000) + 's',
            time_on_page: Math.round(this.metrics.timeOnPage / 1000) + 's'
        };
    }
    
    stop() {
        this.isActive = false;
        
        // Remove event listeners
        this.eventListeners.forEach(([event, handler]) => {
            document.removeEventListener(event, handler);
        });
        
        // Close WebSocket
        if (this.websocket) {
            this.websocket.close();
        }
        
        this.log('🛑 Engagement tracking stopped');
    }
    
    log(...args) {
        if (this.config.debugMode) {
            console.log('[PACT Engagement]', ...args);
        }
    }
    
    // Public API methods
    getMetrics() {
        return { ...this.metrics };
    }
    
    setExperienceId(experienceId) {
        this.experienceId = experienceId;
        this.log(`📚 Experience ID set: ${experienceId}`);
    }
    
    triggerManualAdaptation(triggerType, confidence = 0.8) {
        this.sendAdaptationTrigger({
            type: triggerType,
            confidence: confidence,
            context: { manual_trigger: true }
        });
    }
}

// Auto-initialize if config is provided
if (typeof window !== 'undefined' && window.PACTConfig) {
    window.pactTracker = new PACTEngagementTracker(window.PACTConfig);
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PACTEngagementTracker;
}

// Example usage:
/*
// Basic initialization
const tracker = new PACTEngagementTracker({
    studentId: 'student_123',
    apiEndpoint: 'http://localhost:8000',
    debugMode: true
});

// Set experience when it's generated
tracker.setExperienceId('experience_abc123');

// Manual trigger (for testing)
tracker.triggerManualAdaptation('confusion_detected');

// Get current metrics
console.log(tracker.getMetrics());

// Stop tracking
tracker.stop();
*/
