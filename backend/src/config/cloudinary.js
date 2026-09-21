const cloudinary = require('cloudinary').v2;
const config = require('./env');
const logger = require('../utils/logger');

if (config.cloudinary.isConfigured) {
  cloudinary.config({
    cloud_name: config.cloudinary.cloudName,
    api_key: config.cloudinary.apiKey,
    api_secret: config.cloudinary.apiSecret,
    secure: true
  });
  logger.info('Cloudinary initialized in secure mode.');
} else {
  logger.warn('Cloudinary environment variables missing. Operating in local buffer mock mode.');
}

module.exports = cloudinary;
