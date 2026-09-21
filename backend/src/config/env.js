const dotenv = require('dotenv');
const path = require('path');

dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '5000', 10),
  mongoUri: process.env.MONGO_URI || 'mongodb://localhost:27017/ai_agrivision',
  jwtSecret: process.env.JWT_SECRET || 'agrivision_default_dev_jwt_secret_key_2026',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '7d',
  mlServiceUrl: process.env.ML_SERVICE_URL || 'http://localhost:8000',
  cloudinary: {
    cloudName: process.env.CLOUDINARY_CLOUD_NAME || process.env.CLOUD_NAME || '',
    apiKey: process.env.CLOUDINARY_API_KEY || process.env.CLOUD_KEY || '',
    apiSecret: process.env.CLOUDINARY_API_SECRET || process.env.CLOUD_SECRET || '',
    isConfigured: Boolean(
      (process.env.CLOUDINARY_CLOUD_NAME || process.env.CLOUD_NAME) &&
      (process.env.CLOUDINARY_API_KEY || process.env.CLOUD_KEY) &&
      (process.env.CLOUDINARY_API_SECRET || process.env.CLOUD_SECRET)
    )
  },
  maps: {
    apiKey: process.env.MAPS_API_KEY || ''
  },
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000', 10),
    max: parseInt(process.env.RATE_LIMIT_MAX || '100', 10)
  }
};

module.exports = config;
