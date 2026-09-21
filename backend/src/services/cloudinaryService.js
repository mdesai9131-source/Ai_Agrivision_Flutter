const cloudinary = require('../config/cloudinary');
const config = require('../config/env');
const logger = require('../utils/logger');

class CloudinaryService {
  /**
   * Uploads an image buffer to Cloudinary.
   * If Cloudinary is not configured, provides a mock data URL so the pipeline remains functional.
   * @param {Buffer} buffer - File buffer
   * @param {string} originalname - Original filename
   * @returns {Promise<string>} - Secure URL of uploaded image
   */
  static async uploadImageBuffer(buffer, originalname = 'crop_image.jpg') {
    if (!config.cloudinary.isConfigured) {
      logger.info('Cloudinary not configured with credentials. Generating mock storage URL for development.');
      const base64 = buffer.toString('base64');
      const ext = (originalname || '').toLowerCase();
      let mime = 'image/jpeg';
      if (ext.endsWith('.webp')) {
        mime = 'image/webp';
      } else if (ext.endsWith('.png')) {
        mime = 'image/png';
      }
      // In local dev, store as base64 data URI or simulated CDN URL
      return `data:${mime};base64,${base64.substring(0, 100)}...mock_crop_asset`;
    }

    return new Promise((resolve, reject) => {
      const uploadStream = cloudinary.uploader.upload_stream(
        {
          folder: 'ai_agrivision/crops',
          resource_type: 'image',
          allowed_formats: ['jpg', 'png', 'webp', 'jpeg'],
          transformation: [
            { quality: 'auto:good' },
            { fetch_format: 'auto' }
          ]
        },
        (error, result) => {
          if (error) {
            logger.error(`Cloudinary upload failed: ${error.message}`);
            return reject(new Error(`Cloudinary upload error: ${error.message}`));
          }
          logger.info(`Image uploaded to Cloudinary: ${result.secure_url}`);
          resolve(result.secure_url);
        }
      );

      uploadStream.end(buffer);
    });
  }
}

module.exports = CloudinaryService;
