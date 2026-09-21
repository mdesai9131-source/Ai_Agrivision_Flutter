# AI-AgriVision ML Service

A high-performance, production-grade computer vision microservice built with **FastAPI**, **TensorFlow/Keras**, **OpenCV**, and **Pillow** for agricultural leaf disease classification and safe farmer recommendations.

---

## Key Features

1. **Transfer Learning Architecture**: Pre-trained backbones (MobileNetV3Large, EfficientNetB0, MobileNetV2) optimized for fast CPU/GPU inference and mobile deployment.
2. **Pre-Inference Image Quality Gate**:
   - Laplacian variance blur detection.
   - Mean luminance exposure checks (rejects overexposed glare or dark photos).
   - Minimum resolution verification (>= 200x200px).
3. **Confidence-Aware Triage**:
   - $\ge 80\%$: High Confidence.
   - $60\% - 79\%$: Medium Confidence.
   - $< 60\%$: Marked as `uncertain`; refuses to diagnose falsely.
4. **Transparent Severity Service**:
   - Explicitly discloses `severity_available: false` when models are pure categorical classifiers, adhering to agricultural AI integrity.
5. **Safe Agronomic Recommendation Engine**:
   - Biological and cultural prevention strategies.
   - Strict avoidance of fabricated pesticide dosages.

---

## Directory Structure

```
ml-service/
├── app/
│   ├── main.py                  # FastAPI app entrypoint & Swagger setup
│   ├── api/
│   │   └── prediction_routes.py # /api/v1/predict & /health
│   ├── core/
│   │   ├── config.py            # Pydantic configuration & thresholds
│   │   └── logging_config.py    # Structured logging
│   ├── models/
│   │   ├── crop_disease_model.keras # Pretrained Keras model
│   │   └── class_names.json     # Class taxonomy mapping
│   ├── schemas/
│   │   └── prediction_schema.py # Pydantic request/response schemas
│   ├── services/
│   │   ├── predictor.py         # Model loader & inference pipeline
│   │   ├── preprocessing.py     # 224x224 RGB normalization
│   │   ├── image_quality.py     # Blur, brightness, resolution validation
│   │   ├── severity.py          # Honest severity assessment
│   │   └── recommendation.py    # Safe agricultural knowledge base
│   └── utils/
│       └── image_utils.py       # PIL/OpenCV conversion helpers
├── dataset/
│   ├── raw/
│   ├── train/
│   ├── validation/
│   └── test/
├── notebooks/
│   ├── 01_dataset_analysis.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_training.ipynb
│   └── 04_evaluation.ipynb
├── scripts/
│   ├── train.py                 # 2-stage transfer learning training script
│   ├── evaluate.py              # Confusion matrix & F1 evaluation
│   └── export_model.py          # TFLite conversion & quantization
├── tests/
│   └── test_ml_service.py       # Pytest test suite
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Setup & Execution

### 1. Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger Documentation is available at:
`http://localhost:8000/docs`

### 3. Run Tests
```bash
pytest tests/ -v
```

### 4. Training
Place dataset in `dataset/train/`, `dataset/validation/`, and `dataset/test/` with folders named like `Tomato___Early_Blight`:
```bash
python scripts/train.py --backbone MobileNetV3Large --epochs_head 15 --epochs_finetune 10
```
