# AI-AgriVision Architecture Documentation

## System Overview

AI-AgriVision is an enterprise-grade agricultural diagnostic ecosystem engineered to assist smallholder farmers and agronomy professionals in accurately identifying foliar diseases, assessing image quality, obtaining safe biological/cultural farming recommendations, and finding nearby agricultural assistance centers.

---

## High-Level Architecture Diagram

```mermaid
flowchart TD
    subgraph ClientLayer ["Mobile Client (Flutter / Dart)"]
        F1[Farmer Mobile Device]
        F2[Camera / Image Picker]
        F3[Geolocator GPS]
        F4[Provider State Store]
        F1 --> F2
        F1 --> F3
        F2 --> F4
    end

    subgraph ApiGateway ["Backend API (Node.js / Express.js)"]
        B1[Express HTTP Server]
        B2[Helmet & CORS Security]
        B3[JWT Auth Middleware]
        B4[Multer Memory Stream]
        B5[Rate Limiter]
        B6[Haversine Agro Distance Engine]
        B1 --- B2
        B1 --- B5
        B1 --> B3
        B3 --> B4
        B1 --> B6
    end

    subgraph StorageLayer ["Persistence & CDN"]
        M1[(MongoDB Replica Set)]
        C1[(Cloudinary Image CDN)]
    end

    subgraph MLSuggestionLayer ["ML Inference Microservice (Python FastAPI)"]
        P1[FastAPI REST API]
        P2[Image Quality Validator]
        P3[Laplacian Blur & Luminance Filter]
        P4[TensorFlow / Keras MobileNetV3]
        P5[Confidence Threshold Evaluator]
        P6[Severity Transparency Module]
        P7[Safe Recommendation KB]
        P1 --> P2
        P2 --> P3
        P3 --> P4
        P4 --> P5
        P5 --> P6
        P5 --> P7
    end

    subgraph ExternalServices ["External Providers"]
        E1[Google Maps / OpenStreetMap Places]
    end

    F4 -->|Multipart HTTPS| B1
    B4 -->|Secure Upload| C1
    B4 -->|Buffer Proxy| P1
    B1 -->|Mongoose Queries| M1
    B6 -->|Places Query| E1
    P7 -->|Structured Diagnosis| B1
    B1 -->|Unified JSON Payload| F4
```

---

## Data Flow & Inference Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor Farmer as Farmer
    participant Flutter as Flutter App
    participant Node as Node.js Backend
    participant Cloudinary as Cloudinary CDN
    participant PythonML as Python FastAPI ML
    participant Mongo as MongoDB

    Farmer->>Flutter: Takes photo of diseased crop leaf
    Flutter->>Flutter: Validates file format & local dimensions
    Flutter->>Node: POST /api/v1/predictions (Image Buffer + GPS)
    Note over Node: Verifies JWT, rate limits, and buffers image
    Node->>PythonML: POST /api/v1/predict (Multipart stream)
    
    rect rgb(240, 248, 255)
        Note over PythonML: 1. Image Quality Gate (Resolution, Blur, Exposure)
        alt Image is Blurry or Corrupted
            PythonML-->>Node: 422 Unprocessable (Quality: poor, Reason)
            Node-->>Flutter: 422 Quality Warning (Prompts Recapture)
            Flutter-->>Farmer: "Image too blurry. Please hold steady."
        end
        Note over PythonML: 2. Resize 224x224, Normalize, Keras Inference
        Note over PythonML: 3. Softmax Probabilities & Top-1 Extraction
        alt Confidence < 0.60
            Note over PythonML: Sets status = "uncertain" (Refuses to guess)
        else Confidence >= 0.80
            Note over PythonML: Sets status = "high_confidence"
        else
            Note over PythonML: Sets status = "medium_confidence"
        end
        Note over PythonML: 4. Transparent Severity & Safe Non-Toxic Advisory
        PythonML-->>Node: Return diagnosis JSON
    end

    Node->>Cloudinary: Stream image buffer to cloud storage
    Cloudinary-->>Node: Secure image URL
    Node->>Mongo: Persist record (userId, imageUrl, crop, disease, confidence, status, recommendation, lat/lng)
    Mongo-->>Node: Saved document
    Node-->>Flutter: Return 201 Created with full diagnosis
    Flutter-->>Farmer: Render Farmer-Friendly Diagnosis & Nearby Support
```

---

## Core Security Architecture

1. **Zero Secret Leakage**: Credentials (`JWT_SECRET`, `CLOUDINARY_API_SECRET`, `MAPS_API_KEY`) reside exclusively in encrypted environment variables and are excluded via `.gitignore`.
2. **Sanitized Error Responses**: The backend intercepts unhandled exceptions, logging technical traces internally via Winston while delivering safe, non-leaking error codes to the mobile client.
3. **Pesticide Safety Guardrail**: The ML microservice and recommendation engines strictly prohibit chemical prescriptions or fabricated dosages.
