const jwt = require('jsonwebtoken');
const User = require('../models/User');
const config = require('../config/env');
const ApiResponse = require('../utils/apiResponse');
const logger = require('../utils/logger');

const generateToken = (id) => {
  return jwt.sign({ id }, config.jwtSecret, {
    expiresIn: config.jwtExpiresIn
  });
};

/**
 * @desc    Register a new farmer account
 * @route   POST /api/v1/auth/register
 * @access  Public
 */
const register = async (req, res, next) => {
  try {
    const { name, email, password, phone, location } = req.body;

    if (!name || !email || !password) {
      return ApiResponse.error(
        res,
        'MISSING_FIELDS',
        'Please provide name, email, and password.',
        400
      );
    }

    if (password.length < 6) {
      return ApiResponse.error(
        res,
        'INVALID_PASSWORD',
        'Password must be at least 6 characters long.',
        400
      );
    }

    const existingUser = await User.findOne({ email: email.toLowerCase() });
    if (existingUser) {
      return ApiResponse.error(
        res,
        'EMAIL_EXISTS',
        'An account with this email address already exists.',
        409
      );
    }

    const passwordHash = await User.hashPassword(password);

    const user = await User.create({
      name,
      email: email.toLowerCase(),
      passwordHash,
      phone: phone || '',
      location: location || {}
    });

    const token = generateToken(user._id);

    logger.info(`Farmer registered successfully: ${user.email} (${user._id})`);

    return ApiResponse.success(
      res,
      {
        user: {
          id: user._id,
          name: user.name,
          email: user.email,
          phone: user.phone,
          location: user.location
        },
        token
      },
      'Account created successfully',
      201
    );
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Login farmer & return JWT token
 * @route   POST /api/v1/auth/login
 * @access  Public
 */
const login = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return ApiResponse.error(
        res,
        'MISSING_CREDENTIALS',
        'Please provide both email and password.',
        400
      );
    }

    const user = await User.findOne({ email: email.toLowerCase() }).select('+passwordHash');
    if (!user) {
      return ApiResponse.error(
        res,
        'INVALID_CREDENTIALS',
        'Invalid email or password.',
        401
      );
    }

    const isMatch = await user.matchPassword(password);
    if (!isMatch) {
      logger.warn(`Failed login attempt for: ${email}`);
      return ApiResponse.error(
        res,
        'INVALID_CREDENTIALS',
        'Invalid email or password.',
        401
      );
    }

    const token = generateToken(user._id);

    logger.info(`Farmer logged in: ${user.email}`);

    return ApiResponse.success(
      res,
      {
        user: {
          id: user._id,
          name: user.name,
          email: user.email,
          phone: user.phone,
          location: user.location
        },
        token
      },
      'Login successful'
    );
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get current authenticated farmer profile
 * @route   GET /api/v1/auth/me
 * @access  Private
 */
const getMe = async (req, res, next) => {
  try {
    return ApiResponse.success(res, { user: req.user });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  register,
  login,
  getMe
};
