#!/usr/bin/env python3
"""
AI-AgriVision Model Training Pipeline
Production transfer-learning script using MobileNetV3Large/EfficientNetB0.
Features:
- Two-stage training: Frozen feature extractor head training, followed by fine-tuning
- Strict data augmentation without data leakage
- EarlyStopping, ModelCheckpoint, and ReduceLROnPlateau callbacks
- Automated generation and export of class_names.json and metrics.json
"""

import os
import sys
import json
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers
from sklearn.metrics import classification_report, confusion_matrix

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def parse_args():
    parser = argparse.ArgumentParser(description="Train AI-AgriVision Crop Disease Classifier")
    parser.add_argument("--data_dir", type=str, default="dataset", help="Path to dataset root")
    parser.add_argument("--epochs_head", type=int, default=15, help="Epochs for classification head")
    parser.add_argument("--epochs_finetune", type=int, default=10, help="Epochs for fine-tuning")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--output_model", type=str, default="app/models/crop_disease_model.keras", help="Model destination")
    parser.add_argument("--output_classes", type=str, default="app/models/class_names.json", help="Class names destination")
    parser.add_argument("--backbone", type=str, default="MobileNetV3Large", choices=["MobileNetV3Large", "MobileNetV2", "EfficientNetB0"])
    return parser.parse_args()

def build_data_pipelines(data_dir: str, batch_size: int):
    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "validation")
    test_dir = os.path.join(data_dir, "test")

    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        raise FileNotFoundError(f"Training or validation directories missing under {data_dir}")

    # Training pipeline with augmentation
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=True,
        seed=42
    )
    class_names = train_ds.class_names

    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=False
    )

    test_ds = None
    if os.path.exists(test_dir):
        test_ds = tf.keras.utils.image_dataset_from_directory(
            test_dir,
            image_size=IMG_SIZE,
            batch_size=batch_size,
            label_mode="categorical",
            shuffle=False
        )

    # Optimization: Prefetch and Cache
    train_ds = train_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
    if test_ds:
        test_ds = test_ds.prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names

def create_model(num_classes: int, backbone_name: str = "MobileNetV3Large"):
    # 1. Augmentation Layers (active only during training)
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),
    ], name="data_augmentation")

    inputs = layers.Input(shape=(224, 224, 3), name="input_image")
    x = data_augmentation(inputs)

    # 2. Backbone Pretrained Model
    if backbone_name == "MobileNetV3Large":
        # Preprocessing built into MobileNetV3
        x = layers.Rescaling(1./255)(x)
        base_model = tf.keras.applications.MobileNetV3Large(
            input_shape=(224, 224, 3),
            include_top=False,
            weights="imagenet"
        )
    elif backbone_name == "MobileNetV2":
        x = layers.Rescaling(1./127.5, offset=-1)(x)
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights="imagenet"
        )
    elif backbone_name == "EfficientNetB0":
        base_model = tf.keras.applications.EfficientNetB0(
            input_shape=(224, 224, 3),
            include_top=False,
            weights="imagenet"
        )
    else:
        raise ValueError(f"Unsupported backbone {backbone_name}")

    base_model.trainable = False
    x = base_model(x, training=False)

    # 3. Custom Classification Head
    x = layers.GlobalAveragePooling2D(name="avg_pool")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name=f"AgriVision_{backbone_name}")
    return model, base_model

def main():
    args = parse_args()
    print(f"[*] Starting AI-AgriVision Model Training with {args.backbone}...")

    train_ds, val_ds, test_ds, class_names = build_data_pipelines(args.data_dir, args.batch_size)
    num_classes = len(class_names)
    print(f"[*] Discovered {num_classes} classes: {class_names}")

    # Save class names
    os.makedirs(os.path.dirname(args.output_classes), exist_ok=True)
    with open(args.output_classes, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)
    print(f"[✓] Saved class names to {args.output_classes}")

    # Build model
    model, base_model = create_model(num_classes, args.backbone)

    # Stage 1: Train Classification Head
    print("\n--- Phase 1: Training Classification Head (Base Frozen) ---")
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )

    stage1_callbacks = [
        callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True, verbose=1),
        callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6, verbose=1)
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs_head,
        callbacks=stage1_callbacks
    )

    # Stage 2: Fine-Tuning
    print("\n--- Phase 2: Fine-Tuning Top Backbone Layers ---")
    base_model.trainable = True
    # Freeze the first 70% of base model layers, fine-tune the rest
    fine_tune_at = int(len(base_model.layers) * 0.70)
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),  # Lower learning rate for fine tuning
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )

    os.makedirs(os.path.dirname(args.output_model), exist_ok=True)
    stage2_callbacks = [
        callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1),
        callbacks.ModelCheckpoint(args.output_model, monitor="val_loss", save_best_only=True, verbose=1),
        callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-7, verbose=1)
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs_finetune,
        callbacks=stage2_callbacks
    )

    # Final Evaluation on Test Set if provided, or Validation Set
    eval_ds = test_ds if test_ds is not None else val_ds
    print("\n--- Final Model Evaluation ---")
    results = model.evaluate(eval_ds, verbose=1)
    metrics_summary = {
        "loss": float(results[0]),
        "accuracy": float(results[1]),
        "precision": float(results[2]),
        "recall": float(results[3]),
        "classes_count": num_classes
    }

    metrics_path = os.path.join(os.path.dirname(args.output_model), "training_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)

    print(f"[✓] Best model saved to: {args.output_model}")
    print(f"[✓] Metrics saved to: {metrics_path}")
    print(f"[✓] Final Validation/Test Accuracy: {metrics_summary['accuracy'] * 100:.2f}%")

if __name__ == "__main__":
    main()
