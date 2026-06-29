// Minimal PACT Integration Server - Getting the magic started! ✨

const express = require('express');
const { Server } = require('socket.io');
const http = require('http');
const cors = require('cors');

// Simple logger until we get the full one working
const simpleLogger = {
  info: (msg, meta) => console.log(`ℹ️  ${msg}`, meta || ''),
  error: (msg, meta) => console.error(`❌ ${msg}`, meta || ''),
  warn: (msg, meta) => console.warn(`⚠️  ${msg}`, meta || ''),
  debug: (msg, meta) => console.log(`🔍 ${msg}`, meta || '')
};

class MinimalPACTServer {
  constructor() {
    this.config = {
      port: process.env.PORT || 3001,
      apiPort: process.env.API_PORT || 3000,
      environment: process.env.NODE_ENV || 'development'
    };

    this.app = express();
    this.server = http.createServer(this.app);
    this.io = new Server(this.server, {
      cors: {
        origin: "*",
        methods: ["GET", "POST"]
      }
    });

    this.setupBasicMiddleware();
    this.setupBasicRoutes();
    this.setupWebSocket();
  }

  setupBasicMiddleware() {
    this.app.use(cors());
    this.app.use(express.json());
    
    // Request logging
    this.app.use((req, res, next) => {
      simpleLogger.info(`${req.method} ${req.path}`);
      next();
    });
  }

  setupBasicRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        message: '🎉 PACT Integration Engine is alive and magical!',
        timestamp: new Date().toISOString(),
        version: '1.0.0-minimal'
      });
    });

    // System status
    this.app.get('/status', (req, res) => {
      res.json({
        server: {
          name: 'PACT Integration Engine (Minimal)',
          version: '1.0.0-minimal',
          environment: this.config.environment,
          uptime: process.uptime()
        },
        magical: true
      });
    });

    // Basic session endpoint
    this.app.post('/api/sessions', (req, res) => {
      const sessionId = `minimal-session-${Date.now()}`;
      res.json({
        success: true,
        sessionId,
        message: '🎭 Minimal session created - full magic coming soon!',
        participantId: req.body.participantId,
        learningObjective: req.body.learningObjective
      });
    });
  }

  setupWebSocket() {
    this.io.on('connection', (socket) => {
      simpleLogger.info(`🔗 WebSocket connected: ${socket.id}`);
      
      socket.emit('welcome', {
        message: '✨ Welcome to PACT Integration Engine!',
        socketId: socket.id,
        magical: true
      });

      socket.on('register_component', (data) => {
        simpleLogger.info(`📝 Component registration: ${data.componentType}`);
        socket.emit('registration_confirmed', {
          message: '🎉 Component registered successfully!',
          componentType: data.componentType
        });
      });

      socket.on('disconnect', () => {
        simpleLogger.info(`🔌 WebSocket disconnected: ${socket.id}`);
      });
    });
  }

  async start() {
    try {
      this.server.listen(this.config.port, () => {
        simpleLogger.info(`🚀 PACT Integration Engine (Minimal) started!`, {
          port: this.config.port,
          environment: this.config.environment
        });
        simpleLogger.info(`🌐 Health check: http://localhost:${this.config.port}/health`);
        simpleLogger.info(`📊 Status: http://localhost:${this.config.port}/status`);
        simpleLogger.info(`🎭 Ready for magical learning sessions!`);
      });
    } catch (error) {
      simpleLogger.error('Failed to start server', error.message);
      throw error;
    }
  }

  async shutdown() {
    simpleLogger.info('🛑 Shutting down PACT Integration Engine...');
    this.io.close();
    this.server.close();
    simpleLogger.info('✅ Shutdown complete');
  }
}

// Start the minimal server
if (require.main === module) {
  const server = new MinimalPACTServer();
  
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
    console.error('❌ Failed to start server:', error.message);
    process.exit(1);
  });
}

module.exports = MinimalPACTServer;
