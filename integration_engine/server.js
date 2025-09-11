// integration_engine/server.js
// Main PACT Integration Engine Server - Entry Point

const express = require('express');
const { Server } = require('socket.io');
const http = require('http');
const cors = require('cors');
const helmet = require('helmet');
const winston = require('winston');
const path = require('path');

// Import our modular components
const PACTOrchestrator = require('./components/pact_orchestrator');
const ComponentRegistry = require('./components/component_registry');
const SessionManager = require('./components/session_manager');
const DataCoordinator = require('./components/data_coordinator');
const AdaptationEngine = require('./components/adaptation_engine');

// Import API routes
const sessionRoutes = require('./routes/sessions');
const studentRoutes = require('./routes/students');
const adaptationRoutes = require('./routes/adaptations');
const analyticsRoutes = require('./routes/analytics');

// Import configuration
const config = require('./config/default.json');

// Import utilities
const logger = require('./utils/logger');
const { validateEnvironment } = require('./utils/validation');

class PACTIntegrationServer {
  constructor(options = {}) {
    // Merge configuration
    this.config = {
      ...config,
      ...options,
      port: options.port || process.env.PORT || 3001,
      apiPort: options.apiPort || process.env.API_PORT || 3000,
      environment: process.env.NODE_ENV || 'development'
    };

    // Initialize Express app
    this.app = express();
    this.server = http.createServer(this.app);
    
    // Initialize Socket.IO
    this.io = new Server(this.server, {
      cors: {
        origin: this.config.cors.origins,
        methods: ['GET', 'POST', 'PUT', 'DELETE'],
        credentials: true
      }
    });

    // Initialize core components
    this.componentRegistry = new ComponentRegistry(this);
    this.sessionManager = new SessionManager(this);
    this.dataCoordinator = new DataCoordinator(this);
    this.adaptationEngine = new AdaptationEngine(this);
    this.orchestrator = new PACTOrchestrator(this);

    // Setup middleware and routes
    this.setupMiddleware();
    this.setupRoutes();
    this.setupWebSocketHandlers();
    this.setupErrorHandling();

    logger.info('🧠 PACT Integration Server initialized', {
      environment: this.config.environment,
      port: this.config.port,
      apiPort: this.config.apiPort
    });
  }

  setupMiddleware() {
    // Security middleware
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "'unsafe-inline'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          imgSrc: ["'self'", "data:", "https:"],
        },
      },
    }));

    // CORS configuration
    this.app.use(cors({
      origin: this.config.cors.origins,
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
    }));

    // Body parsing
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));

    // Request logging
    this.app.use((req, res, next) => {
      logger.info(`${req.method} ${req.path}`, {
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        timestamp: new Date().toISOString()
      });
      next();
    });

    // Static file serving (for demo purposes)
    this.app.use('/static', express.static(path.join(__dirname, 'public')));
  }

  setupRoutes() {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      const health = this.getSystemHealth();
      res.status(health.status === 'healthy' ? 200 : 503).json(health);
    });

    // System status endpoint
    this.app.get('/status', (req, res) => {
      res.json(this.getSystemStatus());
    });

    // API routes
    this.app.use('/api/sessions', sessionRoutes(this));
    this.app.use('/api/students', studentRoutes(this));
    this.app.use('/api/adaptations', adaptationRoutes(this));
    this.app.use('/api/analytics', analyticsRoutes(this));

    // WebSocket endpoint info
    this.app.get('/api/websocket', (req, res) => {
      res.json({
        url: `ws://localhost:${this.config.port}`,
        events: this.getWebSocketEventsList(),
        documentation: '/api/docs/websocket'
      });
    });

    // API documentation
    this.app.get('/api/docs', (req, res) => {
      res.json({
        title: 'PACT Integration Engine API',
        version: '1.0.0',
        endpoints: this.getAPIEndpointsList(),
        websocket: this.getWebSocketEventsList()
      });
    });

    // Catch-all route for undefined endpoints
    this.app.use('*', (req, res) => {
      res.status(404).json({
        error: 'Endpoint not found',
        message: `${req.method} ${req.originalUrl} is not a valid endpoint`,
        availableEndpoints: '/api/docs'
      });
    });
  }

  setupWebSocketHandlers() {
    this.io.on('connection', (socket) => {
      logger.info(`🔗 WebSocket connection established: ${socket.id}`, {
        socketId: socket.id,
        timestamp: new Date().toISOString()
      });

      // Component registration
      socket.on('register_component', async (data) => {
        try {
          await this.componentRegistry.registerComponent(socket, data);
        } catch (error) {
          logger.error('Component registration failed', { error: error.message, socketId: socket.id });
          socket.emit('registration_error', { error: error.message });
        }
      });

      // Session management events
      socket.on('session_start_request', async (data) => {
        try {
          const session = await this.sessionManager.createSession(data);
          socket.emit('session_started', session);
        } catch (error) {
          logger.error('Session start failed', { error: error.message, data });
          socket.emit('session_error', { error: error.message });
        }
      });

      // Real-time data events
      socket.on('engagement_update', async (data) => {
        try {
          await this.dataCoordinator.handleEngagementUpdate(socket, data);
        } catch (error) {
          logger.error('Engagement update failed', { error: error.message, data });
        }
      });

      socket.on('trust_event', async (data) => {
        try {
          await this.dataCoordinator.handleTrustEvent(socket, data);
        } catch (error) {
          logger.error('Trust event handling failed', { error: error.message, data });
        }
      });

      socket.on('student_interaction', async (data) => {
        try {
          await this.dataCoordinator.handleStudentInteraction(socket, data);
        } catch (error) {
          logger.error('Student interaction handling failed', { error: error.message, data });
        }
      });

      // Adaptation requests
      socket.on('adaptation_request', async (data) => {
        try {
          const adaptation = await this.adaptationEngine.processAdaptationRequest(data);
          socket.emit('adaptation_response', adaptation);
        } catch (error) {
          logger.error('Adaptation request failed', { error: error.message, data });
          socket.emit('adaptation_error', { error: error.message });
        }
      });

      // Teacher dashboard requests
      socket.on('teacher_request', async (data) => {
        try {
          const response = await this.orchestrator.handleTeacherRequest(data);
          socket.emit('teacher_response', response);
        } catch (error) {
          logger.error('Teacher request failed', { error: error.message, data });
          socket.emit('teacher_error', { error: error.message });
        }
      });

      // Component health checks
      socket.on('component_heartbeat', (data) => {
        this.componentRegistry.updateComponentHeartbeat(socket.id, data);
      });

      // Disconnection handling
      socket.on('disconnect', (reason) => {
        logger.info(`🔌 WebSocket disconnected: ${socket.id}`, {
          socketId: socket.id,
          reason,
          timestamp: new Date().toISOString()
        });
        this.componentRegistry.handleDisconnection(socket.id);
      });

      // Error handling
      socket.on('error', (error) => {
        logger.error('WebSocket error', {
          socketId: socket.id,
          error: error.message,
          stack: error.stack
        });
      });
    });
  }

  setupErrorHandling() {
    // Global error handler
    this.app.use((error, req, res, next) => {
      logger.error('Unhandled API error', {
        error: error.message,
        stack: error.stack,
        url: req.url,
        method: req.method
      });

      res.status(error.status || 500).json({
        error: 'Internal server error',
        message: this.config.environment === 'development' ? error.message : 'Something went wrong',
        requestId: req.headers['x-request-id'] || 'unknown'
      });
    });

    // Global promise rejection handler
    process.on('unhandledRejection', (reason, promise) => {
      logger.error('Unhandled promise rejection', {
        reason: reason.toString(),
        stack: reason.stack
      });
    });

    // Global exception handler
    process.on('uncaughtException', (error) => {
      logger.error('Uncaught exception', {
        error: error.message,
        stack: error.stack
      });
      
      // Graceful shutdown
      this.shutdown().then(() => {
        process.exit(1);
      });
    });
  }

  getSystemHealth() {
    const components = this.componentRegistry.getRegisteredComponents();
    const sessions = this.sessionManager.getActiveSessions();
    
    return {
      status: this.determineOverallHealth(),
      timestamp: new Date().toISOString(),
      components: {
        registered: components.length,
        healthy: components.filter(c => c.status === 'healthy').length,
        unhealthy: components.filter(c => c.status !== 'healthy').length
      },
      sessions: {
        active: sessions.length,
        total: this.sessionManager.getTotalSessionsCount()
      },
      memory: process.memoryUsage(),
      uptime: process.uptime()
    };
  }

  getSystemStatus() {
    return {
      server: {
        name: 'PACT Integration Engine',
        version: '1.0.0',
        environment: this.config.environment,
        startTime: this.startTime,
        uptime: Date.now() - this.startTime
      },
      components: this.componentRegistry.getComponentsStatus(),
      sessions: this.sessionManager.getSessionsOverview(),
      adaptation: this.adaptationEngine.getAdaptationStats(),
      data: this.dataCoordinator.getDataStats()
    };
  }

  determineOverallHealth() {
    const requiredComponents = ['creative_synthesis', 'engagement_tracker'];
    const registeredComponents = this.componentRegistry.getRegisteredComponents();
    const registeredTypes = registeredComponents.map(c => c.type);
    
    const missingRequired = requiredComponents.filter(type => 
      !registeredTypes.includes(type)
    );

    if (missingRequired.length === 0) {
      return 'healthy';
    } else if (missingRequired.length < requiredComponents.length) {
      return 'degraded';
    } else {
      return 'unhealthy';
    }
  }

  getWebSocketEventsList() {
    return {
      client_to_server: [
        'register_component',
        'session_start_request',
        'engagement_update',
        'trust_event',
        'student_interaction',
        'adaptation_request',
        'teacher_request',
        'component_heartbeat'
      ],
      server_to_client: [
        'registration_confirmed',
        'session_started',
        'engagement_update_processed',
        'adaptation_triggered',
        'teacher_response',
        'system_notification'
      ]
    };
  }

  getAPIEndpointsList() {
    return [
      { method: 'GET', path: '/health', description: 'System health check' },
      { method: 'GET', path: '/status', description: 'Detailed system status' },
      { method: 'POST', path: '/api/sessions', description: 'Create new learning session' },
      { method: 'GET', path: '/api/sessions/:id', description: 'Get session details' },
      { method: 'GET', path: '/api/students/:id/profile', description: 'Get unified student profile' },
      { method: 'POST', path: '/api/adaptations/trigger', description: 'Trigger manual adaptation' },
      { method: 'GET', path: '/api/analytics/classroom/:id', description: 'Get classroom analytics' }
    ];
  }

  async start() {
    try {
      // Validate environment
      validateEnvironment();

      // Initialize external connections
      await this.dataCoordinator.initializeConnections();
      await this.adaptationEngine.initialize();

      // Start the server
      this.server.listen(this.config.port, () => {
        this.startTime = Date.now();
        logger.info(`🚀 PACT Integration Engine started`, {
          port: this.config.port,
          environment: this.config.environment,
          timestamp: new Date().toISOString()
        });
      });

      // Start health monitoring
      this.startHealthMonitoring();

      return this;
    } catch (error) {
      logger.error('Failed to start PACT Integration Engine', {
        error: error.message,
        stack: error.stack
      });
      throw error;
    }
  }

  startHealthMonitoring() {
    // Check system health every 30 seconds
    setInterval(() => {
      const health = this.getSystemHealth();
      if (health.status !== 'healthy') {
        logger.warn('System health degraded', health);
      }
    }, 30000);

    // Component heartbeat check every 60 seconds
    setInterval(() => {
      this.componentRegistry.checkComponentHealth();
    }, 60000);
  }

  async shutdown() {
    logger.info('🛑 Shutting down PACT Integration Engine...');

    try {
      // Close all active sessions
      await this.sessionManager.closeAllSessions();

      // Disconnect from external services
      await this.dataCoordinator.closeConnections();

      // Close WebSocket connections
      this.io.close();

      // Close HTTP server
      await new Promise((resolve) => {
        this.server.close(resolve);
      });

      logger.info('✅ PACT Integration Engine shutdown complete');
    } catch (error) {
      logger.error('Error during shutdown', {
        error: error.message,
        stack: error.stack
      });
    }
  }
}

// Initialize and start server if this file is run directly
if (require.main === module) {
  const server = new PACTIntegrationServer();
  
  // Graceful shutdown handlers
  process.on('SIGTERM', async () => {
    await server.shutdown();
    process.exit(0);
  });
  
  process.on('SIGINT', async () => {
    await server.shutdown();
    process.exit(0);
  });

  // Start the server
  server.start().catch((error) => {
    logger.error('Failed to start server', { error: error.message });
    process.exit(1);
  });
}

module.exports = PACTIntegrationServer;
