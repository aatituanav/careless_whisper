# Client Examples

This directory contains examples of how to use the Whisper Large V3 RunPod worker from client applications.

## Setup

1. Install requirements:
```bash
pip install requests
```

2. Get your RunPod credentials:
   - API Key: https://runpod.io/console/user/settings
   - Endpoint ID: From your RunPod serverless endpoint

3. Update `client_examples.py` with your credentials:
```python
RUNPOD_API_KEY = "your-api-key"
ENDPOINT_ID = "your-endpoint-id"
```

## Running Examples

```bash
python client_examples.py
```

## Available Examples

1. **Basic Transcription**: Simple transcription with auto language detection
2. **With Language**: Specify language for better accuracy
3. **Translation**: Translate speech to English
4. **Async Request**: Handle long audio files asynchronously
5. **Batch Processing**: Process multiple files
6. **High Performance**: Optimized for speed
7. **Error Handling**: Proper error handling patterns

## API Modes

### Synchronous (runsync)
- Best for: Short audio files (<1 minute)
- Timeout: 90 seconds max
- Immediate response

### Asynchronous (run + status)
- Best for: Long audio files (>1 minute)
- No timeout limit
- Poll for results

## Language Codes

Common language codes:
- `en`: English
- `es`: Spanish
- `fr`: French
- `de`: German
- `it`: Italian
- `pt`: Portuguese
- `zh`: Chinese
- `ja`: Japanese
- `ko`: Korean
- `ar`: Arabic

See full list: https://github.com/openai/whisper#available-models-and-languages
