#!/usr/bin/env python3
"""
AI-AgriVision Model Export Script
Converts trained Keras model into optimized TensorFlow Lite (.tflite) format
for low-latency on-device or lightweight edge inference.
"""

import os
import sys
import argparse
import tensorflow as tf

def parse_args():
    parser = argparse.ArgumentParser(description="Export Keras Model to TFLite")
    parser.add_argument("--model_path", type=str, default="app/models/crop_disease_model.keras")
    parser.add_argument("--tflite_output", type=str, default="app/models/crop_disease_model.tflite")
    parser.add_argument("--quantize", action="store_true", help="Apply dynamic range quantization")
    return parser.parse_args()

def main():
    args = parse_args()

    if not os.path.exists(args.model_path):
        print(f"Model path {args.model_path} does not exist.")
        sys.exit(1)

    print(f"[*] Loading Keras model from {args.model_path}...")
    model = tf.keras.models.load_model(args.model_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    if args.quantize:
        print("[*] Applying dynamic range float16/int8 optimization...")
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_model = converter.convert()

    os.makedirs(os.path.dirname(args.tflite_output), exist_ok=True)
    with open(args.tflite_output, "wb") as f:
        f.write(tflite_model)

    size_mb = os.path.getsize(args.tflite_output) / (1024 * 1024)
    print(f"[✓] Successfully exported TFLite model to {args.tflite_output} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
