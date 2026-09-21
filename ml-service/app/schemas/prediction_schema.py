from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class RecommendationData(BaseModel):
    disease: str = Field(..., description="Crop and disease formatted name")
    description: str = Field(..., description="Overview of the condition")
    symptoms: List[str] = Field(default_factory=list, description="Common observable symptoms")
    prevention: List[str] = Field(default_factory=list, description="Safe prevention and cultural practices")
    management: List[str] = Field(default_factory=list, description="Safe non-chemical and advisory management steps")
    expert_required: bool = Field(False, description="Flag indicating if immediate certified agronomist inspection is needed")

class PredictionData(BaseModel):
    crop: Optional[str] = None
    disease: Optional[str] = None
    confidence: float
    status: str = Field(..., description="high_confidence, medium_confidence, or uncertain")
    severity: Optional[str] = None
    severity_available: bool = False
    severity_message: Optional[str] = None
    image_quality: str = "good"
    message: Optional[str] = None
    recommendation: Optional[RecommendationData] = None

class PredictionResponse(BaseModel):
    success: bool
    data: Optional[PredictionData] = None
    error: Optional[Dict[str, Any]] = None

class ImageQualityResult(BaseModel):
    is_valid: bool
    quality: str
    reason: Optional[str] = None
    blur_score: Optional[float] = None
    brightness: Optional[float] = None
    resolution: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str = "1.0.0"
