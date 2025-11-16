#!/usr/bin/env python3
"""
Pre-download Whisper Large V3 model during Docker build
This reduces cold start time for RunPod workers
"""

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

print("=" * 60)
print("Downloading Whisper Large V3 Model")
print("=" * 60)

model_id = "openai/whisper-large-v3"

# Determine device and dtype
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

print(f"Device: {device}")
print(f"Dtype: {torch_dtype}")

# Download model
print(f"\nDownloading model from: {model_id}")
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True
)

# Download processor (tokenizer + feature extractor)
print(f"\nDownloading processor from: {model_id}")
processor = AutoProcessor.from_pretrained(model_id)

print("\n" + "=" * 60)
print("Model download completed successfully!")
print("=" * 60)
