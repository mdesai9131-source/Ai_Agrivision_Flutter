import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.services.predictor import predictor
from app.services.image_quality import image_quality_service
from app.services.preprocessing import preprocess_image
from app.services.severity import severity_service
from app.services.recommendation import recommendation_service

client = TestClient(app)

def create_synthetic_image(width=250, height=250, color=(34, 139, 34)):
    """Creates an in-memory valid RGB PIL image."""
    img = Image.new("RGB", (width, height), color=color)
    return img

def create_image_bytes(image: Image.Image, format="JPEG") -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()

# 1. Health Endpoint Test
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data

# 2. Model Loading & Class Names Test
def test_class_names_loaded():
    assert len(predictor.class_names) > 0
    assert "Tomato___Healthy" in predictor.class_names

# 3. Preprocessing Test
def test_preprocessing():
    img = create_synthetic_image(300, 300)
    tensor = preprocess_image(img)
    assert tensor.shape == (1, 224, 224, 3)
    assert tensor.dtype == np.float32
    assert np.min(tensor) >= 0.0
    assert np.max(tensor) <= 1.0

# 4. Image Quality Service Tests
def test_image_quality_low_resolution():
    tiny_img = create_synthetic_image(100, 100)
    res = image_quality_service.validate_quality(tiny_img)
    assert res.is_valid is False
    assert res.quality == "poor"
    assert "below the minimum required" in res.reason

def test_image_quality_too_dark():
    dark_img = create_synthetic_image(250, 250, color=(5, 5, 5))
    res = image_quality_service.validate_quality(dark_img)
    assert res.is_valid is False
    assert res.quality == "poor"
    assert "underexposed" in res.reason

def test_image_quality_too_bright():
    bright_img = create_synthetic_image(250, 250, color=(250, 250, 250))
    res = image_quality_service.validate_quality(bright_img)
    assert res.is_valid is False
    assert res.quality == "poor"
    assert "overexposed" in res.reason

# 5. Severity Service Transparency Test
def test_severity_service_transparency():
    # When disease is Healthy
    healthy_sev = severity_service.evaluate_severity("Tomato", "Healthy", 0.95)
    assert healthy_sev["severity"] == "Healthy"
    assert healthy_sev["severity_available"] is True

    # When disease is a fungal disease but no severity model exists
    blight_sev = severity_service.evaluate_severity("Tomato", "Early Blight", 0.92, has_specialized_severity_model=False)
    assert blight_sev["severity"] is None
    assert blight_sev["severity_available"] is False
    assert "Severity estimation requires" in blight_sev["severity_message"]

# 6. Recommendation Safety Test
def test_recommendation_safe_guidance():
    rec = recommendation_service.get_recommendation("Tomato", "Early Blight")
    assert rec is not None
    assert "Tomato Early Blight" in rec.disease
    assert len(rec.symptoms) > 0
    assert len(rec.prevention) > 0
    assert len(rec.management) > 0
    # Ensure no fabricated chemical prescription
    for item in rec.management:
        assert "apply 500ml of poison" not in item.lower()

# 7. Prediction Endpoint Integration Tests
def test_predict_endpoint_valid_image():
    # Create image with texture to pass blur check
    arr = np.random.randint(50, 180, (250, 250, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    img_bytes = create_image_bytes(img)

    response = client.post(
        "/api/v1/predict",
        files={"image": ("crop_test.jpg", img_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert "data" in res_json
    assert res_json["data"]["confidence"] > 0
    assert res_json["data"]["image_quality"] == "good"

def test_predict_endpoint_invalid_file_type():
    response = client.post(
        "/api/v1/predict",
        files={"image": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400
    res_json = response.json()
    assert "INVALID_IMAGE_TYPE" in str(res_json)

def test_predict_wheat_image_returns_wheat():
    arr = np.random.randint(50, 180, (250, 250, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    img_bytes = create_image_bytes(img)

    # Test wheat prediction via filename hint
    response = client.post(
        "/api/v1/predict",
        files={"image": ("wheat_rust_leaf.jpg", img_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["crop"] == "Wheat"
    assert "Rust" in data["disease"] or "Septoria" in data["disease"] or "Healthy" in data["disease"]
    assert data["recommendation"] is not None

def test_predict_with_crop_parameter_wheat():
    arr = np.random.randint(50, 180, (250, 250, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    img_bytes = create_image_bytes(img)

    # Test explicit crop parameter
    response = client.post(
        "/api/v1/predict",
        files={"image": ("unknown_sample.jpg", img_bytes, "image/jpeg")},
        data={"crop": "Wheat"}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["crop"] == "Wheat"
    assert data["recommendation"]["disease"] is not None

def test_wheat_recommendations_coverage():
    wheat_diseases = ["Brown Rust", "Yellow Rust", "Powdery Mildew", "Septoria", "Healthy"]
    for disease in wheat_diseases:
        rec = recommendation_service.get_recommendation("Wheat", disease)
        assert rec is not None
        assert "Wheat" in rec.disease
        assert len(rec.prevention) > 0
        assert len(rec.management) > 0

