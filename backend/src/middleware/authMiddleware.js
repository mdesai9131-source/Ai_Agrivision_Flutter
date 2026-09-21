const jwt = require('jsonwebtoken');
const config = require('../config/env');
const User = require('../models/User');
const ApiResponse = require('../utils/apiResponse');
const logger = require('../utils/logger');

const protect = async (req, res, next) => {
  let token;

  if (
    req.headers.authorization &&
    req.headers.authorization.startsWith('Bearer ')
  ) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return ApiResponse.error(
      res,
      'UNAUTHORIZED',
      'Authentication token is required to access this resource.',
      401
    );
  }

  try {
    const decoded = jwt.verify(token, config.jwtSecret);
    const user = await User.findById(decoded.id).select('-passwordHash');

    if (!user) {
      return ApiResponse.error(
        res,
        'USER_NOT_FOUND',
        'The user associated with this token no longer exists.',
        401
      );
    }

    req.user = user;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return ApiResponse.error(
        res,
        'TOKEN_EXPIRED',
        'Session expired. Please log in again.',
        401
      );
    }
    logger.warn(`JWT verification failure: ${err.message}`);
    return ApiResponse.error(
      res,
      'INVALID_TOKEN',
      'Provided authentication token is invalid.',
      401
    );
  }
};

/**
 * Protect middleware with graceful guest fallback:
 * If authenticated, attaches req.user.
 * If unauthenticated or token expired, seamlessly falls back to a Guest Farmer account
 * so crop diagnosis and agro center discovery are never blocked.
 */
const protectWithGuestFallback = async (req, res, next) => {
  let token;

  if (
    req.headers.authorization &&
    req.headers.authorization.startsWith('Bearer ')
  ) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (token) {
    try {
      const decoded = jwt.verify(token, config.jwtSecret);
      const user = await User.findById(decoded.id).select('-passwordHash');
      if (user) {
        req.user = user;
        return next();
      }
    } catch (err) {
      logger.info(`Session token fallback to guest mode: ${err.message}`);
    }
  }

  // Graceful Guest Farmer fallback
  try {
    let guestUser = await User.findOne({ email: 'guest.farmer@agrivision.internal' });
    if (!guestUser) {
      guestUser = await User.create({
        name: 'Field Farmer (Guest)',
        email: 'guest.farmer@agrivision.internal',
        passwordHash: '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890',
        phone: '+91 1800-180-1551',
        location: {
          latitude: 23.0040,
          longitude: 72.5087,
          city: 'Ahmedabad',
          state: 'Gujarat'
        }
      });
    }
    req.user = guestUser;
    next();
  } catch (guestErr) {
    logger.warn(`Using in-memory guest user: ${guestErr.message}`);
    req.user = {
      _id: '000000000000000000000000',
      name: 'Field Farmer (Guest)',
      email: 'guest.farmer@agrivision.internal'
    };
    next();
  }
};

module.exports = { protect, protectWithGuestFallback };
