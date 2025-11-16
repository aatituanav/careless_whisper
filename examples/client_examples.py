#!/usr/bin/env python3
"""
Client examples for using the Whisper Large V3 RunPod worker
"""

import requests
import json
import time

# Configuration - Replace with your actual values
RUNPOD_API_KEY = "your-runpod-api-key-here"
ENDPOINT_ID = "your-endpoint-id-here"

# RunPod API endpoints
RUNSYNC_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
RUN_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
STATUS_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status"

HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}


def example_basic_transcription():
    """Basic transcription with auto language detection"""
    print("=" * 60)
    print("Example 1: Basic Transcription")
    print("=" * 60)

    payload = {
        "input": {
            "audio_url": "https://github.com/runpod-workers/sample-inputs/raw/main/audio/gettysburg.wav"
        }
    }

    response = requests.post(RUNSYNC_URL, json=payload, headers=HEADERS)
    result = response.json()

    print(json.dumps(result, indent=2))
    return result


def example_with_language():
    """Transcription with specified language"""
    print("\n" + "=" * 60)
    print("Example 2: Transcription with Language Specification")
    print("=" * 60)

    payload = {
        "input": {
            "audio_url": "https://example.com/spanish_audio.mp3",
            "language": "es",
            "return_timestamps": "word"
        }
    }

    response = requests.post(RUNSYNC_URL, json=payload, headers=HEADERS)
    result = response.json()

    print(json.dumps(result, indent=2))
    return result


def example_translation():
    """Translate speech to English"""
    print("\n" + "=" * 60)
    print("Example 3: Translation to English")
    print("=" * 60)

    payload = {
        "input": {
            "audio_url": "https://example.com/french_audio.mp3",
            "language": "fr",
            "task": "translate",
            "return_timestamps": True
        }
    }

    response = requests.post(RUNSYNC_URL, json=payload, headers=HEADERS)
    result = response.json()

    print(json.dumps(result, indent=2))
    return result


def example_async_request():
    """Asynchronous request for long audio files"""
    print("\n" + "=" * 60)
    print("Example 4: Async Request (for long audio)")
    print("=" * 60)

    # Submit job
    payload = {
        "input": {
            "audio_url": "https://example.com/long_audio.mp3",
            "batch_size": 24,
            "chunk_length_s": 30
        }
    }

    print("Submitting job...")
    response = requests.post(RUN_URL, json=payload, headers=HEADERS)
    job_data = response.json()
    job_id = job_data["id"]
    print(f"Job ID: {job_id}")

    # Poll for status
    while True:
        status_response = requests.get(f"{STATUS_URL}/{job_id}", headers=HEADERS)
        status_data = status_response.json()
        status = status_data.get("status")

        print(f"Status: {status}")

        if status == "COMPLETED":
            print("\nJob completed!")
            print(json.dumps(status_data["output"], indent=2))
            break
        elif status == "FAILED":
            print("\nJob failed!")
            print(json.dumps(status_data, indent=2))
            break

        time.sleep(2)  # Wait 2 seconds before checking again


def example_batch_processing():
    """Process multiple audio files"""
    print("\n" + "=" * 60)
    print("Example 5: Batch Processing")
    print("=" * 60)

    audio_files = [
        "https://example.com/audio1.mp3",
        "https://example.com/audio2.mp3",
        "https://example.com/audio3.mp3",
    ]

    results = []

    for i, audio_url in enumerate(audio_files, 1):
        print(f"\nProcessing file {i}/{len(audio_files)}: {audio_url}")

        payload = {
            "input": {
                "audio_url": audio_url,
                "language": "en",
                "return_timestamps": True
            }
        }

        response = requests.post(RUNSYNC_URL, json=payload, headers=HEADERS)
        result = response.json()
        results.append(result)

        print(f"Completed: {len(result.get('text', ''))} characters")

    print(f"\nProcessed {len(results)} files successfully")
    return results


def example_high_performance():
    """High performance configuration"""
    print("\n" + "=" * 60)
    print("Example 6: High Performance Configuration")
    print("=" * 60)

    payload = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "batch_size": 32,  # Larger batch size
            "chunk_length_s": 30,
            "return_timestamps": False  # Disable timestamps for speed
        }
    }

    start_time = time.time()
    response = requests.post(RUNSYNC_URL, json=payload, headers=HEADERS)
    end_time = time.time()

    result = response.json()

    print(f"Processing time: {end_time - start_time:.2f} seconds")
    print(json.dumps(result, indent=2))
    return result


def example_error_handling():
    """Proper error handling"""
    print("\n" + "=" * 60)
    print("Example 7: Error Handling")
    print("=" * 60)

    payload = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "language": "en"
        }
    }

    try:
        response = requests.post(RUNSYNC_URL, json=payload, headers=HEADERS, timeout=300)
        response.raise_for_status()  # Raise exception for HTTP errors

        result = response.json()

        # Check for RunPod errors
        if "error" in result:
            print(f"RunPod Error: {result['error']}")
            return None

        print("Success!")
        print(json.dumps(result, indent=2))
        return result

    except requests.exceptions.Timeout:
        print("Error: Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

    return None


if __name__ == "__main__":
    print("Whisper Large V3 RunPod Worker - Client Examples")
    print("\nMake sure to set your RUNPOD_API_KEY and ENDPOINT_ID!\n")

    # Run examples (comment out ones you don't want to run)
    # example_basic_transcription()
    # example_with_language()
    # example_translation()
    # example_async_request()
    # example_batch_processing()
    # example_high_performance()
    # example_error_handling()

    print("\nExamples completed!")
