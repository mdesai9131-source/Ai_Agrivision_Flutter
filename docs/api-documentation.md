# AI-AgriVision API Documentation

## 1. Node.js Backend API

Base URL: `http://localhost:5000/api/v1`

---

### Authentication Endpoints

#### Register Farmer Account
- **Endpoint**: `POST /auth/register`
- **Access**: Public
- **Request Body**:
```json
{
  "name": "Ramesh Patel",
  "email": "ramesh.patel@example.com",
  "password": "SecurePassword123!",
  "phone": "+91 98765 43210",
  "location": {
    "latitude": 23.2599,
    "longitude": 77.4126,
    "city": "Bhopal",
    "state": "Madhya Pradesh"
  }
}
```
- **Response (201 Created)**:
```json
{
  "success": true,
  "message": "Account created successfully",
  "data": {
    "user": {
      "id": "664c12...",
      "name": "Ramesh Patel",
      "email": "ramesh.patel@example.com",
      "phone": "+91 98765 43210",
      "location": { "latitude": 23.2599, "longitude": 77.4126, "city": "Bhopal", "state": "Madhya Pradesh" }
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### Login Farmer
- **Endpoint**: `POST /auth/login`
- **Access**: Public
- **Request Body**:
```json
{
  "email": "ramesh.patel@example.com",
  "password": "SecurePassword123!"
}
```
- **Response (200 OK)**:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { ... },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### Get Current Profile
- **Endpoint**: `GET /auth/me`
- **Access**: Private (`Authorization: Bearer <token>`)
- **Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "664c12...",
      "name": "Ramesh Patel",
      "email": "ramesh.patel@example.com",
      "location": { ... }
    }
  }
}
```

---

### Prediction Endpoints

#### Create Crop Diagnosis
- **Endpoint**: `POST /predictions`
- **Access**: Private (`Authorization: Bearer <token>`)
- **Content-Type**: `multipart/form-data`
- **Form Fields**:
  - `image`: Image file (JPEG, PNG, WEBP, <= 10MB)
  - `latitude`: `23.2599` (optional)
  - `longitude`: `77.4126` (optional)
- **Response (201 Created - Confident)**:
```json
{
  "success": true,
  "message": "Crop analysis completed",
  "data": {
    "prediction": {
      "_id": "664c1f...",
      "userId": "664c12...",
      "imageUrl": "https://res.cloudinary.com/demo/image/upload/v1/ai_agrivision/crops/sample.jpg",
      "crop": "Tomato",
      "disease": "Early Blight",
      "confidence": 0.94,
      "status": "high_confidence",
      "severity": null,
      "severityAvailable": false,
      "severityMessage": "Severity estimation requires lesion surface segmentation or a dedicated severity-trained model.",
      "imageQuality": "good",
      "recommendation": {
        "disease": "Tomato Early Blight (Alternaria solani)",
        "description": "A common fungal disease affecting tomato foliage...",
        "symptoms": [ "Small brown-to-black spots on older leaves" ],
        "prevention": [ "Practice 2-3 year crop rotation" ],
        "management": [ "Prune infected bottom leaves during dry morning weather" ],
        "expert_required": false
      },
      "latitude": 23.2599,
      "longitude": 77.4126,
      "createdAt": "2026-09-19T13:00:00.000Z"
    },
    "message": "Successfully identified Tomato Early Blight with high confidence."
  }
}
```

- **Response (201 Created - Uncertain, Confidence < 60%)**:
```json
{
  "success": true,
  "data": {
    "prediction": {
      "crop": null,
      "disease": null,
      "confidence": 0.44,
      "status": "uncertain",
      "severity": null,
      "imageQuality": "good",
      "recommendation": null
    },
    "message": "The image is not clear enough for a reliable prediction. Please upload a clearer crop/leaf image."
  }
}
```

- **Response (422 Unprocessable Entity - Poor Image Quality)**:
```json
{
  "success": false,
  "error": {
    "code": "POOR_IMAGE_QUALITY",
    "message": "Image is too blurry. Please hold camera steady and focus on the affected leaf.",
    "quality": "poor",
    "reason": "Image is too blurry. Please hold camera steady and focus on the affected leaf.",
    "blur_score": 42.15,
    "brightness": 128.4
  }
}
```

#### List Prediction History
- **Endpoint**: `GET /predictions?page=1&limit=20&crop=Tomato`
- **Access**: Private (`Authorization: Bearer <token>`)

---

### Nearby Agro Support Endpoints

#### Find Nearby Agricultural Centers
- **Endpoint**: `GET /agro/nearby?lat=23.2599&lng=77.4126&category=all&radius=25`
- **Access**: Private (`Authorization: Bearer <token>`)
- **Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "centers": [
      {
        "id": "agro-center-01",
        "name": "District Krishi Vigyan Kendra (KVK) & Extension Center",
        "category": "Agro Office & Research",
        "address": "District Agriculture Complex, Block 4",
        "distanceKm": 3.8,
        "rating": 4.8,
        "phone": "+91 1800-180-1551",
        "services": ["Free Soil Testing", "Certified Pathologist Advice", "Kisan Helpline"],
        "isOpenNow": true
      }
    ],
    "coordinates": { "latitude": 23.2599, "longitude": 77.4126 },
    "total": 5
  }
}
```

---

## 2. Python ML Microservice API

Base URL: `http://localhost:8000`

### Health Check
- **Endpoint**: `GET /health`
- **Response (200 OK)**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Predict Crop Disease
- **Endpoint**: `POST /api/v1/predict`
- **Content-Type**: `multipart/form-data`
- **File field**: `image`
