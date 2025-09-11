// integration_engine/components/pact_orchestrator.js
// Main orchestration logic for PACT system coordination

const EventEmitter = require('events');
const logger = require('../utils/logger');
const CreativeSynthesisClient = require('../clients/creative_synthesis_client');

class PACTOrchestrator extends EventEmitter {
  constructor(integrationServer) {
    super();
    this.server = integrationServer;
    this.config = integrationServer.config;
    
    // Initialize external clients
    this.creativeSynthesisClient = new CreativeSynthesisClient(
      this.config.creativeSynthesis.apiUrl
    );
    
    // Active orchestrations
    this.activeOrchestrations = new Map();
    this.orchestrationHistory = new Map();
    
    logger.info('🎭 PACT Orchestrator initialized');
  }

  async orchestratePersonalizedLearning(studentId, learningObjective, sessionContext = {}) {
    const orchestrationId = this.generateOrchestrationId();
    
    logger.info('🎯 Starting personalized learning orchestration', {
      orchestrationId,
      studentId,
      learningObjective
    });

    try {
      // 1. Get comprehensive student state from all components
      const studentProfile = await this.getUnifiedStudentProfile(studentId);
      
      // 2. Generate initial creative experience
      const initialExperience = await this.creativeSynthesisClient.generateExperience({
        learningObjective,
        studentProfile,
        sessionContext
      });

      // 3. Create orchestration tracking
      const orchestration = {
        id: orchestrationId,
        studentId,
        learningObjective,
        sessionContext,
        studentProfile,
        currentExperience: initialExperience,
        adaptationHistory: [],
        startTime: Date.now(),
        status: 'active'
      };

      this.activeOrchestrations.set(orchestrationId, orchestration);

      // 4. Start real-time monitoring and adaptation
      this.startRealTimeOrchestration(orchestration);

      // 5. Notify all components about new orchestration
      this.notifyComponentsOfNewOrchestration(orchestration);

      logger.info('✅ Personalized learning orchestration started', {
        orchestrationId,
        experienceTitle: initialExperience.title
      });

      return {
        orchestrationId,
        initialExperience,
        studentProfile,
        estimatedDuration: sessionContext.timeLimit || 30,
        adaptationCapabilities: this.getAdaptationCapabilities()
      };

    } catch (error) {
      logger.error('❌ Failed to orchestrate personalized learning', {
        orchestrationId,
        studentId,
        error: error.message
      });
      throw error;
    }
  }

  async getUnifiedStudentProfile(studentId) {
    const profile = {
      studentId,
      timestamp: Date.now(),
      
      // Default profile structure
      engagement: { averageScore: 0.5, trend: 'stable' },
      trust: { level: 0.5, stage: 'basic_comfort' },
      emotional: { state: 'neutral', motivation: 'medium' },
      learning: { styles: ['visual'], preferences: {} },
      creative: { modalities: ['story'], strengths: [] },
      history: { sessions: [], outcomes: [] }
    };

    try {
      // Get engagement data from engagement tracker
      const engagementComponent = this.server.componentRegistry.findComponentByType('engagement_tracker');
      if (engagementComponent) {
        const engagementData = await this.requestFromComponent(
          engagementComponent, 
          'get_student_profile', 
          { studentId }
        );
        if (engagementData) {
          profile.engagement = { ...profile.engagement, ...engagementData.engagement };
          profile.trust = { ...profile.trust, ...engagementData.trust };
        }
      }

      // Get emotional/empathetic data
      const empathyComponent = this.server.componentRegistry.findComponentByType('empathetic_interaction');
      if (empathyComponent) {
        const empathyData = await this.requestFromComponent(
          empathyComponent,
          'get_emotional_profile',
          { studentId }
        );
        if (empathyData) {
          profile.emotional = { ...profile.emotional, ...empathyData };
        }
      }

      // Get creative profile from creative synthesis
      try {
        const creativeData = await this.creativeSynthesisClient.getStudentCreativeProfile(studentId);
        if (creativeData) {
          profile.creative = { ...profile.creative, ...creativeData };
        }
      } catch (error) {
        logger.warn('Could not fetch creative profile, using defaults', { studentId });
      }

      // Get session history
      const sessionHistory = await this.server.sessionManager.getStudentSessionHistory(studentId);
      if (sessionHistory) {
        profile.history = sessionHistory;
      }

      // Compute derived insights
      profile.insights = this.computeStudentInsights(profile);

      logger.debug('📊 Unified student profile assembled', {
        studentId,
        profileComponents: Object.keys(profile)
      });

      return profile;

    } catch (error) {
      logger.error('Failed to assemble unified student profile', {
        studentId,
        error: error.message
      });
      
      // Return default profile on error
      return profile;
    }
  }

  computeStudentInsights(profile) {
    const insights = {
      overallPerformance: 0.5,
      recommendedApproaches: [],
      growthAreas: [],
      strengths: [],
      riskFactors: []
    };

    // Calculate overall performance
    const engagementScore = profile.engagement?.averageScore || 0.5;
    const trustScore = profile.trust?.level || 0.5;
    const motivationScore = this.mapMotivationToScore(profile.emotional?.motivation);
    
    insights.overallPerformance = (engagementScore * 0.4 + trustScore * 0.3 + motivationScore * 0.3);

    // Generate recommendations based on profile
    if (engagementScore < 0.5) {
      insights.recommendedApproaches.push('Increase interactive and kinesthetic elements');
      insights.growthAreas.push('Sustained attention and engagement');
    }

    if (trustScore < 0.5) {
      insights.recommendedApproaches.push('Focus on relationship building and encouragement');
      insights.growthAreas.push('Comfort with AI assistance');
    }

    if (motivationScore < 0.5) {
      insights.recommendedApproaches.push('Connect learning to personal interests');
      insights.growthAreas.push('Intrinsic motivation');
    }

    // Identify strengths
    if (engagementScore > 0.7) insights.strengths.push('High engagement capacity');
    if (trustScore > 0.7) insights.strengths.push('Strong AI collaboration');
    if (motivationScore > 0.7) insights.strengths.push('Self-motivated learner');

    // Identify risk factors
    if (engagementScore < 0.3) insights.riskFactors.push('Low engagement - risk of disengagement');
    if (trustScore < 0.3) insights.riskFactors.push('AI trust issues - may resist technology');
    
    return insights;
  }

  mapMotivationToScore(motivation) {
    const motivationMap = {
      'high': 0.8,
      'medium': 0.6,
      'low': 0.4,
      'very_low': 0.2
    };
    return motivationMap[motivation] || 0.5;
  }

  startRealTimeOrchestration(orchestration) {
    const orchestrationId = orchestration.id;
    
    // Set up real-time monitoring interval
    const monitoringInterval = setInterval(async () => {
      try {
        await this.performOrchestrationCycle(orchestration);
      } catch (error) {
        logger.error('Orchestration cycle failed', {
          orchestrationId,
          error: error.message
        });
      }
    }, this.config.orchestration.cycleInterval || 10000); // 10 seconds

    // Store monitoring interval for cleanup
    orchestration.monitoringInterval = monitoringInterval;

    // Set up orchestration timeout
    const timeoutDuration = orchestration.sessionContext.timeLimit * 60000 || 1800000; // 30 minutes default
    orchestration.timeoutHandler = setTimeout(async () => {
      await this.endOrchestration(orchestrationId, 'timeout');
    }, timeoutDuration);
  }

  async performOrchestrationCycle(orchestration) {
    const { id: orchestrationId, studentId } = orchestration;

    // 1. Check for adaptation triggers from all components
    const adaptationNeeds = await this.assessAdaptationNeeds(orchestration);

    if (adaptationNeeds.length > 0) {
      logger.info('🔄 Adaptation needs detected', {
        orchestrationId,
        adaptationCount: adaptationNeeds.length,
        triggers: adaptationNeeds.map(a => a.trigger)
      });

      // 2. Select and execute the most important adaptation
      const primaryAdaptation = this.selectPrimaryAdaptation(adaptationNeeds);
      await this.executeAdaptation(orchestration, primaryAdaptation);
    }

    // 3. Update orchestration health and metrics
    await this.updateOrchestrationMetrics(orchestration);

    // 4. Check for orchestration completion conditions
    const shouldComplete = await this.checkCompletionConditions(orchestration);
    if (shouldComplete.complete) {
      await this.endOrchestration(orchestrationId, shouldComplete.reason);
    }
  }

  async assessAdaptationNeeds(orchestration) {
    const adaptationNeeds = [];
    const { studentId } = orchestration;

    try {
      // Check engagement-based adaptations
      const engagementAdaptation = await this.server.adaptationEngine.assessEngagementAdaptation(
        studentId, orchestration
      );
      if (engagementAdaptation) {
        adaptationNeeds.push({
          type: 'engagement',
          trigger: engagementAdaptation.trigger,
          priority: engagementAdaptation.priority || 'medium',
          data: engagementAdaptation
        });
      }

      // Check trust-based adaptations
      const trustAdaptation = await this.server.adaptationEngine.assessTrustAdaptation(
        studentId, orchestration
      );
      if (trustAdaptation) {
        adaptationNeeds.push({
          type: 'trust',
          trigger: trustAdaptation.trigger,
          priority: trustAdaptation.priority || 'medium',
          data: trustAdaptation
        });
      }

      // Check learning progress adaptations
      const progressAdaptation = await this.assessLearningProgressAdaptation(orchestration);
      if (progressAdaptation) {
        adaptationNeeds.push({
          type: 'progress',
          trigger: progressAdaptation.trigger,
          priority: progressAdaptation.priority || 'low',
          data: progressAdaptation
        });
      }

      // Check teacher-initiated adaptations
      const teacherAdaptation = await this.checkTeacherAdaptationRequests(orchestration);
      if (teacherAdaptation) {
        adaptationNeeds.push({
          type: 'teacher',
          trigger: teacherAdaptation.trigger,
          priority: 'high', // Teacher requests have high priority
          data: teacherAdaptation
        });
      }

    } catch (error) {
      logger.error('Failed to assess adaptation needs', {
        orchestrationId: orchestration.id,
        error: error.message
      });
    }

    return adaptationNeeds;
  }

  selectPrimaryAdaptation(adaptationNeeds) {
    // Sort by priority: high > medium > low
    const priorityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
    
    adaptationNeeds.sort((a, b) => {
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });

    return adaptationNeeds[0]; // Return highest priority adaptation
  }

  async executeAdaptation(orchestration, adaptationNeed) {
    const { id: orchestrationId, studentId } = orchestration;
    const adaptationId = this.generateAdaptationId();

    logger.info('🎨 Executing adaptation', {
      orchestrationId,
      adaptationId,
      type: adaptationNeed.type,
      trigger: adaptationNeed.trigger
    });

    try {
      // 1. Get current student profile
      const currentProfile = await this.getUnifiedStudentProfile(studentId);

      // 2. Request adaptation from Creative Synthesis
      const adaptationRequest = {
        currentExperience: orchestration.currentExperience,
        studentProfile: currentProfile,
        adaptationReason: adaptationNeed.trigger,
        adaptationType: adaptationNeed.type,
        adaptationData: adaptationNeed.data,
        constraints: orchestration.sessionContext
      };

      const adaptation = await this.creativeSynthesisClient.generateAdaptation(adaptationRequest);

      // 3. Update orchestration with new experience
      const previousExperience = orchestration.currentExperience;
      orchestration.currentExperience = adaptation.newExperience;

      // 4. Record adaptation in history
      const adaptationRecord = {
        id: adaptationId,
        timestamp: Date.now(),
        type: adaptationNeed.type,
        trigger: adaptationNeed.trigger,
        previousExperience: previousExperience,
        newExperience: adaptation.newExperience,
        strategy: adaptation.strategy,
        confidence: adaptation.confidence || 0.75
      };

      orchestration.adaptationHistory.push(adaptationRecord);

      // 5. Apply adaptation to student interface
      await this.applyAdaptationToInterface(studentId, adaptation, adaptationRecord);

      // 6. Notify teacher dashboard
      await this.notifyTeacherOfAdaptation(studentId, adaptationRecord);

      // 7. Update component states
      await this.updateComponentStates(studentId, adaptation);

      logger.info('✅ Adaptation executed successfully', {
        orchestrationId,
        adaptationId,
        strategy: adaptation.strategy
      });

      return adaptationRecord;

    } catch (error) {
      logger.error('❌ Adaptation execution failed', {
        orchestrationId,
        adaptationId,
        error: error.message
      });
      throw error;
    }
  }

  async applyAdaptationToInterface(studentId, adaptation, adaptationRecord) {
    const studentInterface = this.server.componentRegistry.findComponentByType('student_interface');
    
    if (studentInterface) {
      try {
        await this.requestFromComponent(studentInterface, 'apply_adaptation', {
          studentId,
          adaptation: adaptation.newExperience,
          adaptationId: adaptationRecord.id,
          strategy: adaptation.strategy,
          transition: adaptation.transition || 'smooth'
        });
      } catch (error) {
        logger.warn('Failed to apply adaptation to student interface', {
          studentId,
          adaptationId: adaptationRecord.id,
          error: error.message
        });
      }
    }
  }

  async notifyTeacherOfAdaptation(studentId, adaptationRecord) {
    const teacherDashboard = this.server.componentRegistry.findComponentByType('teacher_dashboard');
    
    if (teacherDashboard) {
      try {
        await this.requestFromComponent(teacherDashboard, 'adaptation_notification', {
          studentId,
          adaptationId: adaptationRecord.id,
          type: adaptationRecord.type,
          trigger: adaptationRecord.trigger,
          strategy: adaptationRecord.strategy,
          timestamp: adaptationRecord.timestamp
        });
      } catch (error) {
        logger.warn('Failed to notify teacher dashboard', {
          studentId,
          adaptationId: adaptationRecord.id,
          error: error.message
        });
      }
    }
  }

  async updateComponentStates(studentId, adaptation) {
    // Update engagement tracker with adaptation info
    const engagementTracker = this.server.componentRegistry.findComponentByType('engagement_tracker');
    if (engagementTracker) {
      try {
        await this.requestFromComponent(engagementTracker, 'adaptation_applied', {
          studentId,
          adaptationStrategy: adaptation.strategy,
          expectedImpact: adaptation.expectedImpact
        });
      } catch (error) {
        logger.warn('Failed to update engagement tracker', { studentId, error: error.message });
      }
    }

    // Update empathetic interaction with new approach
    const empathyComponent = this.server.componentRegistry.findComponentByType('empathetic_interaction');
    if (empathyComponent) {
      try {
        await this.requestFromComponent(empathyComponent, 'update_interaction_style', {
          studentId,
          newApproach: adaptation.empathyAdjustments || {}
        });
      } catch (error) {
        logger.warn('Failed to update empathetic interaction', { studentId, error: error.message });
      }
    }
  }

  async assessLearningProgressAdaptation(orchestration) {
    const { studentId, currentExperience, adaptationHistory } = orchestration;
    
    // Check if student has been stuck on same concept for too long
    const recentAdaptations = adaptationHistory.slice(-3);
    const stuckOnSameConcept = recentAdaptations.length >= 2 && 
      recentAdaptations.every(a => a.trigger.includes('low_engagement'));

    if (stuckOnSameConcept) {
      return {
        trigger: 'stuck_on_concept',
        reason: 'Student showing repeated low engagement on same concept',
        recommendation: 'switch_concept_approach',
        priority: 'medium'
      };
    }

    // Check if student is ready for advancement
    const sessionDuration = Date.now() - orchestration.startTime;
    const minSessionTime = 10 * 60000; // 10 minutes
    
    if (sessionDuration > minSessionTime && adaptationHistory.length === 0) {
      // No adaptations needed - student doing well, might be ready for advancement
      return {
        trigger: 'advancement_opportunity',
        reason: 'Student performing well without adaptations needed',
        recommendation: 'increase_challenge',
        priority: 'low'
      };
    }

    return null;
  }

  async checkTeacherAdaptationRequests(orchestration) {
    // Check for manual teacher interventions
    const teacherRequests = await this.server.sessionManager.getTeacherRequests(orchestration.id);
    
    if (teacherRequests && teacherRequests.length > 0) {
      const latestRequest = teacherRequests[teacherRequests.length - 1];
      
      return {
        trigger: 'teacher_request',
        reason: latestRequest.reason || 'Manual teacher intervention',
        requestedAction: latestRequest.action,
        teacherId: latestRequest.teacherId,
        priority: 'high'
      };
    }

    return null;
  }

  async updateOrchestrationMetrics(orchestration) {
    const { id: orchestrationId, studentId } = orchestration;
    
    try {
      // Get current engagement metrics
      const currentEngagement = await this.getCurrentEngagement(studentId);
      const currentTrust = await this.getCurrentTrust(studentId);

      // Update orchestration metrics
      orchestration.currentMetrics = {
        timestamp: Date.now(),
        engagement: currentEngagement,
        trust: currentTrust,
        adaptationCount: orchestration.adaptationHistory.length,
        sessionDuration: Date.now() - orchestration.startTime
      };

      // Store metrics history
      if (!orchestration.metricsHistory) {
        orchestration.metricsHistory = [];
      }
      orchestration.metricsHistory.push(orchestration.currentMetrics);

      // Keep only last 50 metrics snapshots
      if (orchestration.metricsHistory.length > 50) {
        orchestration.metricsHistory = orchestration.metricsHistory.slice(-50);
      }

    } catch (error) {
      logger.error('Failed to update orchestration metrics', {
        orchestrationId,
        error: error.message
      });
    }
  }

  async checkCompletionConditions(orchestration) {
    const { sessionContext, startTime, adaptationHistory } = orchestration;
    const sessionDuration = Date.now() - startTime;

    // Check time limit
    const timeLimit = sessionContext.timeLimit * 60000 || 1800000; // 30 minutes default
    if (sessionDuration >= timeLimit) {
      return {
        complete: true,
        reason: 'time_limit_reached'
      };
    }

    // Check if learning objective is achieved
    const objectiveAchieved = await this.assessObjectiveCompletion(orchestration);
    if (objectiveAchieved) {
      return {
        complete: true,
        reason: 'objective_achieved'
      };
    }

    // Check for excessive adaptations (might indicate systemic issues)
    if (adaptationHistory.length > 10) {
      return {
        complete: true,
        reason: 'excessive_adaptations'
      };
    }

    // Check for student disengagement
    const currentEngagement = await this.getCurrentEngagement(orchestration.studentId);
    if (currentEngagement && currentEngagement.score < 0.2 && sessionDuration > 600000) { // 10 minutes
      return {
        complete: true,
        reason: 'persistent_disengagement'
      };
    }

    return { complete: false };
  }

  async assessObjectiveCompletion(orchestration) {
    // This would integrate with assessment systems to determine if learning objective is met
    // For now, use simple heuristics
    
    const { studentId, adaptationHistory, currentMetrics } = orchestration;
    
    // If student has high engagement and trust, and minimal adaptations needed
    if (currentMetrics && 
        currentMetrics.engagement?.score > 0.8 && 
        currentMetrics.trust?.level > 0.7 && 
        adaptationHistory.length <= 2) {
      return true;
    }

    return false;
  }

  async endOrchestration(orchestrationId, reason) {
    const orchestration = this.activeOrchestrations.get(orchestrationId);
    if (!orchestration) {
      logger.warn('Attempted to end non-existent orchestration', { orchestrationId });
      return;
    }

    logger.info('🏁 Ending orchestration', {
      orchestrationId,
      studentId: orchestration.studentId,
      reason,
      duration: Date.now() - orchestration.startTime,
      adaptations: orchestration.adaptationHistory.length
    });

    try {
      // Clean up monitoring
      if (orchestration.monitoringInterval) {
        clearInterval(orchestration.monitoringInterval);
      }
      if (orchestration.timeoutHandler) {
        clearTimeout(orchestration.timeoutHandler);
      }

      // Generate final summary
      const summary = await this.generateOrchestrationSummary(orchestration, reason);

      // Notify components of orchestration end
      await this.notifyComponentsOfOrchestrationEnd(orchestration, summary);

      // Archive orchestration
      orchestration.status = 'completed';
      orchestration.endTime = Date.now();
      orchestration.endReason = reason;
      orchestration.summary = summary;

      // Move to history
      this.orchestrationHistory.set(orchestrationId, orchestration);
      this.activeOrchestrations.delete(orchestrationId);

      logger.info('✅ Orchestration ended successfully', {
        orchestrationId,
        summary: {
          outcome: summary.outcome,
          finalEngagement: summary.finalMetrics?.engagement?.score,
          adaptationCount: summary.adaptationCount
        }
      });

      return summary;

    } catch (error) {
      logger.error('❌ Failed to end orchestration cleanly', {
        orchestrationId,
        error: error.message
      });
    }
  }

  async generateOrchestrationSummary(orchestration, endReason) {
    const { id, studentId, learningObjective, startTime, adaptationHistory, currentMetrics } = orchestration;
    const duration = Date.now() - startTime;

    const summary = {
      orchestrationId: id,
      studentId,
      learningObjective,
      duration,
      endReason,
      adaptationCount: adaptationHistory.length,
      finalMetrics: currentMetrics,
      outcome: this.assessOrchestrationOutcome(orchestration, endReason),
      insights: this.generateOrchestrationInsights(orchestration),
      recommendations: this.generateFutureRecommendations(orchestration)
    };

    return summary;
  }

  assessOrchestrationOutcome(orchestration, endReason) {
    const { adaptationHistory, currentMetrics } = orchestration;
    
    if (endReason === 'objective_achieved') {
      return 'excellent';
    } else if (endReason === 'time_limit_reached' && 
               currentMetrics?.engagement?.score > 0.6) {
      return 'good';
    } else if (adaptationHistory.length > 7) {
      return 'challenging';
    } else if (endReason === 'persistent_disengagement') {
      return 'needs_improvement';
    } else {
      return 'satisfactory';
    }
  }

  generateOrchestrationInsights(orchestration) {
    const { adaptationHistory, metricsHistory } = orchestration;
    const insights = [];

    // Analyze adaptation patterns
    if (adaptationHistory.length === 0) {
      insights.push('Student required no adaptations - excellent self-directed learning');
    } else if (adaptationHistory.length > 5) {
      insights.push('Multiple adaptations needed - consider different approach or support');
    }

    // Analyze engagement patterns
    if (metricsHistory && metricsHistory.length > 0) {
      const engagementTrend = this.calculateEngagementTrend(metricsHistory);
      if (engagementTrend === 'improving') {
        insights.push('Engagement improved throughout session');
      } else if (engagementTrend === 'declining') {
        insights.push('Engagement declined - investigate fatigue or difficulty');
      }
    }

    // Analyze trust development
    const trustAdaptations = adaptationHistory.filter(a => a.type === 'trust');
    if (trustAdaptations.length > 0) {
      insights.push('Trust-building was a focus area during session');
    }

    return insights;
  }

  calculateEngagementTrend(metricsHistory) {
    if (metricsHistory.length < 3) return 'stable';

    const recent = metricsHistory.slice(-3);
    const older = metricsHistory.slice(-6, -3);

    if (older.length === 0) return 'stable';

    const recentAvg = recent.reduce((sum, m) => sum + (m.engagement?.score || 0), 0) / recent.length;
    const olderAvg = older.reduce((sum, m) => sum + (m.engagement?.score || 0), 0) / older.length;

    const diff = recentAvg - olderAvg;

    if (diff > 0.1) return 'improving';
    if (diff < -0.1) return 'declining';
    return 'stable';
  }

  generateFutureRecommendations(orchestration) {
    const recommendations = [];
    const { adaptationHistory, currentMetrics } = orchestration;

    // Engagement-based recommendations
    if (currentMetrics?.engagement?.score < 0.5) {
      recommendations.push('Focus on more engaging, interactive content in future sessions');
    }

    // Trust-based recommendations
    if (currentMetrics?.trust?.level < 0.5) {
      recommendations.push('Prioritize relationship building and trust development');
    }

    // Adaptation pattern recommendations
    const adaptationTypes = adaptationHistory.map(a => a.type);
    const mostCommonType = this.getMostFrequent(adaptationTypes);
    
    if (mostCommonType === 'engagement') {
      recommendations.push('Consider pre-session engagement assessment and tailoring');
    } else if (mostCommonType === 'trust') {
      recommendations.push('Plan trust-building activities at session start');
    }

    return recommendations;
  }

  getMostFrequent(array) {
    if (array.length === 0) return null;
    
    const frequency = array.reduce((acc, item) => {
      acc[item] = (acc[item] || 0) + 1;
      return acc;
    }, {});

    return Object.entries(frequency).reduce((max, [item, count]) => 
      count > max.count ? { item, count } : max, 
      { item: null, count: 0 }
    ).item;
  }

  async notifyComponentsOfNewOrchestration(orchestration) {
    const notification = {
      type: 'orchestration_started',
      orchestrationId: orchestration.id,
      studentId: orchestration.studentId,
      learningObjective: orchestration.learningObjective,
      initialExperience: orchestration.currentExperience
    };

    this.server.io.emit('system_notification', notification);
  }

  async notifyComponentsOfOrchestrationEnd(orchestration, summary) {
    const notification = {
      type: 'orchestration_ended',
      orchestrationId: orchestration.id,
      studentId: orchestration.studentId,
      summary: summary
    };

    this.server.io.emit('system_notification', notification);
  }

  async handleTeacherRequest(requestData) {
    const { requestType, data } = requestData;
    
    logger.info('👩‍🏫 Handling teacher request', { requestType });

    switch (requestType) {
      case 'classroom_overview':
        return await this.getClassroomOverview(data.classId);
      
      case 'student_detail':
        return await this.getStudentDetail(data.studentId);
      
      case 'trigger_adaptation':
        return await this.triggerManualAdaptation(data);
      
      case 'orchestration_summary':
        return await this.getOrchestrationSummary(data.orchestrationId);
      
      case 'class_analytics':
        return await this.getClassAnalytics(data.classId, data.timeRange);
      
      default:
        throw new Error(`Unknown teacher request type: ${requestType}`);
    }
  }

  async getClassroomOverview(classId) {
    const activeOrchestrations = Array.from(this.activeOrchestrations.values())
      .filter(o => o.sessionContext.classId === classId);

    const overview = {
      classId,
      timestamp: Date.now(),
      totalStudents: activeOrchestrations.length,
      orchestrations: await Promise.all(
        activeOrchestrations.map(async (o) => ({
          studentId: o.studentId,
          orchestrationId: o.id,
          currentEngagement: await this.getCurrentEngagement(o.studentId),
          currentTrust: await this.getCurrentTrust(o.studentId),
          adaptationCount: o.adaptationHistory.length,
          sessionDuration: Date.now() - o.startTime,
          status: o.status
        }))
      )
    };

    // Calculate class-level metrics
    overview.classMetrics = this.calculateClassMetrics(overview.orchestrations);

    return overview;
  }

  calculateClassMetrics(orchestrations) {
    if (orchestrations.length === 0) {
      return { averageEngagement: 0, averageTrust: 0, totalAdaptations: 0 };
    }

    const totalEngagement = orchestrations.reduce((sum, o) => 
      sum + (o.currentEngagement?.score || 0), 0);
    const totalTrust = orchestrations.reduce((sum, o) => 
      sum + (o.currentTrust?.level || 0), 0);
    const totalAdaptations = orchestrations.reduce((sum, o) => 
      sum + o.adaptationCount, 0);

    return {
      averageEngagement: totalEngagement / orchestrations.length,
      averageTrust: totalTrust / orchestrations.length,
      totalAdaptations,
      studentsNeedingSupport: orchestrations.filter(o => 
        (o.currentEngagement?.score || 0) < 0.4).length,
      highPerformers: orchestrations.filter(o => 
        (o.currentEngagement?.score || 0) > 0.8 && 
        (o.currentTrust?.level || 0) > 0.7).length
    };
  }

  async getCurrentEngagement(studentId) {
    try {
      const engagementComponent = this.server.componentRegistry.findComponentByType('engagement_tracker');
      if (engagementComponent) {
        return await this.requestFromComponent(engagementComponent, 'get_current_engagement', { studentId });
      }
    } catch (error) {
      logger.warn('Could not get current engagement', { studentId, error: error.message });
    }
    return { score: 0.5, level: 'medium', trend: 'stable' };
  }

  async getCurrentTrust(studentId) {
    try {
      const engagementComponent = this.server.componentRegistry.findComponentByType('engagement_tracker');
      if (engagementComponent) {
        return await this.requestFromComponent(engagementComponent, 'get_current_trust', { studentId });
      }
    } catch (error) {
      logger.warn('Could not get current trust', { studentId, error: error.message });
    }
    return { level: 0.5, stage: 'basic_comfort' };
  }

  async requestFromComponent(component, requestType, data) {
    return new Promise((resolve, reject) => {
      const requestId = Math.random().toString(36).substr(2, 9);
      
      const responseHandler = (response) => {
        if (response.requestId === requestId) {
          component.socket.off('component_response', responseHandler);
          resolve(response.data);
        }
      };
      
      component.socket.on('component_response', responseHandler);
      
      component.socket.emit('component_request', {
        requestId,
        requestType,
        data
      });
      
      setTimeout(() => {
        component.socket.off('component_response', responseHandler);
        reject(new Error('Component request timeout'));
      }, 5000);
    });
  }

  generateOrchestrationId() {
    return `orch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateAdaptationId() {
    return `adapt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  getAdaptationCapabilities() {
    return {
      realTimeAdaptation: true,
      multiModalApproach: true,
      trustBasedAdjustment: true,
      teacherOverride: true,
      progressiveChallenge: true,
      emotionalResponse: true
    };
  }

  // Public API methods for external access
  getActiveOrchestrations() {
    return Array.from(this.activeOrchestrations.values());
  }

  getOrchestrationHistory() {
    return Array.from(this.orchestrationHistory.values());
  }

  getOrchestrationStats() {
    return {
      active: this.activeOrchestrations.size,
      total: this.activeOrchestrations.size + this.orchestrationHistory.size,
      averageDuration: this.calculateAverageDuration(),
      successRate: this.calculateSuccessRate()
    };
  }

  calculateAverageDuration() {
    const completed = Array.from(this.orchestrationHistory.values());
    if (completed.length === 0) return 0;

    const totalDuration = completed.reduce((sum, o) => sum + (o.endTime - o.startTime), 0);
    return totalDuration / completed.length;
  }

  calculateSuccessRate() {
    const completed = Array.from(this.orchestrationHistory.values());
    if (completed.length === 0) return 0;

    const successful = completed.filter(o => 
      o.summary?.outcome === 'excellent' || o.summary?.outcome === 'good'
    ).length;

    return successful / completed.length;
  }
}

module.exports = PACTOrchestrator;
