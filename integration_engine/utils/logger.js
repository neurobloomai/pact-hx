// integration_engine/utils/logger.js
// Winston-based logging utility for PACT Integration Engine

const winston = require('winston');
const path = require('path');

// Create logs directory if it doesn't exist
const fs = require('fs');
const logsDir = path.join(__dirname, '../../logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// Custom format for PACT logs
const pactFormat = winston.format.combine(
  winston.format.timestamp({
    format: 'YYYY-MM-DD HH:mm:ss.SSS'
  }),
  winston.format.errors({ stack: true }),
  winston.format.json(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const logObject = {
      timestamp,
      level,
      message,
      service: 'pact-integration-engine',
      ...meta
    };
    return JSON.stringify(logObject);
  })
);

// Console format for development
const consoleFormat = winston.format.combine(
  winston.format.timestamp({
    format: 'HH:mm:ss'
  }),
  winston.format.colorize(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
    return `${timestamp} ${level}: ${message}${metaStr}`;
  })
);

// Create the logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: pactFormat,
  defaultMeta: {
    service: 'pact-integration-engine',
    version: '1.0.0'
  },
  transports: [
    // File transport for all logs
    new winston.transports.File({
      filename: path.join(logsDir, 'pact-integration.log'),
      maxsize: 20 * 1024 * 1024, // 20MB
      maxFiles: 5,
      tailable: true
    }),
    
    // Separate file for errors
    new winston.transports.File({
      filename: path.join(logsDir, 'pact-errors.log'),
      level: 'error',
      maxsize: 20 * 1024 * 1024, // 20MB
      maxFiles: 3,
      tailable: true
    }),
    
    // Separate file for debug logs in development
    ...(process.env.NODE_ENV === 'development' ? [
      new winston.transports.File({
        filename: path.join(logsDir, 'pact-debug.log'),
        level: 'debug',
        maxsize: 10 * 1024 * 1024, // 10MB
        maxFiles: 2,
        tailable: true
      })
    ] : [])
  ],
  
  // Handle uncaught exceptions and rejections
  exceptionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'pact-exceptions.log')
    })
  ],
  
  rejectionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'pact-rejections.log')
    })
  ]
});

// Add console transport for development
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: consoleFormat,
    level: process.env.LOG_LEVEL || 'debug'
  }));
}

// Custom logging methods for PACT-specific events
logger.pactEvent = (eventType, data = {}) => {
  logger.info(`PACT Event: ${eventType}`, {
    eventType,
    timestamp: Date.now(),
    ...data
  });
};

logger.adaptation = (studentId, adaptationType, details = {}) => {
  logger.info('Adaptation Triggered', {
    type: 'adaptation',
    studentId,
    adaptationType,
    timestamp: Date.now(),
    ...details
  });
};

logger.engagement = (studentId, score, metadata = {}) => {
  logger.debug('Engagement Update', {
    type: 'engagement',
    studentId,
    score,
    timestamp: Date.now(),
    ...metadata
  });
};

logger.trust = (studentId, level, event = {}) => {
  logger.debug('Trust Event', {
    type: 'trust',
    studentId,
    level,
    timestamp: Date.now(),
    ...event
  });
};

logger.session = (sessionId, action, details = {}) => {
  logger.info(`Session ${action}`, {
    type: 'session',
    sessionId,
    action,
    timestamp: Date.now(),
    ...details
  });
};

logger.component = (componentType, action, details = {}) => {
  logger.info(`Component ${action}`, {
    type: 'component',
    componentType,
    action,
    timestamp: Date.now(),
    ...details
  });
};

logger.performance = (operation, duration, metadata = {}) => {
  logger.debug('Performance Metric', {
    type: 'performance',
    operation,
    duration,
    timestamp: Date.now(),
    ...metadata
  });
};

logger.security = (event, details = {}) => {
  logger.warn('Security Event', {
    type: 'security',
    event,
    timestamp: Date.now(),
    ...details
  });
};

// Method to create child loggers for specific components
logger.createChild = (componentName, additionalMeta = {}) => {
  return logger.child({
    component: componentName,
    ...additionalMeta
  });
};

// Method to temporarily change log level
logger.setLevel = (level) => {
  logger.transports.forEach(transport => {
    transport.level = level;
  });
  logger.info(`Log level changed to: ${level}`);
};

// Method to flush logs (useful for testing)
logger.flush = () => {
  return new Promise((resolve) => {
    let pending = 0;
    logger.transports.forEach(transport => {
      if (transport.write) {
        pending++;
        transport.write('', 'utf8', () => {
          pending--;
          if (pending === 0) resolve();
        });
      }
    });
    if (pending === 0) resolve();
  });
};

// Graceful shutdown
logger.shutdown = () => {
  return new Promise((resolve) => {
    logger.end(() => {
      resolve();
    });
  });
};

module.exports = logger;
