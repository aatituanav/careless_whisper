#!/usr/bin/env python3
"""
RunPod Serverless Handler for Whisper Large V3
"""

import runpod
from runpod.serverless.utils import download_files_from_urls, rp_cleanup
from predict import WhisperPredictor
import logging
import sys
import os
import shutil

# Setup logging
logger = logging.getLogger("whisper-handler")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Initialize predictor
logger.info("Initializing Whisper Large V3 predictor...")
predictor = WhisperPredictor()
logger.info("Predictor ready!")


def cleanup_job_files(job_id: str, jobs_directory: str = "/jobs"):
    """Clean up job files after processing"""
    job_path = os.path.join(jobs_directory, job_id)
    if os.path.exists(job_path):
        try:
            shutil.rmtree(job_path)
            logger.info(f"Cleaned up job directory: {job_path}")
        except Exception as e:
            logger.warning(f"Error cleaning up {job_path}: {e}")


def handler(job):
    """
    RunPod handler function

    Expected input:
    {
        "audio_url": "https://example.com/audio.mp3",
        "language": "en" (optional, None for auto-detect),
        "task": "transcribe" or "translate" (optional, default: transcribe),
        "return_timestamps": true/false/"word" (optional, default: true)
    }

    Note: batch_size and chunk_length_s are no longer supported as they cause
    memory issues. Whisper handles audio of any length natively and efficiently.
    """
    job_id = job["id"]
    job_input = job["input"]

    logger.info(f"Processing job {job_id}")

    try:
        # Validate input
        if "audio_url" not in job_input:
            return {"error": "Missing required parameter: audio_url"}

        # Download audio file
        logger.info(f"Downloading audio from: {job_input['audio_url']}")
        audio_paths = download_files_from_urls(job_id, [job_input["audio_url"]])
        audio_path = audio_paths[0]
        logger.info(f"Audio downloaded to: {audio_path}")

        # Extract parameters
        language = job_input.get("language", None)
        task = job_input.get("task", "transcribe")
        return_timestamps = job_input.get("return_timestamps", True)

        # Run prediction using Whisper's native long-form transcription
        # Note: batch_size and chunk_length_s are ignored as they cause memory issues
        # Whisper handles audio of any length natively and efficiently
        logger.info("Starting transcription...")
        result = predictor.predict(
            audio_path=audio_path,
            language=language,
            task=task,
            return_timestamps=return_timestamps
        )

        logger.info("Transcription completed successfully")

        # Cleanup
        cleanup_job_files(job_id)
        rp_cleanup.clean(["input_objects"])

        return result

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
        cleanup_job_files(job_id)
        return {"error": str(e)}


# Start the serverless worker
runpod.serverless.start({"handler": handler})
