import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-AgriVision ML Service"
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Path to trained model and class names
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH: str = os.path.join(BASE_DIR, "models", "crop_disease_model.keras")
    CLASS_NAMES_PATH: str = os.path.join(BASE_DIR, "models", "class_names.json")

    # Prediction Confidence Thresholds
    CONFIDENCE_THRESHOLD: float = 0.60
    HIGH_CONFIDENCE_THRESHOLD: float = 0.80

    # Image Quality Thresholds (Calibrated for diverse field conditions & mobile captures)
    MIN_IMAGE_WIDTH: int = 120
    MIN_IMAGE_HEIGHT: int = 120
    BLUR_LAPLACIAN_THRESHOLD: float = 20.0
    MIN_BRIGHTNESS_THRESHOLD: float = 20.0
    MAX_BRIGHTNESS_THRESHOLD: float = 248.0

    ALLOWED_IMAGE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
