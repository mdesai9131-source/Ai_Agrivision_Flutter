from PIL import Image
from app.core.config import settings
from app.core.logging_config import logger
from app.schemas.prediction_schema import ImageQualityResult
from app.utils.image_utils import (
    pil_to_cv2,
    calculate_laplacian_variance,
    calculate_brightness
)

class ImageQualityService:
    @staticmethod
    def validate_quality(image: Image.Image, filename: str = "") -> ImageQualityResult:
        """
        Validates crop image quality before feeding into ML inference pipeline.
        Checks resolution, blurriness, and exposure limits.
        """
        width, height = image.size
        resolution_str = f"{width}x{height}"

        # 1. Resolution Check
        if width < settings.MIN_IMAGE_WIDTH or height < settings.MIN_IMAGE_HEIGHT:
            logger.warning(f"Image resolution too low: {resolution_str}")
            return ImageQualityResult(
                is_valid=False,
                quality="poor",
                reason=f"Image resolution ({resolution_str}) is below the minimum required {settings.MIN_IMAGE_WIDTH}x{settings.MIN_IMAGE_HEIGHT}px.",
                resolution=resolution_str
            )

        try:
            cv2_img = pil_to_cv2(image)
        except Exception as e:
            logger.error(f"Image conversion failed: {str(e)}")
            return ImageQualityResult(
                is_valid=False,
                quality="poor",
                reason="Corrupted image structure or unreadable color channels.",
                resolution=resolution_str
            )

        # 2. Brightness / Exposure Check
        brightness = calculate_brightness(cv2_img)
        if brightness < settings.MIN_BRIGHTNESS_THRESHOLD:
            logger.warning(f"Image is too dark. Luminance: {brightness:.2f}")
            return ImageQualityResult(
                is_valid=False,
                quality="poor",
                reason="Image is underexposed/too dark. Please take photo in good ambient natural light.",
                brightness=round(brightness, 2),
                resolution=resolution_str
            )

        if brightness > settings.MAX_BRIGHTNESS_THRESHOLD:
            logger.warning(f"Image is too bright/overexposed. Luminance: {brightness:.2f}")
            return ImageQualityResult(
                is_valid=False,
                quality="poor",
                reason="Image is overexposed/glare detected. Please avoid direct sunlight flash.",
                brightness=round(brightness, 2),
                resolution=resolution_str
            )

        # 3. Blur / Focus Check
        blur_score = calculate_laplacian_variance(cv2_img)
        if blur_score < settings.BLUR_LAPLACIAN_THRESHOLD:
            logger.warning(f"Image is too blurry. Laplacian variance: {blur_score:.2f}")
            return ImageQualityResult(
                is_valid=False,
                quality="poor",
                reason="Image is too blurry. Please hold camera steady and focus on the affected leaf.",
                blur_score=round(blur_score, 2),
                resolution=resolution_str
            )

        return ImageQualityResult(
            is_valid=True,
            quality="good",
            reason=None,
            blur_score=round(blur_score, 2),
            brightness=round(brightness, 2),
            resolution=resolution_str
        )

image_quality_service = ImageQualityService()
