import io
import cv2
import numpy as np
from PIL import Image
from typing import Tuple

def read_image_bytes(image_bytes: bytes) -> Image.Image:
    """Safely opens image bytes using PIL and normalizes channels to RGB."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.load()
        # Handle RGBA/LA transparency in WebP/PNG so transparent areas don't become pitch black
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            return background
        elif image.mode != "RGB":
            return image.convert("RGB")
        return image
    except Exception as e:
        raise ValueError(f"Failed to decode image bytes: {str(e)}")

def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """Converts a PIL image to OpenCV BGR/Grayscale format."""
    rgb_image = pil_image.convert("RGB")
    np_image = np.array(rgb_image)
    # Convert RGB to BGR for OpenCV functions
    bgr_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    return bgr_image

def calculate_laplacian_variance(cv2_image: np.ndarray) -> float:
    """Calculates the focus measure (Laplacian variance) to evaluate blurriness."""
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return float(variance)

def calculate_brightness(cv2_image: np.ndarray) -> float:
    """Calculates the average luminance of the image."""
    hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])
    return float(brightness)
