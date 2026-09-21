const config = require('../config/env');
const logger = require('../utils/logger');
const ApiResponse = require('../utils/apiResponse');

const errorHandler = (err, req, res, next) => {
  let statusCode = res.statusCode === 200 ? 500 : res.statusCode;
  let code = err.code || 'INTERNAL_SERVER_ERROR';
  let message = err.message || 'An unexpected server error occurred.';
  let details = null;

  // Log error with request info
  logger.error(`Error on ${req.method} ${req.originalUrl}: ${err.message}`, {
    stack: config.env === 'development' ? err.stack : undefined
  });

  // Mongoose Bad ObjectId (CastError)
  if (err.name === 'CastError') {
    statusCode = 400;
    code = 'RESOURCE_NOT_FOUND';
    message = `Resource not found with id ${err.value}`;
  }

  // Mongoose Validation Error
  if (err.name === 'ValidationError') {
    statusCode = 400;
    code = 'VALIDATION_ERROR';
    message = 'Validation failed for request data.';
    details = Object.values(err.errors).map(val => val.message);
  }

  // Mongoose Duplicate Key Error (E11000)
  if (err.code === 11000) {
    statusCode = 409;
    code = 'DUPLICATE_KEY';
    const field = Object.keys(err.keyValue)[0];
    message = `An account or record with that ${field} already exists.`;
  }

  // Multer File Size Limit Error
  if (err.code === 'LIMIT_FILE_SIZE') {
    statusCode = 413;
    code = 'FILE_TOO_LARGE';
    message = 'Uploaded image file exceeds the 10MB limit.';
  }

  // Multer Unsupported Format
  if (err.code === 'UNSUPPORTED_IMAGE_FORMAT') {
    statusCode = 400;
    code = 'UNSUPPORTED_IMAGE_FORMAT';
    message = err.message;
  }

  // Build safe response payload (never leak stack trace in production)
  return ApiResponse.error(res, code, message, statusCode, details);
};

const notFoundHandler = (req, res, next) => {
  return ApiResponse.error(
    res,
    'NOT_FOUND',
    `Cannot ${req.method} ${req.originalUrl}`,
    404
  );
};

module.exports = { errorHandler, notFoundHandler };
