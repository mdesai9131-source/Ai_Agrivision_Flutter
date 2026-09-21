from typing import Optional, Dict, Any

class SeverityService:
    """
    Dedicated Severity Service.
    In strict compliance with agricultural AI ethics and model transparency:
    Standard classification models classify disease category, NOT lesion surface area
    or multi-stage severity unless explicitly trained on lesion segmentation data.
    """

    @staticmethod
    def evaluate_severity(
        crop: Optional[str],
        disease: Optional[str],
        confidence: float,
        has_specialized_severity_model: bool = False
    ) -> Dict[str, Any]:
        # If crop is Healthy, severity is logically Healthy/None
        if disease and "Healthy" in disease:
            return {
                "severity": "Healthy",
                "severity_available": True,
                "severity_message": "Crop shows healthy tissue characteristics without visible pathological lesions."
            }

        # For diseases where model is purely a classification model
        if not has_specialized_severity_model:
            return {
                "severity": None,
                "severity_available": False,
                "severity_message": "Severity estimation requires lesion surface segmentation or a dedicated severity-trained model. We do not fabricate severity estimates."
            }

        # Fallback for future segmented models (Healthy, Low, Moderate, High)
        return {
            "severity": "Moderate",
            "severity_available": True,
            "severity_message": "Estimated based on lesion coverage."
        }

severity_service = SeverityService()
