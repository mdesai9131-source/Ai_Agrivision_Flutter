const AgroService = require('../services/agroService');
const ApiResponse = require('../utils/apiResponse');

/**
 * @desc    Get nearby agricultural centers, shops, and advisory extension centers
 * @route   GET /api/v1/agro/nearby
 * @access  Private
 */
const getNearbyAgroSupport = async (req, res, next) => {
  try {
    const lat = req.query.lat || req.user?.location?.latitude;
    const lng = req.query.lng || req.user?.location?.longitude;
    const category = req.query.category || 'all';
    const radius = parseFloat(req.query.radius || '25');
    const district = req.query.district || '';
    const locationName = req.query.location || req.query.locationName || '';

    if (!lat || !lng) {
      return ApiResponse.error(
        res,
        'LOCATION_REQUIRED',
        'Latitude and longitude are required. Please enable GPS or enter location manually.',
        400
      );
    }

    const centers = await AgroService.getNearbyAgroSupport(lat, lng, category, radius, district, locationName);

    return ApiResponse.success(res, {
      centers,
      coordinates: { latitude: parseFloat(lat), longitude: parseFloat(lng) },
      total: centers.length
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getNearbyAgroSupport
};
