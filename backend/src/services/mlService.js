const axios = require('axios');
const FormData = require('form-data');
const config = require('../config/env');
const logger = require('../utils/logger');

class MLService {
  /**
   * Forwards an image buffer to Python FastAPI ML service
   * @param {Buffer} buffer - Image file buffer
   * @param {string} filename - Original filename
   * @param {string} [crop] - Optional crop hint / selection
   * @returns {Promise<Object>} - Parsed ML prediction response
   */
  static async sendImageForPrediction(buffer, filename = 'crop_image.jpg', crop = null) {
    const startTime = Date.now();
    const endpoint = `${config.mlServiceUrl}/api/v1/predict`;

    const ext = (filename || '').toLowerCase();
    let contentType = 'image/jpeg';
    if (ext.endsWith('.webp')) {
      contentType = 'image/webp';
    } else if (ext.endsWith('.png')) {
      contentType = 'image/png';
    }

    const formData = new FormData();
    formData.append('image', buffer, {
      filename,
      contentType
    });
    if (crop) {
      formData.append('crop', crop);
    }

    try {
      const response = await axios.post(endpoint, formData, {
        headers: {
          ...formData.getHeaders()
        },
        timeout: 20000 // 20-second timeout for ML inference
      });

      const latency = Date.now() - startTime;
      logger.info(`ML prediction completed in ${latency}ms for ${filename}`);
      return response.data;
    } catch (error) {
      const latency = Date.now() - startTime;
      logger.error(`ML Service communication failed after ${latency}ms: ${error.message}`);

      if (error.response && error.response.data) {
        // If ML service returned structured response with standard success boolean
        if (typeof error.response.data === 'object' && error.response.data !== null && error.response.data.success !== undefined) {
          return error.response.data;
        }

        if (error.response.status === 429) {
          const err = new Error('The AI prediction service is experiencing high traffic. Please retry in a few moments.');
          err.code = 'ML_RATE_LIMITED';
          err.statusCode = 429;
          throw err;
        }

        const rawMsg = typeof error.response.data === 'string'
          ? error.response.data.trim()
          : (error.response.data.message || error.response.data.detail || 'ML microservice returned an error');

        const err = new Error(rawMsg);
        err.code = 'ML_SERVICE_ERROR';
        err.statusCode = error.response.status || 500;
        throw err;
      }

      if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
        const err = new Error('Prediction service is temporarily unavailable. Please verify ML microservice is running.');
        err.code = 'ML_SERVICE_UNAVAILABLE';
        err.statusCode = 503;
        throw err;
      }

      if (error.code === 'ECONNABORTED') {
        const err = new Error('Prediction request timed out. Please try again with a smaller image.');
        err.code = 'ML_TIMEOUT';
        err.statusCode = 504;
        throw err;
      }

      throw error;
    }
  }

  /**
   * Health check for ML microservice
   */
  static async checkHealth() {
    try {
      const res = await axios.get(`${config.mlServiceUrl}/health`, { timeout: 3000 });
      return res.data;
    } catch (err) {
      return { status: 'unreachable', error: err.message };
    }
  }
}

module.exports = MLService;
