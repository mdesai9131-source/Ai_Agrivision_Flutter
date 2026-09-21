const User = require('../models/User');
const ApiResponse = require('../utils/apiResponse');

/**
 * @desc    Get user profile
 * @route   GET /api/v1/users/profile
 * @access  Private
 */
const getProfile = async (req, res, next) => {
  try {
    const user = await User.findById(req.user._id).select('-passwordHash');
    return ApiResponse.success(res, { user });
  } catch (error) {
    next(error);
  }
};

/**
 * @desc    Update user profile & location settings
 * @route   PUT /api/v1/users/profile
 * @access  Private
 */
const updateProfile = async (req, res, next) => {
  try {
    const { name, phone, location } = req.body;

    const fieldsToUpdate = {};
    if (name) fieldsToUpdate.name = name;
    if (phone !== undefined) fieldsToUpdate.phone = phone;
    if (location) {
      fieldsToUpdate.location = {
        latitude: location.latitude ?? req.user.location?.latitude,
        longitude: location.longitude ?? req.user.location?.longitude,
        city: location.city ?? req.user.location?.city,
        state: location.state ?? req.user.location?.state
      };
    }

    const updatedUser = await User.findByIdAndUpdate(
      req.user._id,
      { $set: fieldsToUpdate },
      { new: true, runValidators: true }
    ).select('-passwordHash');

    return ApiResponse.success(res, { user: updatedUser }, 'Profile updated successfully');
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getProfile,
  updateProfile
};
