// integration_engine/components/component_registry.js
// Component Registry - Managing all PACT primitives with joy! ✨

const EventEmitter = require('events');
const logger = require('../utils/logger');

class ComponentRegistry extends EventEmitter {
  constructor(integrationServer) {
    super();
    this.server = integrationServer;
    this.config = integrationServer.config;
    
    // Component storage - where the magic lives! 🎭
    this.registeredComponents = new Map();
    this.componentTypes = new Map();
    this.heartbeatTimers = new Map();
    
    // Component capabilities and requirements
    this.componentDefinitions = {
      'creative_synthesis': {
        required: true,
        capabilities: ['experience_generation', 'adaptation_creation', 'personalization'],
        healthCheck: 'get_health_status',
        description: '🎨 The imagination powerhouse that creates magical learning experiences!',
        joyFactor: 'Creates wonder and transforms boring into brilliant! ✨'
      },
      'engagement_tracker': {
        required: true,
        capabilities: ['real_time_tracking', 'joy_detection', 'trust_monitoring'],
        healthCheck: 'get_engagement_status',
        description: '📊 The joy detection system that senses curiosity and excitement!',
        joyFactor: 'Turns data into celebration moments! 🎉'
      },
      'student_interface': {
        required: true,
        capabilities: ['content_display', 'interaction_capture', 'magic_delivery'],
        healthCheck: 'ping_with_sparkles',
        description: '🎪 The magical learning playground where students discover and explore!',
        joyFactor: 'Where learning adventures come alive! 🚀'
      },
      'teacher_dashboard': {
        required: false,
        capabilities: ['joy_analytics', 'classroom_celebration', 'insight_delivery'],
        healthCheck: 'get_celebration_status',
        description: '👩‍🏫 The command center for celebrating student breakthroughs!',
        joyFactor: 'Helps teachers witness and amplify the magic! 🌟'
      },
      'empathetic_interaction': {
        required: false,
        capabilities: ['emotional_intelligence', 'relationship_building', 'trust_cultivation'],
        healthCheck: 'get_empathy_pulse',
        description: '🤝 The heart system that builds genuine connections!',
        joyFactor: 'Makes AI feel like a caring friend! 💝'
      }
    };
    
    this.startHealthMonitoring();
    logger.info('🎭 Component Registry initialized with joy-driven architecture!');
  }

  async registerComponent(socket, registrationData) {
    const { componentType, componentId, capabilities = [], metadata = {} } = registrationData;
    
    logger.component(componentType, 'registration_attempt', {
      componentId,
      capabilities,
      socketId: socket.id
    });

    try {
      // Validate component type
      if (!this.componentDefinitions[componentType]) {
        throw new Error(`Unknown component type: ${componentType}. We need components that spark joy! ✨`);
      }

      const definition = this.componentDefinitions[componentType];
      
      // Check if component already registered
      const existingComponent = this.findComponentByType(componentType);
      if (existingComponent) {
        logger.warn(`Component type ${componentType} already registered, updating...`, {
          previousSocketId: existingComponent.socket.id,
          newSocketId: socket.id
        });
        await this.unregisterComponent(existingComponent.socket.id);
      }

      // Create component registration
      const component = {
        type: componentType,
        id: componentId,
        socket: socket,
        capabilities: capabilities,
        metadata: metadata,
        definition: definition,
        registeredAt: new Date(),
        lastHeartbeat: new Date(),
        status: 'connected',
        joyLevel: metadata.initialJoy || 0.8, // Start with high joy! 🎉
        connectionCount: 0,
        totalInteractions: 0
      };

      // Store the component
      this.registeredComponents.set(socket.id, component);
      this.componentTypes.set(componentType, component);

      // Set up heartbeat monitoring
      this.setupComponentHeartbeat(socket.id);

      // Send joyful welcome message
      const welcomeMessage = {
        status: 'registered',
        componentId,
        welcomeMessage: `🎉 Welcome, ${definition.description}`,
        joyNote: definition.joyFactor,
        systemStatus: this.getSystemReadiness(),
        availableComponents: this.getComponentSummary(),
        celebrationLevel: 'maximum' // Because every registration is a celebration! ✨
      };

      socket.emit('registration_confirmed', welcomeMessage);

      // Notify other components about the new friend!
      this.broadcastComponentEvent('joyful_arrival', {
        newComponent: {
          type: componentType,
          id: componentId,
          description: definition.description,
          joyFactor: definition.joyFactor
        },
        celebrationMessage: `🎊 ${componentType} just joined our magical system! Welcome to the joy! 🎊`
      });

      // Emit registration event
      this.emit('component_registered', component);

      logger.component(componentType, 'registered', {
        componentId,
        socketId: socket.id,
        joyLevel: component.joyLevel,
        systemReadiness: this.getSystemReadiness().ready
      });

      // If this completes our system, celebrate! 🎉
      const readiness = this.getSystemReadiness();
      if (readiness.ready && readiness.celebrationWorthy) {
        this.triggerSystemReadyCelebration();
      }

      return component;

    } catch (error) {
      logger.error('Component registration failed', {
        componentType,
        componentId,
        error: error.message,
        socketId: socket.id
      });
      
      socket.emit('registration_error', {
        error: error.message,
        helpfulMessage: 'Don\'t worry! Every great system has growing pains. Let\'s figure this out together! 💪'
      });
      
      throw error;
    }
  }

  async unregisterComponent(socketId) {
    const component = this.registeredComponents.get(socketId);
    if (!component) return;

    logger.component(component.type, 'unregistering', {
      componentId: component.id,
      socketId,
      wasConnectedFor: Date.now() - component.registeredAt.getTime()
    });

    // Clear heartbeat timer
    if (this.heartbeatTimers.has(socketId)) {
      clearInterval(this.heartbeatTimers.get(socketId));
      this.heartbeatTimers.delete(socketId);
    }

    // Remove from storage
    this.registeredComponents.delete(socketId);
    this.componentTypes.delete(component.type);

    // Notify other components
    this.broadcastComponentEvent('component_departure', {
      departedComponent: {
        type: component.type,
        id: component.id
      },
      farewellMessage: `👋 ${component.type} has left our system. Thanks for the joy you brought! 🌟`
    });

    // Emit unregistration event
    this.emit('component_unregistered', component);

    logger.component(component.type, 'unregistered', {
      componentId: component.id,
      gracefulDeparture: true
    });
  }

  handleDisconnection(socketId) {
    const component = this.registeredComponents.get(socketId);
    if (component) {
      logger.component(component.type, 'disconnected', {
        componentId: component.id,
        socketId,
        unexpectedDisconnection: true
      });
      
      this.unregisterComponent(socketId);
    }
  }

  findComponentByType(componentType) {
    return this.componentTypes.get(componentType) || null;
  }

  findComponentById(componentId) {
    for (const component of this.registeredComponents.values()) {
      if (component.id === componentId) {
        return component;
      }
    }
    return null;
  }

  getRegisteredComponents() {
    return Array.from(this.registeredComponents.values());
  }

  getComponentsByCapability(capability) {
    return Array.from(this.registeredComponents.values())
      .filter(component => component.capabilities.includes(capability));
  }

  setupComponentHeartbeat(socketId) {
    const component = this.registeredComponents.get(socketId);
    if (!component) return;

    // Set up heartbeat timer
    const heartbeatInterval = setInterval(async () => {
      try {
        await this.checkComponentHealth(component);
      } catch (error) {
        logger.error('Heartbeat check failed', {
          componentType: component.type,
          componentId: component.id,
          error: error.message
        });
        
        // Mark component as unhealthy
        component.status = 'unhealthy';
        component.lastError = error.message;
        
        // Notify system of unhealthy component
        this.emit('component_unhealthy', component);
      }
    }, this.config.components?.heartbeatInterval || 30000);

    this.heartbeatTimers.set(socketId, heartbeatInterval);
  }

  async checkComponentHealth(component) {
    const healthCheckMethod = component.definition.healthCheck;
    
    try {
      // Send health check request
      const healthData = await this.requestFromComponent(
        component, 
        healthCheckMethod, 
        { timestamp: Date.now(), joyCheck: true }
      );

      // Update component status
      component.lastHeartbeat = new Date();
      component.status = 'healthy';
      component.joyLevel = healthData.joyLevel || component.joyLevel;
      
      if (healthData.interactionCount) {
        component.totalInteractions = healthData.interactionCount;
      }

      return healthData;

    } catch (error) {
      component.status = 'unhealthy';
      component.lastError = error.message;
      throw error;
    }
  }

  async requestFromComponent(component, requestType, data = {}) {
    return new Promise((resolve, reject) => {
      const requestId = Math.random().toString(36).substr(2, 9);
      const timeout = this.config.components?.requestTimeout || 5000;
      
      // Set up response listener
      const responseHandler = (response) => {
        if (response.requestId === requestId) {
          component.socket.off('component_response', responseHandler);
          resolve(response.data);
        }
      };
      
      // Set up timeout
      const timeoutHandler = setTimeout(() => {
        component.socket.off('component_response', responseHandler);
        reject(new Error(`Component request timeout: ${requestType}`));
      }, timeout);
      
      component.socket.on('component_response', responseHandler);
      
      // Send the request
      component.socket.emit('component_request', {
        requestId,
        requestType,
        data,
        joyfulGreeting: `Hello from the joy-filled registry! 🌟`,
        timestamp: Date.now()
      });

      // Clear timeout when resolved/rejected
      const originalResolve = resolve;
      const originalReject = reject;
      
      resolve = (value) => {
        clearTimeout(timeoutHandler);
        originalResolve(value);
      };
      
      reject = (error) => {
        clearTimeout(timeoutHandler);
        originalReject(error);
      };
    });
  }

  broadcastComponentEvent(eventType, data) {
    const broadcastData = {
      eventType,
      timestamp: Date.now(),
      systemJoyLevel: this.calculateSystemJoyLevel(),
      ...data
    };

    this.registeredComponents.forEach(component => {
      if (component.socket && component.status === 'healthy') {
        component.socket.emit('system_event', broadcastData);
      }
    });

    logger.pactEvent(eventType, broadcastData);
  }

  getSystemReadiness() {
    const requiredComponents = Object.entries(this.componentDefinitions)
      .filter(([type, definition]) => definition.required)
      .map(([type]) => type);

    const registeredTypes = Array.from(this.componentTypes.keys());
    const missingRequired = requiredComponents.filter(type => !registeredTypes.includes(type));

    const readiness = {
      ready: missingRequired.length === 0,
      missingComponents: missingRequired,
      registeredComponents: registeredTypes,
      totalComponents: this.registeredComponents.size,
      systemJoyLevel: this.calculateSystemJoyLevel(),
      celebrationWorthy: missingRequired.length === 0 && registeredTypes.length >= 3
    };

    readiness.status = readiness.ready ? 
      (readiness.celebrationWorthy ? '🎉 SYSTEM READY FOR MAGIC!' : '✅ System Ready') : 
      '⚠️ Waiting for Components';

    return readiness;
  }

  getComponentSummary() {
    return Array.from(this.registeredComponents.values()).map(component => ({
      type: component.type,
      id: component.id,
      status: component.status,
      joyLevel: component.joyLevel,
      description: component.definition.description,
      capabilities: component.capabilities,
      connectedSince: component.registeredAt,
      totalInteractions: component.totalInteractions
    }));
  }

  calculateSystemJoyLevel() {
    const components = Array.from(this.registeredComponents.values());
    if (components.length === 0) return 0.5;

    const totalJoy = components.reduce((sum, component) => sum + component.joyLevel, 0);
    return Math.min(1.0, totalJoy / components.length);
  }

  triggerSystemReadyCelebration() {
    const celebrationData = {
      message: '🎊 ALL SYSTEMS GO! THE MAGIC IS READY TO BEGIN! 🎊',
      systemJoyLevel: this.calculateSystemJoyLevel(),
      readyComponents: this.getComponentSummary(),
      celebrationLevel: 'MAXIMUM',
      specialMessage: 'Every component is connected and ready to create learning magic! ✨'
    };

    this.broadcastComponentEvent('system_ready_celebration', celebrationData);

    logger.pactEvent('system_ready_celebration', {
      componentsReady: this.registeredComponents.size,
      systemJoyLevel: celebrationData.systemJoyLevel,
      readinessAchieved: true
    });

    // Emit to the main server for additional celebrations
    this.emit('system_ready', celebrationData);
  }

  startHealthMonitoring() {
    // Overall system health check every minute
    setInterval(() => {
      this.performSystemHealthCheck();
    }, this.config.components?.healthCheckInterval || 60000);

    logger.info('🏥 Component health monitoring started with care and attention!');
  }

  async performSystemHealthCheck() {
    const healthResults = {};
    const unhealthyComponents = [];

    for (const [socketId, component] of this.registeredComponents.entries()) {
      try {
        if (component.status !== 'healthy') {
          unhealthyComponents.push(component);
          continue;
        }

        // Check last heartbeat
        const timeSinceHeartbeat = Date.now() - component.lastHeartbeat.getTime();
        const heartbeatTimeout = this.config.components?.heartbeatTimeout || 45000;

        if (timeSinceHeartbeat > heartbeatTimeout) {
          component.status = 'stale';
          unhealthyComponents.push(component);
        }

        healthResults[component.type] = {
          status: component.status,
          joyLevel: component.joyLevel,
          lastSeen: component.lastHeartbeat,
          interactions: component.totalInteractions
        };

      } catch (error) {
        logger.error('Health check error', {
          componentType: component.type,
          error: error.message
        });
        unhealthyComponents.push(component);
      }
    }

    // Log system health summary
    if (unhealthyComponents.length > 0) {
      logger.warn('System health concerns detected', {
        unhealthyCount: unhealthyComponents.length,
        totalComponents: this.registeredComponents.size,
        unhealthyComponents: unhealthyComponents.map(c => ({
          type: c.type,
          id: c.id,
          status: c.status,
          issue: c.lastError || 'Heartbeat timeout'
        }))
      });
    } else if (this.registeredComponents.size > 0) {
      logger.debug('System health excellent', {
        healthyComponents: this.registeredComponents.size,
        averageJoyLevel: this.calculateSystemJoyLevel()
      });
    }

    return healthResults;
  }

  getComponentsStatus() {
    return {
      total: this.registeredComponents.size,
      byType: Object.fromEntries(
        Array.from(this.componentTypes.entries()).map(([type, component]) => [
          type, {
            status: component.status,
            joyLevel: component.joyLevel,
            id: component.id,
            connectedSince: component.registeredAt
          }
        ])
      ),
      systemReadiness: this.getSystemReadiness(),
      healthSummary: this.getHealthSummary()
    };
  }

  getHealthSummary() {
    const components = Array.from(this.registeredComponents.values());
    const healthy = components.filter(c => c.status === 'healthy').length;
    const unhealthy = components.filter(c => c.status === 'unhealthy').length;
    const stale = components.filter(c => c.status === 'stale').length;

    return {
      healthy,
      unhealthy,
      stale,
      total: components.length,
      averageJoyLevel: this.calculateSystemJoyLevel(),
      overallStatus: unhealthy > 0 ? 'degraded' : (stale > 0 ? 'warning' : 'excellent')
    };
  }

  // Joy-focused utility methods
  celebrateComponent(componentType, celebrationReason) {
    const component = this.findComponentByType(componentType);
    if (!component) return;

    component.joyLevel = Math.min(1.0, component.joyLevel + 0.1);

    const celebrationData = {
      componentType,
      celebrationReason,
      newJoyLevel: component.joyLevel,
      message: `🎉 Celebrating ${componentType}: ${celebrationReason}! 🎉`
    };

    this.broadcastComponentEvent('component_celebration', celebrationData);
    
    logger.pactEvent('component_celebration', celebrationData);
  }

  // Public API methods
  isSystemReady() {
    return this.getSystemReadiness().ready;
  }

  getAvailableCapabilities() {
    const capabilities = new Set();
    this.registeredComponents.forEach(component => {
      component.capabilities.forEach(cap => capabilities.add(cap));
    });
    return Array.from(capabilities);
  }

  async gracefulShutdown() {
    logger.info('🛑 Component Registry shutting down gracefully...');

    // Clear all heartbeat timers
    for (const timer of this.heartbeatTimers.values()) {
      clearInterval(timer);
    }
    this.heartbeatTimers.clear();

    // Notify all components of shutdown
    this.broadcastComponentEvent('system_shutdown', {
      message: '👋 System is shutting down. Thank you for all the joy and magic! 🌟',
      gracefulShutdown: true
    });

    // Clear component storage
    this.registeredComponents.clear();
    this.componentTypes.clear();

    logger.info('✅ Component Registry shutdown complete');
  }
}

module.exports = ComponentRegistry;
