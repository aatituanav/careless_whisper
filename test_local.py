#!/usr/bin/env python3
"""
Local testing script for Whisper Large V3 predictor
Run this to test the predictor before deploying to RunPod
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from predict import WhisperPredictor
import json


def test_predictor():
    """Test the predictor with a sample audio file"""
    print("=" * 60)
    print("Testing Whisper Large V3 Predictor")
    print("=" * 60)

    # Initialize predictor
    print("\nInitializing predictor...")
    predictor = WhisperPredictor()
    print("Predictor initialized successfully!")

    # You need to provide your own test audio file
    audio_path = "test_audio.mp3"  # Change this to your test file

    if not os.path.exists(audio_path):
        print(f"\nError: Audio file not found: {audio_path}")
        print("Please provide a test audio file and update the path in this script")
        return

    # Test 1: Basic transcription
    print("\n" + "=" * 60)
    print("Test 1: Basic Transcription")
    print("=" * 60)

    result = predictor.predict(
        audio_path=audio_path,
        return_timestamps=True
    )

    print("\nResult:")
    print(json.dumps(result, indent=2))

    # Test 2: With language specified
    print("\n" + "=" * 60)
    print("Test 2: With Language (English)")
    print("=" * 60)

    result = predictor.predict(
        audio_path=audio_path,
        language="en",
        return_timestamps="word"
    )

    print("\nResult:")
    print(json.dumps(result, indent=2))

    # Test 3: Translation task
    print("\n" + "=" * 60)
    print("Test 3: Translation to English")
    print("=" * 60)

    result = predictor.predict(
        audio_path=audio_path,
        task="translate",
        return_timestamps=False
    )

    print("\nResult:")
    print(json.dumps(result, indent=2))

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_predictor()
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
