// integration_engine/routes/sessions.js
// Session API Routes - RESTful endpoints for magical learning sessions! 🎭✨

const express = require('express');
const { body, param, query, validationResult } = require('express-validator');
const logger = require('../utils/logger');

const router = express.Router();

module.exports = (integrationServer) => {
  const sessionManager = integrationServer.sessionManager;
  const componentRegistry = integrationServer.componentRegistry;

  // Middleware for joy-filled error handling! 🌟
  const handleValidationErrors = (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Oops! We need a bit more info to create the perfect learning experience! ✨',
        errors: errors.array().map(error => ({
          field: error.param,
          message: error.msg,
          value: error.value
        })),
        helpfulHint: 'Check our API docs for the magical parameters needed! 📚'
      });
    }
    next();
  };

  // 🎉 CREATE NEW LEARNING SESSION
  router.post('/',
    [
      body('studentId')
        .notEmpty()
        .withMessage('Every learning adventure needs a hero! Please provide studentId 🌟'),
      body('learningObjective')
        .isLength({ min: 5 })
        .withMessage('Tell us what amazing thing you want to learn! (at least 5 characters) 🎯'),
      body('subject')
        .optional()
        .isIn(['math', 'science', 'reading', 'history', 'art', 'music', 'general'])
        .withMessage('Choose a magical subject realm to explore! 📚'),
      body('timeLimit')
        .optional()
        .isInt({ min: 5, max: 120 })
        .withMessage('Sessions can be 5-120 minutes of pure learning magic! ⏰'),
      body('joyGoal')
        .optional()
        .isIn(['moderate', 'high', 'maximum'])
        .withMessage('How much joy should we aim for? (moderate/high/maximum) 🎊')
    ],
    handleValidationErrors,
    async (req, res) => {
      const startTime = Date.now();
      
      try {
        const {
          studentId,
          classId,
          teacherId,
          learningObjective,
          subject = 'general',
          timeLimit = 30,
          personalizedApproach = 'adaptive',
          joyGoal = 'high'
        } = req.body;

        logger.session('create_request', 'received', {
          studentId,
          learningObjective,
          subject,
          joyGoal,
          requestId: req.headers['x-request-id']
        });

        // Check if system is ready for magical sessions
        if (!componentRegistry.isSystemReady()) {
          const readiness = componentRegistry.getSystemReadiness();
          return res.status(503).json({
            success: false,
            message: '🔧 Our magical system is still warming up! Missing some key components.',
            systemStatus: readiness,
            retryAfter: 30,
            encouragement: 'Great things are worth waiting for! ✨'
          });
        }

        // Create the magical learning session!
        const sessionResult = await sessionManager.createSession({
          studentId,
          classId,
          teacherId,
          learningObjective,
          subject,
          timeLimit,
          personalizedApproach,
          joyGoal
        });

        const responseTime = Date.now() - startTime;
        
        logger.session(sessionResult.sessionId, 'created_successfully', {
          studentId,
          responseTime,
          joyGoal,
          experienceTitle: sessionResult.initialExperience?.title
        });

        res.status(201).json({
          success: true,
          message: `🎉 Magical learning session created for ${studentId}!`,
          session: {
            sessionId: sessionResult.sessionId,
            studentId,
            learningObjective,
            subject,
            timeLimit,
            joyGoal,
            status: 'active',
            startTime: sessionResult.sessionData.startTime,
            estimatedEndTime: sessionResult.sessionData.estimatedEndTime
          },
          initialExperience: sessionResult.initialExperience,
          welcomeMessage: sessionResult.welcomeMessage,
          nextSteps: {
            websocketUrl: `/ws?sessionId=${sessionResult.sessionId}`,
            trackingEnabled: true,
            celebrationMode: 'automatic'
          },
          responseTime,
          magical: true
        });

      } catch (error) {
        const responseTime = Date.now() - startTime;
        
        logger.error('Session creation failed', {
          error: error.message,
          requestBody: req.body,
          responseTime
        });

        res.status(500).json({
          success: false,
          message: '😅 Oops! Our creative magic hit a small snag while creating your session.',
          error: process.env.NODE_ENV === 'development' ? error.message : 'Internal server error',
          suggestion: 'Try again in a moment - sometimes magic needs a second try! ✨',
          supportContact: 'If this keeps happening, let us know! We\'re here to help! 💝'
        });
      }
    }
  );

  // 📊 GET SESSION DETAILS
  router.get('/:sessionId',
    [
      param('sessionId')
        .notEmpty()
        .withMessage('Which magical session would you like to peek into? 🔍')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const { sessionId } = req.params;
        const includeJoyMoments = req.query.includeJoyMoments === 'true';
        const includeLiveInsights = req.query.includeLiveInsights === 'true';

        logger.session(sessionId, 'details_requested', {
          includeJoyMoments,
          includeLiveInsights
        });

        const sessionDetails = await sessionManager.getSessionDetails(sessionId);

        // Add joy moments if requested
        if (includeJoyMoments) {
          sessionDetails.joyMoments = sessionDetails.joyMetrics.recentJoyMoments;
        }

        // Add live insights if requested
        if (includeLiveInsights) {
          sessionDetails.liveRecommendations = sessionDetails.liveInsights.recommendedActions;
        }

        res.json({
          success: true,
          message: `✨ Here are the magical details for session ${sessionId}!`,
          session: sessionDetails,
          systemHealth: componentRegistry.getHealthSummary(),
          delightful: true
        });

      } catch (error) {
        logger.error('Get session details failed', {
          sessionId: req.params.sessionId,
          error: error.message
        });

        if (error.message.includes('not found')) {
          return res.status(404).json({
            success: false,
            message: `🔍 Hmm, we can't find session ${req.params.sessionId}. It might have completed its magical journey!`,
            suggestion: 'Double-check the session ID, or create a new learning adventure! 🚀'
          });
        }

        res.status(500).json({
          success: false,
          message: '😅 Oops! We had trouble fetching those session details.',
          error: process.env.NODE_ENV === 'development' ? error.message : 'Internal server error',
          encouragement: 'Try again! We believe in the magic of persistence! ✨'
        });
      }
    }
  );

  // 🔄 UPDATE SESSION
  router.put('/:sessionId',
    [
      param('sessionId')
        .notEmpty()
        .withMessage('Which session needs a magical update? ✨'),
      body('currentJoyLevel')
        .optional()
        .isFloat({ min: 0, max: 1 })
        .withMessage('Joy level should be between 0 and 1 (we prefer closer to 1! 🌟)'),
      body('status')
        .optional()
        .isIn(['active', 'paused', 'completed'])
        .withMessage('Status should be active, paused, or completed 📋')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const { sessionId } = req.params;
        const updateData = req.body;

        logger.session(sessionId, 'update_requested', {
          updateFields: Object.keys(updateData)
        });

        const updatedSession = await sessionManager.updateSession(sessionId, updateData);

        res.json({
          success: true,
          message: `🎊 Session ${sessionId} updated with magical enhancements!`,
          session: {
            sessionId: updatedSession.sessionId,
            studentId: updatedSession.studentId,
            status: updatedSession.status,
            currentJoyLevel: updatedSession.currentJoyLevel,
            lastUpdated: updatedSession.lastUpdated
          },
          updateApplied: Object.keys(updateData),
          wonderful: true
        });

      } catch (error) {
        logger.error('Session update failed', {
          sessionId: req.params.sessionId,
          updateData: req.body,
          error: error.message
        });

        res.status(500).json({
          success: false,
          message: '😅 We hit a tiny snag updating that session.',
          error: process.env.NODE_ENV === 'development' ? error.message : 'Update failed',
          encouragement: 'The magic is still there - try updating again! ✨'
        });
      }
    }
  );

  // 🏁 END SESSION
  router.post('/:sessionId/end',
    [
      param('sessionId')
        .notEmpty()
        .withMessage('Which magical session should we celebrate and conclude? 🎉'),
      body('reason')
        .optional()
        .isIn(['completed', 'timeout', 'student_request', 'teacher_request', 'system_shutdown'])
        .withMessage('Let us know why this learning adventure is ending! 📝')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const { sessionId } = req.params;
        const { reason = 'completed', feedback } = req.body;

        logger.session(sessionId, 'end_requested', { reason, hasFeedback: !!feedback });

        const sessionSummary = await sessionManager.endSession(sessionId, reason);

        res.json({
          success: true,
          message: `🎊 What a wonderful learning journey! Session ${sessionId} completed with joy!`,
          summary: sessionSummary,
          celebrationMessage: sessionSummary.celebrationMessage,
          achievements: {
            joyMomentsExperienced: sessionSummary.learningMetrics.joyMomentsExperienced,
            celebrationsTriggered: sessionSummary.learningMetrics.celebrationsTriggered,
            finalJoyLevel: sessionSummary.learningMetrics.finalJoyLevel,
            memorableMoments: sessionSummary.memorableMoments.length
          },
          nextSteps: {
            recommendedBreak: '5-10 minutes of celebration time! 🎉',
            futureRecommendations: sessionSummary.futureRecommendations,
            availableForNewSession: true
          },
          magical: true
        });

      } catch (error) {
        logger.error('Session end failed', {
          sessionId: req.params.sessionId,
          reason: req.body.reason,
          error: error.message
        });

        res.status(500).json({
          success: false,
          message: '😅 We had trouble ending that session gracefully.',
          error: process.env.NODE_ENV === 'development' ? error.message : 'End session failed',
          suggestion: 'The session might have already ended, or try again in a moment! ✨'
        });
      }
    }
  );

  // 📋 LIST ACTIVE SESSIONS
  router.get('/',
    [
      query('studentId')
        .optional()
        .notEmpty()
        .withMessage('If filtering by student, provide a valid studentId! 👤'),
      query('classId')
        .optional()
        .notEmpty()
        .withMessage('If filtering by class, provide a valid classId! 🏫'),
      query('status')
        .optional()
        .isIn(['active', 'paused', 'completed', 'all'])
        .withMessage('Status filter can be: active, paused, completed, or all 📊'),
      query('limit')
        .optional()
        .isInt({ min: 1, max: 100 })
        .withMessage('Limit should be between 1-100 sessions 📝'),
      query('offset')
        .optional()
        .isInt({ min: 0 })
        .withMessage('Offset should be 0 or greater 📄')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const {
          studentId,
          classId,
          status = 'active',
          limit = 50,
          offset = 0,
          includeJoyMetrics = 'false'
        } = req.query;

        logger.info('📋 Sessions list requested', {
          filters: { studentId, classId, status },
          pagination: { limit, offset }
        });

        let sessions = [];

        if (status === 'all' || status === 'active') {
          sessions = sessions.concat(sessionManager.getActiveSessions());
        }

        // Apply filters
        if (studentId) {
          sessions = sessions.filter(session => session.studentId === studentId);
        }

        if (classId) {
          sessions = sessions.filter(session => session.classId === classId);
        }

        // Apply pagination
        const totalSessions = sessions.length;
        const paginatedSessions = sessions.slice(offset, offset + parseInt(limit));

        // Format session data
        const formattedSessions = paginatedSessions.map(session => {
          const basicInfo = {
            sessionId: session.sessionId,
            studentId: session.studentId,
            classId: session.classId,
            teacherId: session.teacherId,
            subject: session.subject,
            learningObjective: session.learningObjective,
            status: session.status,
            startTime: session.startTime,
            timeRemaining: Math.max(0, session.timeLimit - (Date.now() - session.startTime.getTime())),
            currentJoyLevel: Math.round(session.currentJoyLevel * 100),
            celebrationCount: session.celebrationCount
          };

          if (includeJoyMetrics === 'true') {
            basicInfo.joyMetrics = {
              joyMoments: session.joyMoments.length,
              recentCelebrations: session.celebrationCount,
              engagementTrend: session.engagementTrend || 'stable'
            };
          }

          return basicInfo;
        });

        // Get system overview
        const systemOverview = {
          totalActiveSessions: sessionManager.getActiveSessions().length,
          systemJoyLevel: Math.round(sessionManager.calculateAverageJoyLevel() * 100),
          componentsHealthy: componentRegistry.getHealthSummary().healthy,
          celebrationMode: 'active'
        };

        res.json({
          success: true,
          message: `✨ Found ${totalSessions} magical learning sessions!`,
          sessions: formattedSessions,
          pagination: {
            total: totalSessions,
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (offset + parseInt(limit)) < totalSessions
          },
          systemOverview,
          filters: { studentId, classId, status },
          delightful: true
        });

      } catch (error) {
        logger.error('List sessions failed', {
          query: req.query,
          error: error.message
        });

        res.status(500).json({
          success: false,
          message: '😅 We had trouble gathering those session details.',
          error: process.env.NODE_ENV === 'development' ? error.message : 'List failed',
          encouragement: 'The sessions are all there - try refreshing! ✨'
        });
      }
    }
  );

  // 🎊 TRIGGER CELEBRATION
  router.post('/:sessionId/celebrate',
    [
      param('sessionId')
        .notEmpty()
        .withMessage('Which session deserves a celebration? 🎉'),
      body('celebrationType')
        .optional()
        .isIn(['achievement', 'breakthrough', 'effort', 'collaboration', 'creativity'])
        .withMessage('What kind of amazing thing should we celebrate? 🌟'),
      body('message')
        .optional()
        .isLength({ max: 200 })
        .withMessage('Celebration message should be 200 characters or less! 💝')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const { sessionId } = req.params;
        const {
          celebrationType = 'achievement',
          message = 'Amazing work! Keep up the fantastic learning! 🌟',
          intensity = 'high'
        } = req.body;

        logger.session(sessionId, 'celebration_triggered', {
          type: celebrationType,
          intensity
        });

        // Record the celebration moment
        sessionManager.recordJoyMoment(sessionId, {
          type: 'manual_celebration',
          celebrationType,
          message,
          joyImpact: 0.2,
          triggeredBy: 'api_request'
        });

        // Trigger system-wide celebration
        sessionManager.triggerCelebration(sessionId, {
          type: celebrationType,
          message,
          intensity,
          timestamp: new Date()
        });

        res.json({
          success: true,
          message: `🎊 Celebration activated for session ${sessionId}!`,
          celebration: {
            type: celebrationType,
            message,
            intensity,
            timestamp: new Date(),
            confettiLevel: 'maximum'
          },
          joyBoost: '🚀 Joy levels rising!',
          sparkles: '✨✨✨'
        });

      } catch (error) {
        logger.error('Celebration trigger failed', {
          sessionId: req.params.sessionId,
          error: error.message
        });

        res.status(500).json({
          success: false,
          message: '😅 Our celebration cannon had a tiny misfire!',
          error: process.env.NODE_ENV === 'development' ? error.message : 'Celebration failed',
          encouragement: 'The joy is still there - try celebrating again! 🎉'
        });
      }
    }
  );

  // 📊 GET SESSION ANALYTICS
  router.get('/:sessionId/analytics',
    [
      param('sessionId')
        .notEmpty()
        .withMessage('Which session\'s magical analytics would you like? 📈')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const { sessionId } = req.params;
        const includeRealTime = req.query.realTime === 'true';

        logger.session(sessionId, 'analytics_requested', { includeRealTime });

        const sessionDetails = await sessionManager.getSessionDetails(sessionId);
        
        // Calculate detailed analytics
        const analytics = {
          overview: {
            sessionId,
            studentId: sessionDetails.basicInfo.studentId,
            duration: sessionDetails.timing.duration,
            progressPercentage: sessionDetails.timing.progressPercentage,
            overallJoyLevel: sessionDetails.joyMetrics.currentJoyLevel
          },
          
          engagement: {
            currentLevel: sessionDetails.learningProgress.currentExperience?.joyFactor || 'high',
            trend: sessionDetails.liveInsights.engagementTrend,
            interactionCount: sessionDetails.learningProgress.interactionCount,
            adaptationsNeeded: sessionDetails.learningProgress.adaptationsApplied
          },
          
          joyAnalytics: {
            joyMoments: sessionDetails.joyMetrics.totalJoyMoments,
            celebrationCount: sessionDetails.joyMetrics.celebrationCount,
            breakthroughMoments: sessionDetails.joyMetrics.breakthroughCount,
            joyProgression: sessionDetails.joyMetrics.recentJoyMoments.map(moment => ({
              timestamp: moment.timestamp,
              joyLevel: moment.joyImpact,
              type: moment.type
            }))
          },
          
          learning: {
            milestonesReached: sessionDetails.learningProgress.milestonesReached,
            currentActivity: sessionDetails.learningProgress.currentExperience?.title,
            learningVelocity: this.calculateLearningVelocity(sessionDetails),
            comprehensionIndicators: this.getComprehensionSignals(sessionDetails)
          },
          
          recommendations: sessionDetails.liveInsights.recommendedActions,
          
          systemHealth: {
            componentsActive: componentRegistry.getRegisteredComponents().length,
            systemJoyLevel: componentRegistry.calculateSystemJoyLevel(),
            adaptationEngineStatus: 'magical'
          }
        };

        if (includeRealTime) {
          analytics.realTime = {
            timestamp: new Date(),
            currentEnergyLevel: sessionDetails.liveInsights.energyLevel,
            suggestedActions: sessionDetails.liveInsights.recommendedActions,
            celebrationReadiness: sessionDetails.joyMetrics.currentJoyLevel > 0.8
          };
        }

        res.json({
          success: true,
          message: `📊 Here are the magical analytics for ${sessionId}!`,
          analytics,
          insightful: true,
          generatedAt: new Date()
        });

      } catch (error) {
        logger.error('Session analytics failed', {
          sessionId: req.params.sessionId,
          error: error.message
        });

        res.status(500).json({
          success: false,
          message: '😅 Our analytics crystal ball got a bit cloudy!',
          error: process.env.NODE_ENV === 'development' ? error.message : 'Analytics failed',
          suggestion: 'Try again - sometimes the best insights take a moment to gather! ✨'
        });
      }
    }
  );

  // 🏥 SESSION HEALTH CHECK
  router.get('/:sessionId/health',
    [
      param('sessionId')
        .notEmpty()
        .withMessage('Which session needs a health check? 🏥')
    ],
    handleValidationErrors,
    async (req, res) => {
      try {
        const { sessionId } = req.params;

        const sessionDetails = await sessionManager.getSessionDetails(sessionId);
        
        // Assess session health
        const health = {
          sessionId,
          overallHealth: 'excellent', // Default to positive!
          indicators: {
            joyLevel: {
              value: sessionDetails.joyMetrics.currentJoyLevel,
              status: sessionDetails.joyMetrics.currentJoyLevel > 0.6 ? 'healthy' : 'needs_attention',
              recommendation: sessionDetails.joyMetrics.currentJoyLevel > 0.6 ? 
                'Joy levels are fantastic! 🌟' : 'Let\'s add some fun activities! 🎪'
            },
            engagement: {
              trend: sessionDetails.liveInsights.engagementTrend,
              status: sessionDetails.liveInsights.engagementTrend === 'rising' ? 'excellent' : 'good',
              recommendation: sessionDetails.liveInsights.engagementTrend === 'rising' ?
                'Engagement is soaring! 🚀' : 'Steady progress - keep it up! ✨'
            },
            timeManagement: {
              timeRemaining: sessionDetails.timing.timeRemaining,
              progressRate: sessionDetails.timing.progressPercentage,
              status: sessionDetails.timing.timeRemaining > 300000 ? 'healthy' : 'approaching_end',
              recommendation: sessionDetails.timing.timeRemaining > 300000 ?
                'Plenty of time for more magic! ⏰' : 'Perfect timing for a strong finish! 🏁'
            },
            systemSupport: {
              componentsHealth: componentRegistry.getHealthSummary(),
              adaptationCapability: 'fully_operational',
              status: 'excellent',
              recommendation: 'All systems supporting this magical learning journey! 🎭'
            }
          },
          timestamp: new Date(),
          checkType: 'comprehensive'
        };

        // Determine overall health
        const healthScores = Object.values(health.indicators).map(indicator => {
          const scoreMap = { excellent: 1, healthy: 0.8, good: 0.6, needs_attention: 0.4 };
          return scoreMap[indicator.status] || 0.5;
        });
        
        const avgHealth = healthScores.reduce((sum, score) => sum + score, 0) / healthScores.length;
        
        if (avgHealth > 0.8) health.overallHealth = 'excellent';
        else if (avgHealth > 0.6) health.overallHealth = 'good';
        else health.overallHealth = 'needs_attention';

        res.json({
          success: true,
          message: `🏥 Health check complete for session ${sessionId}!`,
          health,
          overallStatus: health.overallHealth,
          checkComplete: true,
          careLevel: 'maximum'
        });

      } catch (error) {
        logger.error('Session health check failed', {
          sessionId: req.params.sessionId,
          error: error.message
        });

        res.status(500).json({
          success: false,
          message: '😅 Our health check tools need a quick tune-up!',
          error: process.env.NODE_ENV === 'development' ? error.message : 'Health check failed',
          encouragement: 'Don\'t worry - we care about every session\'s wellbeing! 💝'
        });
      }
    }
  );

  // Helper methods for analytics
  router.calculateLearningVelocity = (sessionDetails) => {
    const duration = sessionDetails.timing.duration;
    const interactions = sessionDetails.learningProgress.interactionCount;
    const milestones = sessionDetails.learningProgress.milestonesReached;
    
    if (duration === 0) return 0;
    
    // Simple velocity calculation: (interactions + milestones) per minute
    return ((interactions + milestones * 10) / (duration / 60000)).toFixed(2);
  };

  router.getComprehensionSignals = (sessionDetails) => {
    const signals = [];
    
    if (sessionDetails.joyMetrics.breakthroughCount > 0) {
      signals.push('breakthrough_moments_detected');
    }
    
    if (sessionDetails.learningProgress.adaptationsApplied === 0) {
      signals.push('steady_comprehension_no_adaptations_needed');
    }
    
    if (sessionDetails.joyMetrics.currentJoyLevel > 0.7) {
      signals.push('high_confidence_and_enjoyment');
    }
    
    return signals.length > 0 ? signals : ['learning_in_progress'];
  };

  // Add some joy to every response! ✨
  router.use((req, res, next) => {
    if (res.locals.response) {
      res.locals.response.poweredBy = 'NeuroBloom.ai Magic ✨';
      res.locals.response.joyLevel = 'maximum';
    }
    next();
  });

  return router;
};
