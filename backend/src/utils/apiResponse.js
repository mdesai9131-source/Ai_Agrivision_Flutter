/**
 * Standardized API response formatter
 */
class ApiResponse {
  static success(res, data = null, message = null, statusCode = 200) {
    const response = {
      success: true,
      data
    };
    if (message) {
      response.message = message;
    }
    return res.status(statusCode).json(response);
  }

  static error(res, code, message, statusCode = 500, details = null) {
    const errorBody = {
      code,
      message
    };
    if (details) {
      errorBody.details = details;
    }
    return res.status(statusCode).json({
      success: false,
      error: errorBody
    });
  }
}

module.exports = ApiResponse;
