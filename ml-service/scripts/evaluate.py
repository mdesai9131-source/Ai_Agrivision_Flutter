#!/usr/bin/env python3
"""
AI-AgriVision Model Evaluation Script
Computes overall accuracy, precision, recall, macro/weighted F1-scores,
and outputs a detailed per-class classification report and confusion matrix.
"""

import os
import sys
import json
import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate AI-AgriVision Crop Disease Classifier")
    parser.add_argument("--model_path", type=str, default="app/models/crop_disease_model.keras")
    parser.add_argument("--class_names_path", type=str, default="app/models/class_names.json")
    parser.add_argument("--test_dir", type=str, default="dataset/test")
    parser.add_argument("--output_report", type=str, default="app/models/evaluation_report.json")
    return parser.parse_args()

def main():
    args = parse_args()

    if not os.path.exists(args.model_path):
        print(f"Error: Model not found at {args.model_path}")
        sys.exit(1)

    with open(args.class_names_path, "r", encoding="utf-8") as f:
        class_names = json.load(f)

    print(f"[*] Loading model from {args.model_path}...")
    model = tf.keras.models.load_model(args.model_path)

    print(f"[*] Loading test dataset from {args.test_dir}...")
    test_ds = tf.keras.utils.image_dataset_from_directory(
        args.test_dir,
        image_size=(224, 224),
        batch_size=32,
        label_mode="categorical",
        shuffle=False
    )

    y_true = []
    y_pred = []

    print("[*] Running inference on test split...")
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )

    conf_matrix = confusion_matrix(y_true, y_pred).tolist()

    summary = {
        "classification_report": report_dict,
        "confusion_matrix": conf_matrix,
        "total_test_samples": int(len(y_true)),
        "accuracy": float(report_dict.get("accuracy", 0.0)),
        "macro_f1": float(report_dict.get("macro avg", {}).get("f1-score", 0.0)),
        "weighted_f1": float(report_dict.get("weighted avg", {}).get("f1-score", 0.0))
    }

    os.makedirs(os.path.dirname(args.output_report), exist_ok=True)
    with open(args.output_report, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[✓] Evaluation completed!")
    print(f"Accuracy:    {summary['accuracy'] * 100:.2f}%")
    print(f"Macro F1:    {summary['macro_f1']:.4f}")
    print(f"Weighted F1: {summary['weighted_f1']:.4f}")
    print(f"Report exported to: {args.output_report}")

if __name__ == "__main__":
    main()
