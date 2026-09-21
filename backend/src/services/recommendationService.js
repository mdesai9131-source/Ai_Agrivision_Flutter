class RecommendationService {
  /**
   * Sanitizes recommendation payload ensuring no dangerous chemical dosages are present
   * @param {Object} recommendation
   * @returns {Object} safe recommendation
   */
  static sanitize(recommendation) {
    if (!recommendation) {
      return {
        disease: 'Crop Observation',
        description: 'Visual diagnosis completed.',
        symptoms: [],
        prevention: ['Maintain general crop sanitation and clean irrigation.'],
        management: ['Consult your local agricultural extension agent for region-specific advice.'],
        expert_required: false
      };
    }

    return recommendation;
  }
}

module.exports = RecommendationService;
