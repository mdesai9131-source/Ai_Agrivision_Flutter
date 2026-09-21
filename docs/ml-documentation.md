# AI-AgriVision Machine Learning Documentation

## 1. Computer Vision Model Architecture

The core crop leaf diagnosis model utilizes **transfer learning** with modern, parameter-efficient convolutional neural network (CNN) architectures:

- **Primary Backbone**: `MobileNetV3Large` (or `EfficientNetB0` / `MobileNetV2`) pre-trained on ImageNet.
- **Input Dimension**: `(224, 224, 3)` RGB float32 tensor normalized to `[0.0, 1.0]`.
- **Classification Head**:
  - Global Average Pooling 2D (`GlobalAveragePooling2D`)
  - Batch Normalization
  - Dropout ($p = 0.3$)
  - Dense layer (256 units, ReLU activation)
  - Dropout ($p = 0.2$)
  - Dense output layer ($N$ classes, Softmax activation)

---

## 2. Inference & Quality Pipeline

```
Raw Image Bytes
   ↓
Image Quality Gate (OpenCV / PIL)
   ├── Decodable structure & RGB conversion
   ├── Minimum resolution: width >= 200px, height >= 200px
   ├── Focus assessment: Laplacian variance >= 80.0
   └── Exposure assessment: Luminance 40.0 <= V <= 230.0
   ↓ [If Quality Passes]
Preprocessing (224x224 Lanczos Resizing, [0, 1] Normalization)
   ↓
Model Inference (Forward Pass)
   ↓
Softmax Probabilities & Top Prediction
   ↓
Confidence Threshold Evaluator
   ├── Confidence >= 0.80 -> status: "high_confidence"
   ├── 0.60 <= Confidence < 0.80 -> status: "medium_confidence"
   └── Confidence < 0.60 -> status: "uncertain" (Refuses false prediction)
   ↓
Severity Evaluation & Agricultural Guidance
   ├── Severity Transparency: severity_available = false (Unless segmented)
   └── Safe Agronomic Advice: Cultural & biological prevention (No toxic dosage)
```

---

## 3. Image Quality Algorithms

### Laplacian Blur Detection
The variance of the Laplacian operator measures the rate of high-frequency edge transitions in the grayscale image:
$$\sigma^2 = \text{Var}(\nabla^2 I)$$
- If $\sigma^2 < 80.0$, the image is classified as excessively blurry.

### Exposure Validation
The image is converted to the HSV (Hue, Saturation, Value) color space, and the mean value channel is computed:
$$V_{\text{avg}} = \frac{1}{W \times H} \sum_{x,y} V(x,y)$$
- $V_{\text{avg}} < 40.0$: Flagged as underexposed / dark.
- $V_{\text{avg}} > 230.0$: Flagged as overexposed / glare.

---

## 4. Training Pipeline & Callbacks

The training script `scripts/train.py` executes a **two-phase transfer learning schedule**:

1. **Phase 1 (Head Warmup)**:
   - Base model layers are frozen (`base_model.trainable = False`).
   - Adam optimizer with learning rate $\eta = 10^{-3}$.
   - Trains classification head for 15 epochs.
2. **Phase 2 (Backbone Fine-Tuning)**:
   - Top 30% of base model layers are unfrozen.
   - Adam optimizer with reduced learning rate $\eta = 10^{-5}$.
   - Trains for 10 epochs.
3. **Callbacks**:
   - `EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)`
   - `ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-7)`
   - `ModelCheckpoint(filepath='crop_disease_model.keras', save_best_only=True)`

---

## 5. Dataset Organization & Limitations

The training data should be organized into:
```
dataset/
├── train/
│   ├── Tomato___Healthy/
│   ├── Tomato___Early_Blight/
│   └── Tomato___Late_Blight/
├── validation/
└── test/
```

### Dataset Limitations
1. **Lab vs Field Domain Gap**: Datasets collected under artificial laboratory backgrounds (e.g. single leaves placed against white or black paper) may experience domain shift when deployed in direct field conditions with complex soil, mulch, or weed backgrounds.
2. **Co-Infection**: The classification head assumes single-class dominance per leaf sample. In field scenarios where leaves suffer from both nutrient deficiency and fungal blight simultaneously, additional multi-label training is recommended.
