// integration_engine/components/session_manager.js
// Session Manager - Orchestrating magical learning journeys! 🎭✨

const EventEmitter = require('events');
const { v4: uuidv4 } = require('uuid');
const logger = require('../utils/logger');

class SessionManager extends EventEmitter {
  constructor(integrationServer) {
    super();
    this.server = integrationServer;
    this.config = integrationServer.config;
    
    // Session storage - where learning adventures live! 🏰
    this.activeSessions = new Map();
    this.sessionHistory = new Map();
    this.studentSessions = new Map(); // studentId -> Set of sessionIds
    
    // Session timeouts and cleanup
    this.sessionTimeouts = new Map();
    this.cleanupInterval = null;
    
    // Joy and celebration tracking
    this.sessionJoyMoments = new Map();
    this.celebrationQueue = [];
    
    this.startSessionCleanup();
    logger.info('🎭 Session Manager initialized - ready to orchestrate learning magic!');
  }

  async createSession(sessionData) {
    const {
      studentId,
      classId,
      teacherId,
      learningObjective,
      subject,
      timeLimit = 30, // Default 30 minutes
      personalizedApproach = 'adaptive',
      joyGoal = 'maximum' // Because why not aim for maximum joy! 🎉
    } = sessionData;

    // Generate magical session ID
    const sessionId = this.generateMagicalSessionId();

    logger.session(sessionId, 'creating', {
      studentId,
      classId,
      teacherId,
      learningObjective,
      subject,
      joyGoal
    });

    try {
      // Get student's learning profile and history
      const studentProfile = await this.getStudentLearningProfile(studentId);
      const sessionHistory = await this.getStudentSessionHistory(studentId);

      // Create the session with extra magical properties ✨
      const session = {
        // Basic session info
        sessionId,
        studentId,
        classId,
        teacherId,
        learningObjective,
        subject,
        
        // Timing and lifecycle
        startTime: new Date(),
        timeLimit: timeLimit * 60000, // Convert to milliseconds
        estimatedEndTime: new Date(Date.now() + (timeLimit * 60000)),
        status: 'initializing',
        
        // Joy and engagement tracking
        joyGoal,
        currentJoyLevel: 0.5, // Start neutral, build up! 🌟
        joyMoments: [],
        celebrationCount: 0,
        breakthroughMoments: [],
        
        // Learning progress
        learningMilestones: [],
        adaptationHistory: [],
        interactionCount: 0,
        
        // Personalization
        personalizedApproach,
        studentProfile,
        sessionContext: {
          isFirstTimeStudent: sessionHistory.length === 0,
          previousSessionCount: sessionHistory.length,
          preferredLearningStyle: studentProfile?.preferredStyle || 'mixed',
          currentEnergyLevel: 'fresh', // fresh, focused, tired, excited
          socialContext: 'individual' // individual, small_group, whole_class
        },
        
        // Technical tracking
        componentInteractions: {},
        dataSnapshots: [],
        performanceMetrics: {
          responseTime: [],
          adaptationSpeed: [],
          systemHealth: []
        },
        
        // Metadata
        metadata: {
          createdBy: 'session_manager',
          version: '1.0.0',
          magicLevel: 'enchanted' // Because every session is magical! ✨
        }
      };

      // Store the session
      this.activeSessions.set(sessionId, session);
      
      // Track student sessions
      if (!this.studentSessions.has(studentId)) {
        this.studentSessions.set(studentId, new Set());
      }
      this.studentSessions.get(studentId).add(sessionId);

      // Set up session timeout
      this.setupSessionTimeout(sessionId);

      // Initialize joy moment tracking
      this.sessionJoyMoments.set(sessionId, []);

      // Request initial learning experience from orchestrator
      const initialExperience = await this.requestInitialExperience(session);
      session.currentExperience = initialExperience;
      session.status = 'active';

      // Notify all components of new session magic! 🎊
      await this.notifyComponentsOfNewSession(session);

      // Emit session created event
      this.emit('session_created', session);

      logger.session(sessionId, 'created', {
        studentId,
        learningObjective,
        experienceTitle: initialExperience?.title,
        magicInitialized: true,
        joyGoal
      });

      // Add welcome joy moment
      this.recordJoyMoment(sessionId, {
        type: 'session_welcome',
        message: `🌟 Welcome to your ${subject} adventure! Let's discover amazing things together!`,
        joyImpact: 0.2
      });

      return {
        sessionId,
        sessionData: session,
        initialExperience,
        welcomeMessage: this.generateWelcomeMessage(session),
        joyfulStart: true
      };

    } catch (error) {
      logger.error('Session creation failed', {
        sessionId,
        studentId,
        error: error.message
      });

      // Clean up failed session
      this.cleanupFailedSession(sessionId);
      
      throw new Error(`Could not create learning session: ${error.message}`);
    }
  }

  async getSessionDetails(sessionId) {
    const session = this.activeSessions.get(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found - it might have completed its magical journey! ✨`);
    }

    // Calculate dynamic session metrics
    const currentTime = Date.now();
    const sessionDuration = currentTime - session.startTime.getTime();
    const timeRemaining = Math.max(0, session.timeLimit - sessionDuration);
    const progressPercentage = Math.min(100, (sessionDuration / session.timeLimit) * 100);

    // Get latest joy and engagement data
    const latestJoyMoments = this.sessionJoyMoments.get(sessionId) || [];
    const recentJoy = latestJoyMoments.slice(-5); // Last 5 joy moments

    return {
      sessionId,
      basicInfo: {
        studentId: session.studentId,
        subject: session.subject,
        learningObjective: session.learningObjective,
        status: session.status
      },
      
      timing: {
        startTime: session.startTime,
        duration: sessionDuration,
        timeRemaining,
        progressPercentage,
        estimatedEndTime: session.estimatedEndTime
      },
      
      joyMetrics: {
        currentJoyLevel: session.currentJoyLevel,
        joyGoal: session.joyGoal,
        celebrationCount: session.celebrationCount,
        totalJoyMoments: latestJoyMoments.length,
        recentJoyMoments: recentJoy,
        breakthroughCount: session.breakthroughMoments.length
      },
      
      learningProgress: {
        milestonesReached: session.learningMilestones.length,
        adaptationsApplied: session.adaptationHistory.length,
        interactionCount: session.interactionCount,
        currentExperience: session.currentExperience
      },
      
      liveInsights: {
        energyLevel: this.assessCurrentEnergyLevel(session),
        engagementTrend: this.calculateEngagementTrend(session),
        recommendedActions: this.generateLiveRecommendations(session)
      }
    };
  }

  async updateSession(sessionId, updateData) {
    const session = this.activeSessions.get(sessionId);
    if (!session) {
      throw new Error(`Cannot update session ${sessionId} - session not found`);
    }

    logger.session(sessionId, 'updating', {
      updateFields: Object.keys(updateData),
      previousStatus: session.status
    });

    // Apply updates
    Object.entries(updateData).forEach(([key, value]) => {
      if (key === 'metadata') {
        session.metadata = { ...session.metadata, ...value };
      } else if (key === 'sessionContext') {
        session.sessionContext = { ...session.sessionContext, ...value };
      } else {
        session[key] = value;
      }
    });

    // Update timestamp
    session.lastUpdated = new Date();

    // Check for joy-worthy updates
    if (updateData.currentJoyLevel && updateData.currentJoyLevel > session.currentJoyLevel) {
      this.recordJoyMoment(sessionId, {
        type: 'joy_increase',
        message: `🎉 Joy level increased to ${Math.round(updateData.currentJoyLevel * 100)}%!`,
        joyImpact: updateData.currentJoyLevel - session.currentJoyLevel
      });
    }

    // Emit update event
    this.emit('session_updated', { sessionId, session, updates: updateData });

    return session;
  }

  async endSession(sessionId, reason = 'completed') {
    const session = this.activeSessions.get(sessionId);
    if (!session) {
      logger.warn(`Attempted to end non-existent session: ${sessionId}`);
      return null;
    }

    logger.session(sessionId, 'ending', {
      reason,
      duration: Date.now() - session.startTime.getTime(),
      joyLevel: session.currentJoyLevel,
      celebrationCount: session.celebrationCount
    });

    try {
      // Calculate final session metrics
      const endTime = new Date();
      const totalDuration = endTime.getTime() - session.startTime.getTime();
      
      // Generate session summary with extra joy! ✨
      const sessionSummary = await this.generateJoyfulSessionSummary(session, reason, totalDuration);

      // Update session with completion data
      session.endTime = endTime;
      session.totalDuration = totalDuration;
      session.endReason = reason;
      session.status = 'completed';
      session.summary = sessionSummary;

      // Record final joy moment
      this.recordJoyMoment(sessionId, {
        type: 'session_completion',
        message: sessionSummary.celebrationMessage,
        joyImpact: 0.1
      });

      // Notify components of session end
      await this.notifyComponentsOfSessionEnd(session, sessionSummary);

      // Clear session timeout
      if (this.sessionTimeouts.has(sessionId)) {
        clearTimeout(this.sessionTimeouts.get(sessionId));
        this.sessionTimeouts.delete(sessionId);
      }

      // Move to history
      this.sessionHistory.set(sessionId, session);
      this.activeSessions.delete(sessionId);

      // Clean up student session tracking
      if (this.studentSessions.has(session.studentId)) {
        this.studentSessions.get(session.studentId).delete(sessionId);
      }

      // Clean up joy moments
      this.sessionJoyMoments.delete(sessionId);

      // Emit completion event
      this.emit('session_completed', { sessionId, session, summary: sessionSummary });

      logger.session(sessionId, 'completed', {
        reason,
        finalJoyLevel: session.currentJoyLevel,
        outcome: sessionSummary.outcome,
        memorable: sessionSummary.memorableMoments.length > 0
      });

      return sessionSummary;

    } catch (error) {
      logger.error('Session ending failed', {
        sessionId,
        error: error.message
      });
      throw error;
    }
  }

  recordJoyMoment(sessionId, joyMomentData) {
    const session = this.activeSessions.get(sessionId);
    if (!session) return;

    const joyMoment = {
      timestamp: new Date(),
      sessionId,
      ...joyMomentData
    };

    // Add to session
    session.joyMoments.push(joyMoment);

    // Add to session joy tracking
    const sessionJoyMoments = this.sessionJoyMoments.get(sessionId) || [];
    sessionJoyMoments.push(joyMoment);
    this.sessionJoyMoments.set(sessionId, sessionJoyMoments);

    // Update session joy level
    if (joyMomentData.joyImpact) {
      session.currentJoyLevel = Math.min(1.0, 
        session.currentJoyLevel + joyMomentData.joyImpact
      );
    }

    // Check for celebration triggers
    if (joyMoment.type === 'breakthrough' || session.currentJoyLevel > 0.8) {
      this.triggerCelebration(sessionId, joyMoment);
    }

    logger.pactEvent('joy_moment', {
      sessionId,
      studentId: session.studentId,
      joyType: joyMoment.type,
      joyLevel: session.currentJoyLevel,
      message: joyMoment.message
    });
  }

  triggerCelebration(sessionId, triggerMoment) {
    const session = this.activeSessions.get(sessionId);
    if (!session) return;

    session.celebrationCount++;

    const celebration = {
      sessionId,
      studentId: session.studentId,
      timestamp: new Date(),
      trigger: triggerMoment,
      celebrationLevel: session.currentJoyLevel > 0.9 ? 'epic' : 'wonderful',
      message: `🎊 Celebration #${session.celebrationCount} for ${session.studentId}! 🎊`
    };

    this.celebrationQueue.push(celebration);

    // Notify components to join the celebration!
    this.server.io.emit('celebration_time', celebration);

    logger.pactEvent('celebration_triggered', celebration);
  }

  async requestInitialExperience(session) {
    try {
      // Request from orchestrator
      if (this.server.orchestrator) {
        return await this.server.orchestrator.orchestratePersonalizedLearning(
          session.studentId,
          session.learningObjective,
          session.sessionContext
        );
      }

      // Fallback: create basic experience
      return this.createFallbackExperience(session);

    } catch (error) {
      logger.warn('Failed to get initial experience from orchestrator, using fallback', {
        sessionId: session.sessionId,
        error: error.message
      });
      return this.createFallbackExperience(session);
    }
  }

  createFallbackExperience(session) {
    const subjects = {
      math: { emoji: '🔢', adventure: 'Mathematical Quest' },
      science: { emoji: '🔬', adventure: 'Scientific Discovery' },
      reading: { emoji: '📚', adventure: 'Literary Journey' },
      history: { emoji: '🏛️', adventure: 'Time Travel Adventure' },
      art: { emoji: '🎨', adventure: 'Creative Expression' }
    };

    const subjectInfo = subjects[session.subject?.toLowerCase()] || 
                       { emoji: '✨', adventure: 'Learning Adventure' };

    return {
      title: `${subjectInfo.emoji} ${session.studentId}'s ${subjectInfo.adventure}`,
      description: `Let's explore ${session.learningObjective} together!`,
      type: 'adaptive_exploration',
      estimatedDuration: session.timeLimit / 60000, // Convert to minutes
      joyFactor: 'high',
      activities: [
        {
          name: 'Welcome & Discovery',
          type: 'interactive_introduction',
          duration: 5
        },
        {
          name: 'Guided Exploration',
          type: 'adaptive_learning',
          duration: 20
        },
        {
          name: 'Celebration & Reflection',
          type: 'joyful_conclusion',
          duration: 5
        }
      ]
    };
  }

  async generateJoyfulSessionSummary(session, endReason, totalDuration) {
    const joyMoments = this.sessionJoyMoments.get(session.sessionId) || [];
    const finalJoyLevel = session.currentJoyLevel;

    // Determine outcome based on joy and engagement
    let outcome = 'satisfactory';
    let celebrationMessage = '🌟 Great job completing your learning session!';

    if (finalJoyLevel > 0.8 && session.celebrationCount > 2) {
      outcome = 'magical';
      celebrationMessage = '🎉 What an AMAZING learning adventure! You were absolutely brilliant!';
    } else if (finalJoyLevel > 0.6) {
      outcome = 'wonderful';
      celebrationMessage = '✨ You did fantastic work today! So much discovery and growth!';
    } else if (finalJoyLevel > 0.4) {
      outcome = 'good';
      celebrationMessage = '👏 Nice work on your learning journey today!';
    }

    // Find memorable moments
    const memorableMoments = joyMoments
      .filter(moment => moment.type === 'breakthrough' || moment.joyImpact > 0.15)
      .map(moment => ({
        timestamp: moment.timestamp,
        description: moment.message,
        joyImpact: moment.joyImpact
      }));

    // Calculate learning metrics
    const learningMetrics = {
      sessionDuration: Math.round(totalDuration / 60000), // minutes
      interactionCount: session.interactionCount,
      adaptationsApplied: session.adaptationHistory.length,
      joyMomentsExperienced: joyMoments.length,
      celebrationsTriggered: session.celebrationCount,
      finalJoyLevel: Math.round(finalJoyLevel * 100),
      milestonesAchieved: session.learningMilestones.length
    };

    // Generate insights and recommendations
    const insights = this.generateSessionInsights(session, joyMoments, finalJoyLevel);
    const futureRecommendations = this.generateFutureRecommendations(session, outcome);

    return {
      sessionId: session.sessionId,
      studentId: session.studentId,
      subject: session.subject,
      learningObjective: session.learningObjective,
      outcome,
      celebrationMessage,
      learningMetrics,
      memorableMoments,
      insights,
      futureRecommendations,
      endReason,
      completedAt: new Date(),
      joyfulConclusion: true
    };
  }

  generateSessionInsights(session, joyMoments, finalJoyLevel) {
    const insights = [];

    // Joy pattern analysis
    if (joyMoments.length > 5) {
      insights.push('🎊 This student experienced many joyful learning moments!');
    }

    // Engagement pattern analysis
    if (session.adaptationHistory.length === 0) {
      insights.push('✨ No adaptations needed - student was perfectly engaged throughout!');
    } else if (session.adaptationHistory.length > 3) {
      insights.push('🔄 Student benefited from personalized adaptations to stay engaged');
    }

    // Celebration analysis
    if (session.celebrationCount > 3) {
      insights.push('🎉 Multiple celebration moments - this was a breakthrough session!');
    }

    // Final joy analysis
    if (finalJoyLevel > 0.8) {
      insights.push('🚀 Ended on a high note with excellent joy and engagement!');
    } else if (finalJoyLevel < 0.4) {
      insights.push('💝 Student may benefit from different approaches next time');
    }

    return insights;
  }

  generateFutureRecommendations(session, outcome) {
    const recommendations = [];

    // Based on outcome
    if (outcome === 'magical') {
      recommendations.push('🌟 Student is ready for more challenging content');
      recommendations.push('👥 Consider peer collaboration or leadership opportunities');
    } else if (outcome === 'good' || outcome === 'wonderful') {
      recommendations.push('✨ Continue with similar approaches - they work well for this student');
      recommendations.push('🎯 Gradually introduce more interactive elements');
    } else {
      recommendations.push('💝 Try more kinesthetic or hands-on approaches next time');
      recommendations.push('🤝 Consider shorter sessions with more frequent breaks');
    }

    // Based on learning patterns
    if (session.adaptationHistory.length > 2) {
      const adaptationTypes = session.adaptationHistory.map(a => a.type);
      const mostCommon = this.getMostFrequent(adaptationTypes);
      if (mostCommon === 'engagement') {
        recommendations.push('🎪 Pre-plan more engaging activities from the start');
      }
    }

    return recommendations;
  }

  getMostFrequent(array) {
    if (array.length === 0) return null;
    const frequency = {};
    array.forEach(item => frequency[item] = (frequency[item] || 0) + 1);
    return Object.keys(frequency).reduce((a, b) => frequency[a] > frequency[b] ? a : b);
  }

  async notifyComponentsOfNewSession(session) {
    const notification = {
      type: 'session_started',
      sessionId: session.sessionId,
      studentId: session.studentId,
      learningObjective: session.learningObjective,
      joyGoal: session.joyGoal,
      welcomeMessage: `🎊 New learning adventure starting for ${session.studentId}! 🎊`
    };

    this.server.io.emit('session_notification', notification);
    
    logger.pactEvent('session_started_notification', {
      sessionId: session.sessionId,
      studentId: session.studentId,
      componentsNotified: this.server.componentRegistry.getRegisteredComponents().length
    });
  }

  async notifyComponentsOfSessionEnd(session, summary) {
    const notification = {
      type: 'session_completed',
      sessionId: session.sessionId,
      studentId: session.studentId,
      summary: summary,
      celebrationMessage: summary.celebrationMessage
    };

    this.server.io.emit('session_notification', notification);
    
    logger.pactEvent('session_completed_notification', {
      sessionId: session.sessionId,
      outcome: summary.outcome,
      componentsNotified: this.server.componentRegistry.getRegisteredComponents().length
    });
  }

  setupSessionTimeout(sessionId) {
    const session = this.activeSessions.get(sessionId);
    if (!session) return;

    const timeoutHandler = setTimeout(async () => {
      logger.session(sessionId, 'timeout', {
        plannedDuration: session.timeLimit,
        actualDuration: Date.now() - session.startTime.getTime()
      });

      await this.endSession(sessionId, 'timeout');
    }, session.timeLimit);

    this.sessionTimeouts.set(sessionId, timeoutHandler);
  }

  cleanupFailedSession(sessionId) {
    this.activeSessions.delete(sessionId);
    this.sessionJoyMoments.delete(sessionId);
    
    if (this.sessionTimeouts.has(sessionId)) {
      clearTimeout(this.sessionTimeouts.get(sessionId));
      this.sessionTimeouts.delete(sessionId);
    }
  }

  generateWelcomeMessage(session) {
    const welcomeMessages = [
      `🌟 Welcome to your ${session.subject} adventure, ${session.studentId}! Let's discover amazing things together!`,
      `🚀 Ready for an exciting learning journey? Your ${session.subject} quest begins now!`,
      `✨ Hello ${session.studentId}! I'm excited to explore ${session.subject} with you today!`,
      `🎉 Let's make today's ${session.subject} session absolutely magical!`
    ];

    return welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
  }

  generateMagicalSessionId() {
    const adjectives = ['magical', 'wonderful', 'brilliant', 'amazing', 'fantastic', 'incredible'];
    const nouns = ['adventure', 'journey', 'quest', 'discovery', 'exploration', 'experience'];
    
    const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
    const noun = nouns[Math.floor(Math.random() * nouns.length)];
    const timestamp = Date.now().toString(36);
    
    return `${adjective}-${noun}-${timestamp}`;
  }

  // Utility methods for session analysis
  assessCurrentEnergyLevel(session) {
    const sessionDuration = Date.now() - session.startTime.getTime();
    const joyLevel = session.currentJoyLevel;
    
    if (sessionDuration < 600000) { // First 10 minutes
      return joyLevel > 0.7 ? 'energetic' : 'warming_up';
    } else if (sessionDuration < 1200000) { // 10-20 minutes
      return joyLevel > 0.6 ? 'focused' : 'needs_boost';
    } else {
      return joyLevel > 0.5 ? 'sustained' : 'tired';
    }
  }

  calculateEngagementTrend(session) {
    const joyMoments = session.joyMoments.slice(-5); // Last 5 moments
    if (joyMoments.length < 2) return 'stable';

    const recentTrend = joyMoments.reduce((sum, moment, index) => {
      return sum + moment.joyImpact * (index + 1); // Weight recent moments more
    }, 0);

    if (recentTrend > 0.2) return 'rising';
    if (recentTrend < -0.1) return 'declining';
    return 'stable';
  }

  generateLiveRecommendations(session) {
    const recommendations = [];
    const energyLevel = this.assessCurrentEnergyLevel(session);
    const trend = this.calculateEngagementTrend(session);

    if (energyLevel === 'tired') {
      recommendations.push('💪 Consider a fun brain break or energizing activity');
    }

    if (trend === 'declining') {
      recommendations.push('🎪 Time for a creative change of pace!');
    }

    if (session.currentJoyLevel > 0.8) {
      recommendations.push('🚀 Perfect moment to introduce more challenging content!');
    }

    return recommendations;
  }

  // Public API methods
  getActiveSessions() {
    return Array.from(this.activeSessions.values());
  }

  getSessionsOverview() {
    return {
      active: this.activeSessions.size,
      completed: this.sessionHistory.size,
      totalCelebrations: Array.from(this.activeSessions.values())
        .reduce((sum, session) => sum + session.celebrationCount, 0),
      averageJoyLevel: this.calculateAverageJoyLevel()
    };
  }

  calculateAverageJoyLevel() {
    const activeSessions = Array.from(this.activeSessions.values());
    if (activeSessions.length === 0) return 0;

    const totalJoy = activeSessions.reduce((sum, session) => sum + session.currentJoyLevel, 0);
    return totalJoy / activeSessions.length;
  }

  async getStudentSessionHistory(studentId) {
    // Get active sessions for this student
    const activeSessions = Array.from(this.activeSessions.values())
      .filter(session => session.studentId === studentId);

    // Get completed sessions from history
    const completedSessions = Array.from(this.sessionHistory.values())
      .filter(session => session.studentId === studentId);

    return [...completedSessions, ...activeSessions]
      .sort((a, b) => new Date(b.startTime) - new Date(a.startTime));
  }

  async getStudentLearningProfile(studentId) {
    try {
      // Try to get from data coordinator
      if (this.server.dataCoordinator) {
        return await this.server.dataCoordinator.getUnifiedStudentProfile(studentId);
      }

      // Fallback: create basic profile
      return this.createBasicStudentProfile(studentId);
    } catch (error) {
      logger.warn('Failed to get student profile, using basic profile', {
        studentId,
        error: error.message
      });
      return this.createBasicStudentProfile(studentId);
    }
  }

  createBasicStudentProfile(studentId) {
    return {
      studentId,
      preferredStyle: 'mixed',
      joyPreferences: ['celebration', 'discovery', 'collaboration'],
      learningHistory: {
        sessionsCompleted: 0,
        averageJoyLevel: 0.5,
        preferredSubjects: []
      }
    };
  }

  getTotalSessionsCount() {
    return this.activeSessions.size + this.sessionHistory.size;
  }

  async closeAllSessions() {
    const activeSessionIds = Array.from(this.activeSessions.keys());
    
    logger.info('🛑 Closing all active sessions gracefully...', {
      sessionsToClose: activeSessionIds.length
    });

    for (const sessionId of activeSessionIds) {
      try {
        await this.endSession(sessionId, 'system_shutdown');
      } catch (error) {
        logger.error('Failed to close session gracefully', {
          sessionId,
          error: error.message
        });
      }
    }

    logger.info('✅ All sessions closed');
  }

  startSessionCleanup() {
    // Clean up old completed sessions every hour
    this.cleanupInterval = setInterval(() => {
      this.cleanupOldSessions();
    }, 3600000); // 1 hour

    logger.info('🧹 Session cleanup monitoring started');
  }

  cleanupOldSessions() {
    const maxHistoryAge = 7 * 24 * 60 * 60 * 1000; // 7 days
    const cutoffTime = Date.now() - maxHistoryAge;
    
    let cleanedCount = 0;

    for (const [sessionId, session] of this.sessionHistory.entries()) {
      if (session.endTime && session.endTime.getTime() < cutoffTime) {
        this.sessionHistory.delete(sessionId);
        cleanedCount++;
      }
    }

    if (cleanedCount > 0) {
      logger.info('🧹 Cleaned up old session history', {
        cleanedSessions: cleanedCount,
        remainingHistory: this.sessionHistory.size
      });
    }
  }

  async shutdown() {
    logger.info('🛑 Session Manager shutting down...');

    // Clear cleanup interval
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
    }

    // Close all active sessions
    await this.closeAllSessions();

    // Clear all timeouts
    for (const timeout of this.sessionTimeouts.values()) {
      clearTimeout(timeout);
    }
    this.sessionTimeouts.clear();

    // Clear data
    this.activeSessions.clear();
    this.studentSessions.clear();
    this.sessionJoyMoments.clear();
    this.celebrationQueue = [];

    logger.info('✅ Session Manager shutdown complete');
  }
}

module.exports = SessionManager;
