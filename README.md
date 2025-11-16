# Whisper Large V3 Worker for RunPod

A serverless worker for automatic speech recognition using OpenAI's Whisper Large V3 model on RunPod.

## Features

- **State-of-the-art ASR**: Uses OpenAI's Whisper Large V3 model
- **Multi-language support**: Supports 99 languages with automatic language detection
- **Flexible transcription**: Word-level and segment-level timestamps
- **Translation**: Translate speech to English
- **Optimized for RunPod**: Pre-loaded models for fast cold starts
- **GPU accelerated**: Runs on NVIDIA GPUs with CUDA support

## Model Information

This worker uses the `openai/whisper-large-v3` model from Hugging Face:
- **Parameters**: 1550M
- **Languages**: 99 languages supported
- **Training data**: 1M hours of weakly labeled audio + 4M hours pseudo-labeled
- **Improvements**: 10-20% error reduction compared to Whisper Large V2

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `audio_url` | string | Yes | - | URL to the audio file |
| `language` | string | No | null | Language code (e.g., 'en', 'es', 'fr'). Auto-detected if not specified |
| `task` | string | No | "transcribe" | Task to perform: "transcribe" or "translate" |
| `batch_size` | int | No | 16 | Batch size for processing |
| `chunk_length_s` | int | No | 30 | Chunk length in seconds for long audio files |
| `return_timestamps` | bool/string | No | true | Return timestamps: true (segment), "word", or false |

## Usage Examples

### Basic Transcription

```json
{
  "input": {
    "audio_url": "https://example.com/audio.mp3"
  }
}
```

### Transcription with Language Specification

```json
{
  "input": {
    "audio_url": "https://example.com/spanish_audio.mp3",
    "language": "es",
    "return_timestamps": "word"
  }
}
```

### Translation to English

```json
{
  "input": {
    "audio_url": "https://example.com/french_audio.mp3",
    "language": "fr",
    "task": "translate"
  }
}
```

### High Performance Configuration

```json
{
  "input": {
    "audio_url": "https://example.com/long_audio.mp3",
    "batch_size": 24,
    "chunk_length_s": 30,
    "return_timestamps": true
  }
}
```

## Output Format

### With Segment Timestamps

```json
{
  "text": "Full transcription text...",
  "chunks": [
    {
      "timestamp": [0.0, 5.5],
      "text": "First segment text"
    },
    {
      "timestamp": [5.5, 12.0],
      "text": "Second segment text"
    }
  ]
}
```

### With Word Timestamps

```json
{
  "text": "Full transcription text...",
  "chunks": [
    {
      "timestamp": [0.0, 0.5],
      "text": "First"
    },
    {
      "timestamp": [0.5, 1.0],
      "text": "word"
    }
  ]
}
```

## Supported Languages

The model supports 99 languages including:
- English, Spanish, French, German, Italian, Portuguese
- Chinese, Japanese, Korean
- Arabic, Hebrew, Hindi
- Russian, Polish, Czech
- And many more...

For automatic detection, simply omit the `language` parameter.

## Performance Tips

1. **Batch Size**: Increase for better throughput on longer files (up to GPU memory limit)
2. **Chunk Length**: 30 seconds is optimal for most cases
3. **Timestamps**: Disable timestamps if not needed for faster processing
4. **Language**: Specify language when known for better accuracy

## Development

### Local Testing

```bash
# Build the Docker image
docker build -t whisper-large-v3-worker .

# Run locally
docker run --gpus all -p 8000:8000 whisper-large-v3-worker
```

### Deployment to RunPod

This project automatically deploys to RunPod when you push to the `main` branch:

1. Set up GitHub secrets:
   - `DOCKERHUB_TOKEN`: Your Docker Hub token
   - `RUNPOD_API_KEY`: Your RunPod API key

2. Set up GitHub variables:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username

3. Push to main branch - GitHub Actions will handle the rest!

## Requirements

- GPU with CUDA support (recommended: RTX 4090, A100, or similar)
- ~6GB VRAM for inference
- ~20GB disk space for model and dependencies

## License

This project uses the Whisper Large V3 model which is licensed under Apache 2.0.

## Credits

- OpenAI for the Whisper model
- Hugging Face for the Transformers library
- RunPod for the serverless platform
