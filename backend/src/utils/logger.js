const winston = require('winston');
const config = require('../config/env');

const sensitiveKeys = ['password', 'passwordHash', 'token', 'authorization', 'secret', 'apiKey'];

const maskSensitiveData = winston.format((info) => {
  if (info && typeof info === 'object') {
    for (const key of Object.keys(info)) {
      if (sensitiveKeys.some(sk => key.toLowerCase().includes(sk.toLowerCase()))) {
        info[key] = '[REDACTED]';
      }
    }
  }
  return info;
});

const logger = winston.createLogger({
  level: config.env === 'development' ? 'debug' : 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    maskSensitiveData(),
    winston.format.json()
  ),
  defaultMeta: { service: 'agrivision-backend' },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.printf(({ timestamp, level, message, ...meta }) => {
          const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
          return `[${timestamp}] [${level}] ${message}${metaStr}`;
        })
      )
    })
  ]
});

module.exports = logger;
