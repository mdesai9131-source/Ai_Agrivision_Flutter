import time
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.core.logging_config import logger
from app.schemas.prediction_schema import PredictionResponse
from app.services.predictor import predictor
from app.utils.image_utils import read_image_bytes

router = APIRouter()

ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg",
    "image/x-webp",
    "image/pjpeg",
    "image/x-png"
]
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Crop Disease from Image",
    description="Validates image quality and classifies crop leaf disease with confidence scoring and safe advisory."
)
async def predict_crop_disease(
    image: UploadFile = File(..., description="Crop leaf photo"),
    crop: Optional[str] = Form(None, description="Optional crop hint (e.g. Wheat, Tomato, Potato)")
):
    start_time = time.time()
    
    # 1. Validate MIME type and file extension fallback
    content_type = (image.content_type or "").lower()
    filename = (image.filename or "").lower()
    file_ext = "." + filename.split(".")[-1] if "." in filename else ""

    is_valid_mime = content_type in ALLOWED_MIME_TYPES
    is_valid_ext = file_ext in ALLOWED_EXTENSIONS
    is_octet = content_type in ["application/octet-stream", "binary/octet-stream", ""]

    if not is_valid_mime and not (is_octet and is_valid_ext):
        logger.warning(f"Unsupported content type: '{image.content_type}' for filename '{image.filename}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_IMAGE_TYPE",
                "message": f"Unsupported image type '{image.content_type}'. Please upload JPEG, PNG, or WEBP."
            }
        )

    # 2. Read file bytes safely
    try:
        image_bytes = await image.read()
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "EMPTY_FILE", "message": "Uploaded image file is empty."}
            )
        # Limit to 15MB
        if len(image_bytes) > 15 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail={"code": "FILE_TOO_LARGE", "message": "Image size exceeds 15MB limit."}
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading file bytes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "FILE_READ_ERROR", "message": "Could not read uploaded image."}
        )

    # 3. Decode PIL image
    try:
        pil_image = read_image_bytes(image_bytes)
    except ValueError as ve:
        logger.warning(f"Corrupted or invalid image: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_IMAGE", "message": "Image file is corrupted or cannot be decoded."}
        )

    # 4. Predict
    result = predictor.predict_image(pil_image, filename=image.filename or "", crop_hint=crop)

    latency = round((time.time() - start_time) * 1000, 2)
    logger.info(f"Prediction processed for '{image.filename}' in {latency}ms")

    # If quality check failed, return HTTP 422 with structured failure
    if not result.get("success"):
        return PredictionResponse(
            success=False,
            data=None,
            error=result.get("error")
        )

    return PredictionResponse(
        success=True,
        data=result.get("data"),
        error=None
    )
