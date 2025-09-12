const logger = require('./logger');

const validateEnvironment = () => {
  const required = ['NODE_ENV'];
  const missing = required.filter(env => !process.env[env]);
  
  if (missing.length > 0) {
    logger.warn('🔧 Some environment variables are missing (using defaults)', {
      missing,
      suggestion: 'Create a .env file for production use!'
    });
  }
  
  logger.info('✅ Environment validation complete');
};

module.exports = {
  validateEnvironment
};
