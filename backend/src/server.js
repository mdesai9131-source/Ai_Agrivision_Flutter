const app = require('./app');
const config = require('./config/env');
const connectDB = require('./config/db');
const logger = require('./utils/logger');

// Initialize database connection and start server
connectDB();

const server = app.listen(config.port, () => {
  logger.info(`AI-AgriVision Server running in ${config.env} mode on port ${config.port}`);
});

// Graceful Shutdown Handlers
const handleShutdown = (signal) => {
  logger.info(`${signal} received. Closing HTTP server and database connections...`);
  server.close(() => {
    logger.info('HTTP server closed successfully.');
    process.exit(0);
  });

  // Force close after 10s if hanging
  setTimeout(() => {
    logger.error('Forcefully terminating process after timeout.');
    process.exit(1);
  }, 10000);
};

process.on('SIGTERM', () => handleShutdown('SIGTERM'));
process.on('SIGINT', () => handleShutdown('SIGINT'));

process.on('unhandledRejection', (err) => {
  logger.error(`Unhandled Rejection: ${err.message}`, { stack: err.stack });
});

process.on('uncaughtException', (err) => {
  logger.error(`Uncaught Exception: ${err.message}`, { stack: err.stack });
  process.exit(1);
});
