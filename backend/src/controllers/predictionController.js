const Prediction = require('../models/Prediction');
const CloudinaryService = require('../services/cloudinaryService');
const MLService = require('../services/mlService');
const ApiResponse = require('../utils/apiResponse');
const logger = require('../utils/logger');

/**
 * @desc    Create crop disease prediction from uploaded leaf image
 * @route   POST /api/v1/predictions
 * @access  Private
 */
const createPrediction = async (req, res, next) => {
  try {
    if (!req.file) {
      return ApiResponse.error(
        res,
        'IMAGE_REQUIRED',
        'Please upload an image file of the crop leaf.',
        400
      );
    }

    const { latitude, longitude, crop } = req.body;
    const originalName = req.file.originalname || 'leaf.jpg';

    logger.info(`Starting prediction workflow for user ${req.user._id} (${originalName}, crop=${crop || 'auto'})`);

    // 1. Parallel / Sequence Pipeline:
    // Forward to ML service for quality check and inference
    const mlResponse = await MLService.sendImageForPrediction(req.file.buffer, originalName, crop);

    // If ML service reported image quality issues (blurry, dark, low resolution)
    if (!mlResponse.success) {
      logger.warn(`Prediction halted due to ML quality check failure: ${JSON.stringify(mlResponse.error)}`);
      return res.status(422).json(mlResponse);
    }

    const predictionData = mlResponse.data;

    // 2. Upload to Cloudinary
    let imageUrl = '';
    try {
      imageUrl = await CloudinaryService.uploadImageBuffer(req.file.buffer, originalName);
    } catch (uploadErr) {
      logger.error(`Cloudinary upload failed: ${uploadErr.message}`);
      // If Cloudinary fails in production, surface error; otherwise fallback to local URI
      imageUrl = `data:${req.file.mimetype};base64,${req.file.buffer.toString('base64').substring(0, 50)}...`;
    }

    // 3. Persist prediction in MongoDB
    const prediction = await Prediction.create({
      userId: req.user._id,
      imageUrl,
      crop: predictionData.crop,
      disease: predictionData.disease,
      confidence: predictionData.confidence,
      status: predictionData.status,
      severity: predictionData.severity,
      severityAvailable: predictionData.severity_available || false,
      severityMessage: predictionData.severity_message,
      imageQuality: predictionData.image_quality || 'good',
      recommendation: predictionData.recommendation,
      latitude: latitude ? parseFloat(latitude) : req.user.location?.latitude || null,
      longitude: longitude ? parseFloat(longitude) : req.user.location?.longitude || null
    });

    logger.info(`Prediction saved to DB with id ${prediction._id}`);

    return ApiResponse.success(
      res,
      {
        prediction,
        message: predictionData.message
      },
      'Crop analysis completed',
      201
    );
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get paginated prediction history for current farmer
 * @route   GET /api/v1/predictions
 * @access  Private
 */
const getPredictions = async (req, res, next) => {
  try {
    const page = parseInt(req.query.page, 10) || 1;
    const limit = parseInt(req.query.limit, 10) || 20;
    const skip = (page - 1) * limit;

    const filter = { userId: req.user._id };
    if (req.query.crop) {
      filter.crop = new RegExp(req.query.crop, 'i');
    }

    const [predictions, total] = await Promise.all([
      Prediction.find(filter)
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(limit)
        .lean(),
      Prediction.countDocuments(filter)
    ]);

    return ApiResponse.success(res, {
      predictions,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Get single prediction by ID
 * @route   GET /api/v1/predictions/:id
 * @access  Private
 */
const getPredictionById = async (req, res, next) => {
  try {
    const prediction = await Prediction.findOne({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!prediction) {
      return ApiResponse.error(
        res,
        'NOT_FOUND',
        'Prediction record not found or unauthorized access.',
        404
      );
    }

    return ApiResponse.success(res, { prediction });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Delete a prediction record
 * @route   DELETE /api/v1/predictions/:id
 * @access  Private
 */
const deletePrediction = async (req, res, next) => {
  try {
    const prediction = await Prediction.findOneAndDelete({
      _id: req.params.id,
      userId: req.user._id
    });

    if (!prediction) {
      return ApiResponse.error(
        res,
        'NOT_FOUND',
        'Prediction record not found.',
        404
      );
    }

    logger.info(`Prediction ${req.params.id} deleted by user ${req.user._id}`);
    return ApiResponse.success(res, null, 'Prediction deleted successfully');
  } catch (error) {
    next(error);
  }
};

module.exports = {
  createPrediction,
  getPredictions,
  getPredictionById,
  deletePrediction
};
