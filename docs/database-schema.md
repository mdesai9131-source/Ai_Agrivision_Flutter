# AI-AgriVision Database Schema Documentation

AI-AgriVision utilizes **MongoDB** (with Mongoose ODM) for persistent storage of farmer profiles, diagnostic history, and localized geospatial data.

---

## 1. User Collection (`users`)

Stores registered farmer credentials, profile information, and optional default location coordinates.

```javascript
{
  "_id": ObjectId("664c1234567890abcdef1234"),
  "name": "Ramesh Patel",
  "email": "ramesh.patel@example.com",
  "passwordHash": "$2a$10$e8wF3Qv1mS1...",  // bcrypt hash, select: false
  "phone": "+91 98765 43210",
  "location": {
    "latitude": 23.2599,
    "longitude": 77.4126,
    "city": "Bhopal",
    "state": "Madhya Pradesh"
  },
  "createdAt": ISODate("2026-09-19T10:00:00.000Z"),
  "updatedAt": ISODate("2026-09-19T10:00:00.000Z")
}
```

### Indices
- `email: 1` (Unique index)
- `location.latitude: 1, location.longitude: 1` (Compound index for spatial sorting)

---

## 2. Prediction Collection (`predictions`)

Stores leaf disease diagnosis results, confidence calculations, severity flags, Cloudinary image references, and recommendations.

```javascript
{
  "_id": ObjectId("664c1f9876543210fedcba98"),
  "userId": ObjectId("664c1234567890abcdef1234"),
  "imageUrl": "https://res.cloudinary.com/demo/image/upload/v1/ai_agrivision/crops/leaf_01.jpg",
  "crop": "Tomato",
  "disease": "Early Blight",
  "confidence": 0.94,
  "status": "high_confidence",  // 'high_confidence' | 'medium_confidence' | 'uncertain'
  "severity": null,              // 'Healthy' | 'Low' | 'Moderate' | 'High' | null
  "severityAvailable": false,
  "severityMessage": "Severity estimation requires lesion surface segmentation or a dedicated severity-trained model.",
  "imageQuality": "good",
  "recommendation": {
    "disease": "Tomato Early Blight (Alternaria solani)",
    "description": "A common fungal disease affecting tomato foliage, stems, and fruits...",
    "symptoms": [
      "Small brown-to-black spots appearing initially on older/lower leaves",
      "Target-board concentric rings developing within the spots"
    ],
    "prevention": [
      "Practice 2-3 year crop rotation with non-solanaceous crops",
      "Use drip or furrow irrigation to keep foliage dry"
    ],
    "management": [
      "Prune infected bottom leaves during dry morning weather using sanitized shears",
      "Follow local agriculture extension guidelines for registered fungicides"
    ],
    "expert_required": false
  },
  "latitude": 23.2599,
  "longitude": 77.4126,
  "createdAt": ISODate("2026-09-19T10:05:00.000Z")
}
```

### Indices
- `userId: 1, createdAt: -1` (Compound index for fast chronological farmer history retrieval)
- `crop: 1, disease: 1` (Compound index for regional disease prevalence analytics)
- `latitude: 1, longitude: 1` (Compound index for regional outbreak mapping)
