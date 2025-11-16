#!/usr/bin/env python3
"""
Whisper Large V3 Predictor
Based on Hugging Face Transformers implementation
"""

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import logging

logger = logging.getLogger(__name__)


class WhisperPredictor:
    """Predictor class for Whisper Large V3 model"""

    def __init__(self):
        """Initialize the model and processor"""
        self.model_id = "openai/whisper-large-v3"
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        logger.info(f"Loading model: {self.model_id}")
        logger.info(f"Device: {self.device}")
        logger.info(f"Dtype: {self.torch_dtype}")

        # Load model
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id,
            torch_dtype=self.torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True
        )
        self.model.to(self.device)

        # Load processor
        self.processor = AutoProcessor.from_pretrained(self.model_id)

        # Create pipeline
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

        logger.info("Model loaded successfully")

    def predict(
        self,
        audio_path: str,
        language: str = None,
        task: str = "transcribe",
        batch_size: int = 16,
        chunk_length_s: int = 30,
        return_timestamps: bool = True
    ):
        """
        Transcribe or translate audio

        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es', 'fr'). If None, auto-detect
            task: 'transcribe' or 'translate' (to English)
            batch_size: Batch size for processing
            chunk_length_s: Chunk length in seconds for long audio
            return_timestamps: True for segment timestamps, 'word' for word timestamps, False for none

        Returns:
            Dictionary with transcription results
        """
        logger.info(f"Transcribing: {audio_path}")
        logger.info(f"Language: {language or 'auto-detect'}")
        logger.info(f"Task: {task}")
        logger.info(f"Batch size: {batch_size}")

        # Build generation kwargs
        generate_kwargs = {
            "task": task,
            "language": language,
        }

        # Remove None values
        generate_kwargs = {k: v for k, v in generate_kwargs.items() if v is not None}

        # Run transcription
        result = self.pipe(
            audio_path,
            chunk_length_s=chunk_length_s,
            batch_size=batch_size,
            return_timestamps=return_timestamps,
            generate_kwargs=generate_kwargs
        )

        # Format output
        output = {
            "text": result["text"],
        }

        # Add chunks/timestamps if available
        if "chunks" in result:
            output["chunks"] = result["chunks"]

        logger.info(f"Transcription length: {len(result['text'])} characters")

        return output
