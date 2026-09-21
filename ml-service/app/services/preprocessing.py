import numpy as np
from PIL import Image
from typing import Tuple

TARGET_SIZE: Tuple[int, int] = (224, 224)

def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    """
    Preprocesses a PIL image for MobileNet/EfficientNet deep learning models:
    1. Ensures 3-channel RGB format
    2. Resizes to 224x224 using Lanczos/Bicubic high quality interpolation
    3. Converts to float32 NumPy array
    4. Normalizes pixel values [0, 255] -> [0.0, 1.0] (or standard Keras normalization)
    5. Adds batch dimension: (1, 224, 224, 3)
    """
    # 1. Convert to RGB (handles RGBA, Grayscale, etc.)
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")

    # 2. Resize to model input dimensions
    resized_img = pil_image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

    # 3. Convert to float32 NumPy array
    img_array = np.array(resized_img, dtype=np.float32)

    # 4. Normalize to [0, 1]
    img_array = img_array / 255.0

    # 5. Expand batch dimensions: (1, 224, 224, 3)
    batched_array = np.expand_dims(img_array, axis=0)

    return batched_array
