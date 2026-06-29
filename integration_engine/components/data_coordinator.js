// integration_engine/components/data_coordinator.js
// Cross-component data management and synchronization

const EventEmitter = require('events');
const Redis = require('redis');
const logger = require('../utils/logger');

class DataCoordinator extends EventEmitter {
  constructor(integrationServer) {
    super();
    this.server = integrationServer;
    this.config = integrationServer.config;
    
    // Data storage and caching
    this.participantProfiles = new Map();
    this.sessionData = new Map();
    this.realTimeData = new Map();
    this.dataBuffer = new Map();
    
    // Redis connection for persistence
    this.redis = null;
    
    // Data synchronization settings
    this.syncInterval = 5000; // 5 seconds
    this.bufferFlushInterval = 2000; // 2 seconds
    this.maxBufferSize = 1000;
    
    // Component data handlers
    this.dataHandlers = new Map();
    this.setupDataHandlers();
    
    logger.info('📊 Data Coordinator initialized');
  }

  async initializeConnections() {
    try {
      // Initialize Redis connection
      if (this.config.redis?.enabled) {
        this.redis = Redis.createClient({
          url: this.config.redis.url || 'redis://localhost:6379',
          socket: {
            connectTimeout: 5000,
            lazyConnect: true
          }
        });

        this.redis.on('error', (error) => {
          logger.error('Redis connection error', { error: error.message });
        });

        this.redis.on('connect', () => {
          logger.info('📡 Redis connected for data persistence');
        });

        await this.redis.connect();
      }
      
      // Start data synchronization processes
      this.startDataSynchronization();
      this.startBufferFlushing();
      
      logger.info('✅ Data Coordinator connections initialized');
    } catch (error) {
      logger.warn('⚠️ Data Coordinator using in-memory storage only', {
        error: error.message
      });
    }
  }

  setupDataHandlers() {
    // Engagement data handler
    this.dataHandlers.set('engagement', {
      process: this.processEngagementData.bind(this),
      validate: this.validateEngagementData.bind(this),
      sync: this.syncEngagementData.bind(this)
    });

    // Trust data handler
    this.dataHandlers.set('trust', {
      process: this.processTrustData.bind(this),
      validate: this.validateTrustData.bind(this),
      sync: this.syncTrustData.bind(this)
    });

    // Interaction data handler
    this.dataHandlers.set('interaction', {
      process: this.processInteractionData.bind(this),
      validate: this.validateInteractionData.bind(this),
      sync: this.syncInteractionData.bind(this)
    });

    // Learning progress handler
    this.dataHandlers.set('progress', {
      process: this.processProgressData.bind(this),
      validate: this.validateProgressData.bind(this),
      sync: this.syncProgressData.bind(this)
    });

    // Adaptation result handler
    this.dataHandlers.set('adaptation', {
      process: this.processAdaptationData.bind(this),
      validate: this.validateAdaptationData.bind(this),
      sync: this.syncAdaptationData.bind(this)
    });
  }

  startDataSynchronization() {
    setInterval(() => {
      this.synchronizeDataAcrossComponents().catch(error => {
        logger.error('Data synchronization failed', { error: error.message });
      });
    }, this.syncInterval);

    logger.info('🔄 Data synchronization started', { interval: this.syncInterval });
  }

  startBufferFlushing() {
    setInterval(() => {
      this.flushDataBuffer().catch(error => {
        logger.error('Buffer flush failed', { error: error.message });
      });
    }, this.bufferFlushInterval);

    logger.info('💾 Buffer flushing started', { interval: this.bufferFlushInterval });
  }

  // Main event handlers for real-time data
  async handleEngagementUpdate(socket, data) {
    const { participantId, sessionId, engagementData } = data;
    
    try {
      // Validate data
      const handler = this.dataHandlers.get('engagement');
      const validationResult = handler.validate(engagementData);
      
      if (!validationResult.valid) {
        throw new Error(`Invalid engagement data: ${validationResult.errors.join(', ')}`);
      }

      // Process and enrich data
      const processedData = await handler.process(participantId, engagementData, sessionId);

      // Update participant profile
      await this.updateParticipantEngagementProfile(participantId, processedData);

      // Buffer for synchronization
      this.bufferDataUpdate(participantId, 'engagement', processedData);

      // Emit real-time update
      this.emitRealTimeUpdate('engagement_update', {
        participantId,
        sessionId,
        data: processedData,
        timestamp: Date.now()
      });

      // Check for immediate adaptation needs
      const adaptationNeeded = await this.assessImmediateAdaptationNeed(
        participantId, 'engagement', processedData
      );

      // Send acknowledgment
      socket.emit('engagement_update_processed', {
        sessionId,
        processed: true,
        adaptationTriggered: !!adaptationNeeded
      });

      logger.debug('📈 Engagement update processed', {
        participantId,
        sessionId,
        score: processedData.currentScore,
        trend: processedData.trend
      });

    } catch (error) {
      logger.error('❌ Failed to handle engagement update', {
        participantId,
        sessionId,
        error: error.message
      });
      
      socket.emit('engagement_update_error', {
        sessionId,
        error: error.message
      });
    }
  }

  async handleTrustEvent(socket, data) {
    const { participantId, sessionId, trustEvent } = data;
    
    try {
      // Validate trust event
      const handler = this.dataHandlers.get('trust');
      const validationResult = handler.validate(trustEvent);
      
      if (!validationResult.valid) {
        throw new Error(`Invalid trust event: ${validationResult.errors.join(', ')}`);
      }

      // Process trust event
      const processedEvent = await handler.process(participantId, trustEvent, sessionId);

      // Update participant trust profile
      await this.updateParticipantTrustProfile(participantId, processedEvent);

      // Buffer for synchronization
      this.bufferDataUpdate(participantId, 'trust', processedEvent);

      // Emit real-time update
      this.emitRealTimeUpdate('trust_event', {
        participantId,
        sessionId,
        event: processedEvent,
        timestamp: Date.now()
      });

      // Check for trust-based adaptations
      const adaptationNeeded = await this.assessImmediateAdaptationNeed(
        participantId, 'trust', processedEvent
      );

      socket.emit('trust_event_processed', {
        sessionId,
        processed: true,
        adaptationTriggered: !!adaptationNeeded
      });

      logger.debug('🤝 Trust event processed', {
        participantId,
        sessionId,
        eventType: processedEvent.type,
        trustLevel: processedEvent.newTrustLevel
      });

    } catch (error) {
      logger.error('❌ Failed to handle trust event', {
        participantId,
        sessionId,
        error: error.message
      });
      
      socket.emit('trust_event_error', {
        sessionId,
        error: error.message
      });
    }
  }

  async handleParticipantInteraction(socket, data) {
    const { participantId, sessionId, interaction } = data;
    
    try {
      // Validate interaction
      const handler = this.dataHandlers.get('interaction');
      const validationResult = handler.validate(interaction);
      
      if (!validationResult.valid) {
        throw new Error(`Invalid interaction: ${validationResult.errors.join(', ')}`);
      }

      // Process interaction
      const processedInteraction = await handler.process(participantId, interaction, sessionId);

      // Update participant interaction history
      await this.updateParticipantInteractionHistory(participantId, processedInteraction);

      // Buffer for synchronization
      this.bufferDataUpdate(participantId, 'interaction', processedInteraction);

      // Emit to relevant components
      this.emitRealTimeUpdate('participant_interaction', {
        participantId,
        sessionId,
        interaction: processedInteraction,
        timestamp: Date.now()
      });

      logger.debug('👤 Participant interaction processed', {
        participantId,
        sessionId,
        interactionType: processedInteraction.type
      });

    } catch (error) {
      logger.error('❌ Failed to handle participant interaction', {
        participantId,
        sessionId,
        error: error.message
      });
    }
  }

  // Data processing methods
  async processEngagementData(participantId, engagementData, sessionId) {
    const timestamp = Date.now();
    
    // Get current participant profile for context
    const currentProfile = await this.getParticipantProfile(participantId);
    const previousEngagement = currentProfile?.engagement || {};

    // Calculate trend
    const trend = this.calculateEngagementTrend(
      previousEngagement.currentScore || 0.5,
      engagementData.score || 0.5
    );

    // Determine engagement level
    const level = this.determineEngagementLevel(engagementData.score || 0.5);

    // Calculate session progress
    const sessionProgress = await this.calculateSessionProgress(participantId, sessionId);

    return {
      timestamp,
      currentScore: engagementData.score || 0.5,
      previousScore: previousEngagement.currentScore || 0.5,
      trend,
      level,
      sessionProgress,
      rawData: engagementData,
      metadata: {
        interactionCount: engagementData.interactionCount || 0,
        timeOnTask: engagementData.timeOnTask || 0,
        focusEvents: engagementData.focusEvents || 0
      }
    };
  }

  async processTrustData(participantId, trustEvent, sessionId) {
    const timestamp = Date.now();
    
    // Get current trust profile
    const currentProfile = await this.getParticipantProfile(participantId);
    const previousTrust = currentProfile?.trust || { level: 0.5, events: [] };

    // Calculate new trust level based on event
    const trustImpact = this.calculateTrustImpact(trustEvent);
    const newTrustLevel = Math.max(0, Math.min(1, 
      previousTrust.level + trustImpact
    ));

    // Determine trust stage
    const trustStage = this.determineTrustStage(newTrustLevel);

    return {
      timestamp,
      type: trustEvent.type,
      impact: trustImpact,
      previousLevel: previousTrust.level,
      newTrustLevel,
      trustStage,
      eventData: trustEvent,
      metadata: {
        sessionId,
        eventContext: trustEvent.context || {}
      }
    };
  }

  async processInteractionData(participantId, interaction, sessionId) {
    const timestamp = Date.now();
    
    // Classify interaction type
    const classification = this.classifyInteraction(interaction);
    
    // Calculate interaction quality score
    const qualityScore = this.calculateInteractionQuality(interaction);

    return {
      timestamp,
      sessionId,
      type: interaction.type,
      classification,
      qualityScore,
      duration: interaction.duration || 0,
      details: interaction.details || {},
      metadata: {
        element: interaction.element,
        context: interaction.context || {},
        sequence: interaction.sequence || 0
      }
    };
  }

  async processProgressData(participantId, progressData, sessionId) {
    const timestamp = Date.now();
    
    // Calculate learning velocity
    const velocity = await this.calculateLearningVelocity(participantId, progressData);
    
    // Assess comprehension level
    const comprehension = this.assessComprehension(progressData);

    return {
      timestamp,
      sessionId,
      concept: progressData.concept,
      comprehension,
      velocity,
      attempts: progressData.attempts || 1,
      timeSpent: progressData.timeSpent || 0,
      successRate: progressData.successRate || 0
    };
  }

  async processAdaptationData(participantId, adaptationData, sessionId) {
    const timestamp = Date.now();
    
    return {
      timestamp,
      sessionId,
      adaptationId: adaptationData.adaptationId,
      strategy: adaptationData.strategy,
      trigger: adaptationData.trigger,
      effectiveness: null, // Will be calculated later
      metadata: adaptationData.metadata || {}
    };
  }

  // Data validation methods
  validateEngagementData(data) {
    const errors = [];
    
    if (typeof data.score !== 'number' || data.score < 0 || data.score > 1) {
      errors.push('Score must be a number between 0 and 1');
    }
    
    if (data.interactionCount && typeof data.interactionCount !== 'number') {
      errors.push('Interaction count must be a number');
    }
    
    if (data.timeOnTask && typeof data.timeOnTask !== 'number') {
      errors.push('Time on task must be a number');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  validateTrustData(data) {
    const errors = [];
    
    if (!data.type || typeof data.type !== 'string') {
      errors.push('Trust event type is required');
    }
    
    const validTypes = [
      'voluntary_interaction',
      'help_request',
      'mistake_acknowledgment',
      'preference_expression',
      'creative_sharing'
    ];
    
    if (data.type && !validTypes.includes(data.type)) {
      errors.push(`Trust event type must be one of: ${validTypes.join(', ')}`);
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  validateInteractionData(data) {
    const errors = [];
    
    if (!data.type || typeof data.type !== 'string') {
      errors.push('Interaction type is required');
    }
    
    if (data.duration && (typeof data.duration !== 'number' || data.duration < 0)) {
      errors.push('Duration must be a positive number');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  validateProgressData(data) {
    const errors = [];
    
    if (!data.concept || typeof data.concept !== 'string') {
      errors.push('Concept is required');
    }
    
    if (data.successRate && (typeof data.successRate !== 'number' || 
        data.successRate < 0 || data.successRate > 1)) {
      errors.push('Success rate must be a number between 0 and 1');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  validateAdaptationData(data) {
    const errors = [];
    
    if (!data.strategy || typeof data.strategy !== 'string') {
      errors.push('Adaptation strategy is required');
    }
    
    if (!data.trigger || typeof data.trigger !== 'string') {
      errors.push('Adaptation trigger is required');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  // Participant profile management
  async getParticipantProfile(participantId) {
    // Check cache first
    let profile = this.participantProfiles.get(participantId);
    
    if (!profile) {
      // Try to load from Redis
      if (this.redis) {
        try {
          const cachedProfile = await this.redis.get(`participant:${participantId}`);
          if (cachedProfile) {
            profile = JSON.parse(cachedProfile);
            this.participantProfiles.set(participantId, profile);
          }
        } catch (error) {
          logger.warn('Failed to load participant profile from Redis', {
            participantId,
            error: error.message
          });
        }
      }
      
      // Create default profile if not found
      if (!profile) {
        profile = this.createDefaultParticipantProfile(participantId);
        this.participantProfiles.set(participantId, profile);
      }
    }
    
    return profile;
  }

  createDefaultParticipantProfile(participantId) {
    return {
      participantId,
      createdAt: Date.now(),
      lastUpdated: Date.now(),
      engagement: {
        currentScore: 0.5,
        averageScore: 0.5,
        trend: 'stable',
        history: []
      },
      trust: {
        level: 0.5,
        stage: 'basic_comfort',
        events: [],
        growth: []
      },
      interactions: {
        total: 0,
        recent: [],
        patterns: {}
      },
      progress: {
        concepts: {},
        sessions: [],
        velocity: 0.5
      },
      adaptations: {
        total: 0,
        recent: [],
        effectiveness: {}
      }
    };
  }

  async updateParticipantEngagementProfile(participantId, engagementData) {
    const profile = await this.getParticipantProfile(participantId);
    
    // Update engagement section
    profile.engagement.currentScore = engagementData.currentScore;
    profile.engagement.trend = engagementData.trend;
    profile.engagement.lastUpdated = Date.now();
    
    // Add to history
    profile.engagement.history.push({
      timestamp: engagementData.timestamp,
      score: engagementData.currentScore,
      sessionProgress: engagementData.sessionProgress
    });
    
    // Keep only last 100 history points
    if (profile.engagement.history.length > 100) {
      profile.engagement.history = profile.engagement.history.slice(-100);
    }
    
    // Recalculate average
    profile.engagement.averageScore = this.calculateAverageEngagement(
      profile.engagement.history
    );
    
    // Update profile timestamp
    profile.lastUpdated = Date.now();
    
    // Update cache
    this.participantProfiles.set(participantId, profile);
  }

  async updateParticipantTrustProfile(participantId, trustData) {
    const profile = await this.getParticipantProfile(participantId);
    
    // Update trust section
    profile.trust.level = trustData.newTrustLevel;
    profile.trust.stage = trustData.trustStage;
    profile.trust.lastUpdated = Date.now();
    
    // Add event to history
    profile.trust.events.push({
      timestamp: trustData.timestamp,
      type: trustData.type,
      impact: trustData.impact,
      resultingLevel: trustData.newTrustLevel
    });
    
    // Keep only last 50 trust events
    if (profile.trust.events.length > 50) {
      profile.trust.events = profile.trust.events.slice(-50);
    }
    
    // Add to growth tracking
    profile.trust.growth.push({
      timestamp: trustData.timestamp,
      level: trustData.newTrustLevel
    });
    
    // Keep only last 100 growth points
    if (profile.trust.growth.length > 100) {
      profile.trust.growth = profile.trust.growth.slice(-100);
    }
    
    // Update profile timestamp
    profile.lastUpdated = Date.now();
    
    // Update cache
    this.participantProfiles.set(participantId, profile);
  }

  async updateParticipantInteractionHistory(participantId, interactionData) {
    const profile = await this.getParticipantProfile(participantId);
    
    // Update interactions section
    profile.interactions.total += 1;
    profile.interactions.lastUpdated = Date.now();
    
    // Add to recent interactions
    profile.interactions.recent.push({
      timestamp: interactionData.timestamp,
      type: interactionData.type,
      classification: interactionData.classification,
      qualityScore: interactionData.qualityScore
    });
    
    // Keep only last 50 interactions
    if (profile.interactions.recent.length > 50) {
      profile.interactions.recent = profile.interactions.recent.slice(-50);
    }
    
    // Update interaction patterns
    if (!profile.interactions.patterns[interactionData.type]) {
      profile.interactions.patterns[interactionData.type] = {
        count: 0,
        averageQuality: 0,
        lastSeen: null
      };
    }
    
    const pattern = profile.interactions.patterns[interactionData.type];
    pattern.count += 1;
    pattern.lastSeen = interactionData.timestamp;
    pattern.averageQuality = this.updateRunningAverage(
      pattern.averageQuality,
      interactionData.qualityScore,
      pattern.count
    );
    
    // Update profile timestamp
    profile.lastUpdated = Date.now();
    
    // Update cache
    this.participantProfiles.set(participantId, profile);
  }

  // Utility methods
  calculateEngagementTrend(previousScore, currentScore) {
    const diff = currentScore - previousScore;
    
    if (diff > 0.05) return 'increasing';
    if (diff < -0.05) return 'decreasing';
    return 'stable';
  }

  determineEngagementLevel(score) {
    if (score < 0.3) return 'low';
    if (score < 0.6) return 'medium';
    if (score < 0.8) return 'high';
    return 'very_high';
  }

  calculateTrustImpact(trustEvent) {
    const impactMap = {
      'voluntary_interaction': 0.05,
      'help_request': 0.08,
      'mistake_acknowledgment': 0.06,
      'preference_expression': 0.04,
      'creative_sharing': 0.10
    };
    
    return impactMap[trustEvent.type] || 0.02;
  }

  determineTrustStage(trustLevel) {
    if (trustLevel < 0.2) return 'initial_contact';
    if (trustLevel < 0.4) return 'basic_comfort';
    if (trustLevel < 0.6) return 'active_engagement';
    if (trustLevel < 0.8) return 'trust_dependency';
    return 'collaborative_partnership';
  }

  classifyInteraction(interaction) {
    const type = interaction.type?.toLowerCase() || '';
    
    if (type.includes('click')) return 'navigation';
    if (type.includes('input') || type.includes('text')) return 'content_creation';
    if (type.includes('help') || type.includes('hint')) return 'support_seeking';
    if (type.includes('submit') || type.includes('answer')) return 'response_submission';
    
    return 'general';
  }

  calculateInteractionQuality(interaction) {
    let score = 0.5; // Base score
    
    // Duration-based quality
    if (interaction.duration) {
      if (interaction.duration > 1000 && interaction.duration < 30000) { // 1-30 seconds
        score += 0.2; // Thoughtful interaction
      } else if (interaction.duration < 500) {
        score -= 0.1; // Too quick, might be random
      }
    }
    
    // Context-based quality
    if (interaction.context?.educational) {
      score += 0.2; // Educational content interaction
    }
    
    // Details-based quality
    if (interaction.details && Object.keys(interaction.details).length > 0) {
      score += 0.1; // Rich interaction with details
    }
    
    return Math.max(0, Math.min(1, score));
  }

  calculateAverageEngagement(history) {
    if (history.length === 0) return 0.5;
    
    const sum = history.reduce((total, item) => total + item.score, 0);
    return sum / history.length;
  }

  updateRunningAverage(currentAverage, newValue, count) {
    return ((currentAverage * (count - 1)) + newValue) / count;
  }

  async calculateSessionProgress(participantId, sessionId) {
    // This would integrate with session management to determine progress
    // For now, return a placeholder
    return {
      percentage: 0.5,
      timeElapsed: 0,
      activitiesCompleted: 0
    };
  }

  async calculateLearningVelocity(participantId, progressData) {
    // Calculate how quickly participant is learning based on progress data
    // This is a simplified implementation
    const timeSpent = progressData.timeSpent || 1;
    const successRate = progressData.successRate || 0.5;
    
    return successRate / (timeSpent / 60000); // Success per minute
  }

  assessComprehension(progressData) {
    const successRate = progressData.successRate || 0;
    const attempts = progressData.attempts || 1;
    
    // Simple comprehension assessment
    if (successRate > 0.8 && attempts <= 2) return 'excellent';
    if (successRate > 0.6) return 'good';
    if (successRate > 0.4) return 'developing';
    return 'needs_support';
  }

  // Data buffering and synchronization
  bufferDataUpdate(participantId, dataType, data) {
    if (!this.dataBuffer.has(participantId)) {
      this.dataBuffer.set(participantId, new Map());
    }
    
    const participantBuffer = this.dataBuffer.get(participantId);
    participantBuffer.set(dataType, {
      data,
      timestamp: Date.now()
    });
    
    // Check buffer size limits
    if (this.dataBuffer.size > this.maxBufferSize) {
      this.flushOldestBufferEntries();
    }
  }

  async flushDataBuffer() {
    if (this.dataBuffer.size === 0) return;
    
    const flushPromises = [];
    
    for (const [participantId, participantBuffer] of this.dataBuffer.entries()) {
      for (const [dataType, bufferedData] of participantBuffer.entries()) {
        const handler = this.dataHandlers.get(dataType);
        if (handler && handler.sync) {
          flushPromises.push(
            handler.sync(participantId, bufferedData.data).catch(error => {
              logger.error('Failed to sync buffered data', {
                participantId,
                dataType,
                error: error.message
              });
            })
          );
        }
      }
      
      // Clear participant buffer after processing
      participantBuffer.clear();
    }
    
    // Clear the main buffer
    this.dataBuffer.clear();
    
    // Wait for all sync operations
    await Promise.all(flushPromises);
    
    if (flushPromises.length > 0) {
      logger.debug('💾 Data buffer flushed', { operations: flushPromises.length });
    }
  }

  flushOldestBufferEntries() {
    // Remove oldest entries if buffer is too large
    const entries = Array.from(this.dataBuffer.entries());
    const toRemove = Math.floor(entries.length * 0.1); // Remove 10%
    
    for (let i = 0; i < toRemove; i++) {
      this.dataBuffer.delete(entries[i][0]);
    }
  }

  async synchronizeDataAcrossComponents() {
    // Persist participant profiles to Redis
    if (this.redis) {
      const profilePromises = [];
      
      for (const [participantId, profile] of this.participantProfiles.entries()) {
        profilePromises.push(
          this.redis.setEx(
            `participant:${participantId}`,
            86400, // 24 hour TTL
            JSON.stringify(profile)
          ).catch(error => {
            logger.error('Failed to persist participant profile', {
              participantId,
              error: error.message
            });
          })
        );
      }
      
      await Promise.all(profilePromises);
    }
    
    // Emit synchronization event for components
    this.emitRealTimeUpdate('data_sync_complete', {
      timestamp: Date.now(),
      profilesCount: this.participantProfiles.size
    });
  }

  // Data sync methods for each data type
  async syncEngagementData(participantId, data) {
    // Sync engagement data with external systems if needed
    logger.debug('Syncing engagement data', { participantId });
  }

  async syncTrustData(participantId, data) {
    // Sync trust data with external systems if needed
    logger.debug('Syncing trust data', { participantId });
  }

  async syncInteractionData(participantId, data) {
    // Sync interaction data with external systems if needed
    logger.debug('Syncing interaction data', { participantId });
  }

  async syncProgressData(participantId, data) {
    // Sync progress data with external systems if needed
    logger.debug('Syncing progress data', { participantId });
  }

  async syncAdaptationData(participantId, data) {
    // Sync adaptation data with external systems if needed
    logger.debug('Syncing adaptation data', { participantId });
  }

  // Real-time event emission
  emitRealTimeUpdate(eventType, data) {
    // Emit to WebSocket clients
    this.server.io.emit(eventType, data);
    
    // Emit to internal event system
    this.emit(eventType, data);
  }

  async assessImmediateAdaptationNeed(participantId, dataType, processedData) {
    // Quick assessment for immediate adaptation needs
    if (dataType === 'engagement' && processedData.currentScore < 0.3) {
      return {
        type: 'immediate',
        reason: 'critically_low_engagement',
        urgency: 'high'
      };
    }
    
    if (dataType === 'trust' && processedData.newTrustLevel < 0.2) {
      return {
        type: 'immediate',
        reason: 'trust_crisis',
        urgency: 'high'
      };
    }
    
    return null;
  }

  // Public API methods
  async getUnifiedParticipantProfile(participantId) {
    return await this.getParticipantProfile(participantId);
  }

  async updateParticipantProfile(participantId, updates) {
    const profile = await this.getParticipantProfile(participantId);
    
    // Apply updates
    Object.keys(updates).forEach(key => {
      if (profile[key] && typeof profile[key] === 'object') {
        profile[key] = { ...profile[key], ...updates[key] };
      } else {
        profile[key] = updates[key];
      }
    });
    
    profile.lastUpdated = Date.now();
    
    // Update cache
    this.participantProfiles.set(participantId, profile);
    
    // Emit update event
    this.emitRealTimeUpdate('participant_profile_updated', {
      participantId,
      updatedFields: Object.keys(updates),
      timestamp: Date.now()
    });
    
    return profile;
  }

  getDataStats() {
    return {
      participantProfiles: this.participantProfiles.size,
      bufferedUpdates: this.dataBuffer.size,
      dataHandlers: this.dataHandlers.size,
      redisConnected: !!this.redis?.isReady
    };
  }

  async closeConnections() {
    if (this.redis) {
      await this.redis.disconnect();
      logger.info('📡 Redis connection closed');
    }
  }
}

module.exports = DataCoordinator;
