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
      await this.notifyComponentsOfSessionEnd(
