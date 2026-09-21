const mongoose = require('mongoose');

const recommendationSchema = new mongoose.Schema(
  {
    disease: { type: String, default: '' },
    description: { type: String, default: '' },
    symptoms: [{ type: String }],
    prevention: [{ type: String }],
    management: [{ type: String }],
    expert_required: { type: Boolean, default: false }
  },
  { _id: false }
);

const predictionSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'User ID is required'],
      index: true
    },
    imageUrl: {
      type: String,
      required: [true, 'Image URL is required'],
      trim: true
    },
    crop: {
      type: String,
      default: null,
      trim: true
    },
    disease: {
      type: String,
      default: null,
      trim: true
    },
    confidence: {
      type: Number,
      required: true,
      min: 0.0,
      max: 1.0
    },
    status: {
      type: String,
      enum: ['high_confidence', 'medium_confidence', 'uncertain', 'low_confidence'],
      default: 'medium_confidence'
    },
    severity: {
      type: String,
      default: null,
      enum: ['Healthy', 'Low', 'Moderate', 'High', null]
    },
    severityAvailable: {
      type: Boolean,
      default: false
    },
    severityMessage: {
      type: String,
      default: null
    },
    imageQuality: {
      type: String,
      default: 'good'
    },
    recommendation: {
      type: recommendationSchema,
      default: null
    },
    latitude: {
      type: Number,
      default: null
    },
    longitude: {
      type: Number,
      default: null
    }
  },
  {
    timestamps: { createdAt: true, updatedAt: false }
  }
);

// Compound index for querying user prediction history chronologically
predictionSchema.index({ userId: 1, createdAt: -1 });
predictionSchema.index({ crop: 1, disease: 1 });
predictionSchema.index({ latitude: 1, longitude: 1 });

const Prediction = mongoose.model('Prediction', predictionSchema);
module.exports = Prediction;
