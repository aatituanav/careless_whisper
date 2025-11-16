# Project Structure

## Overview

Este proyecto es un worker serverless para RunPod que utiliza el modelo Whisper Large V3 de OpenAI para transcripción automática de audio.

## Directory Structure

```
whisper-large-v3-worker/
│
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions: Build, push y test
│
├── .runpod/
│   ├── hub.json                   # Configuración de RunPod Hub
│   └── tests.json                 # Tests automáticos de RunPod
│
├── builder/
│   ├── download_models.py         # Pre-descarga modelos en Docker build
│   └── requirements.txt           # Dependencias Python
│
├── src/
│   ├── rp_handler.py             # Handler principal de RunPod
│   └── predict.py                # Lógica de predicción con Whisper
│
├── examples/
│   ├── client_examples.py        # Ejemplos de uso del API
│   └── README.md                 # Documentación de ejemplos
│
├── Dockerfile                     # Docker image configuration
├── .gitignore                    # Archivos ignorados por Git
├── README.md                     # Documentación principal
├── DEPLOYMENT_GUIDE.md          # Guía de deployment paso a paso
├── PROJECT_STRUCTURE.md         # Este archivo
└── test_local.py                # Script para testing local
```

## Archivos Clave

### Configuración de RunPod

#### `.runpod/hub.json`
Define metadatos del worker para RunPod Hub:
- Título y descripción
- Tipo (serverless)
- Categoría (audio)
- GPU requerida
- Versiones de CUDA soportadas

#### `.runpod/tests.json`
Define tests automáticos que RunPod ejecuta:
- Casos de prueba con inputs de ejemplo
- Timeouts
- Configuración de GPU para tests

### Docker

#### `Dockerfile`
Construye la imagen Docker:
1. Base: NVIDIA CUDA 12.1 con cuDNN
2. Instala Python 3.10 y dependencias del sistema
3. Instala dependencias Python
4. Pre-descarga modelos de Whisper
5. Copia código de la aplicación
6. Define comando de inicio

#### `builder/requirements.txt`
Lista de dependencias Python:
- PyTorch con soporte CUDA
- Transformers de Hugging Face
- Bibliotecas de procesamiento de audio
- RunPod SDK

#### `builder/download_models.py`
Script que se ejecuta durante Docker build:
- Descarga Whisper Large V3 desde Hugging Face
- Descarga processor (tokenizer + feature extractor)
- Cachea modelos en la imagen para cold starts rápidos

### Aplicación

#### `src/rp_handler.py`
Handler principal que RunPod ejecuta:
- Función `handler(job)` que procesa requests
- Descarga archivos de audio desde URLs
- Llama al predictor
- Maneja errores y cleanup
- Inicia el servidor serverless con `runpod.serverless.start()`

#### `src/predict.py`
Clase `WhisperPredictor`:
- Inicializa modelo Whisper Large V3
- Crea pipeline de Hugging Face
- Método `predict()` para transcribir/traducir audio
- Maneja diferentes configuraciones (language, task, timestamps, etc.)

### Deployment

#### `.github/workflows/deploy.yml`
GitHub Actions workflow:
1. Checkout del código
2. Login a Docker Hub
3. Build y push de imagen Docker
4. Ejecuta tests en RunPod
5. Se activa con push a `main` branch

### Testing

#### `test_local.py`
Script para testing local:
- Inicializa el predictor
- Ejecuta transcripciones de prueba
- Útil para desarrollo y debugging

#### `examples/client_examples.py`
Ejemplos de cómo usar el API desde cliente:
- Requests síncronos y asíncronos
- Batch processing
- Error handling
- Diferentes configuraciones

## Flujo de Datos

### 1. Request → RunPod
```
Cliente → RunPod API → Worker Container
```

### 2. Dentro del Worker
```
rp_handler.py
    ↓
    1. Descarga audio desde URL
    ↓
    2. Llama a predict.py
    ↓
    3. WhisperPredictor procesa audio
    ↓
    4. Retorna transcripción
    ↓
    5. Cleanup
```

### 3. Response → Cliente
```
Worker → RunPod API → Cliente
```

## Variables de Entorno

El proyecto NO requiere variables de entorno en runtime (modelos pre-descargados).

Para deployment necesitas configurar en GitHub:
- `DOCKERHUB_TOKEN` (secret)
- `RUNPOD_API_KEY` (secret)
- `DOCKERHUB_USERNAME` (variable)

## Customización

### Cambiar Modelo de Whisper

Edita en `src/predict.py` y `builder/download_models.py`:

```python
model_id = "openai/whisper-large-v3"  # Cambiar a otro modelo
```

Opciones:
- `openai/whisper-large-v2`
- `openai/whisper-medium`
- `openai/whisper-small`
- `openai/whisper-base`
- `openai/whisper-tiny`

### Ajustar GPU

Edita `.runpod/hub.json`:

```json
"config": {
    "gpuIds": "ADA_24",  // Cambiar según necesidades
    "containerDiskInGb": 25
}
```

### Agregar Features

Modifica `src/predict.py` para agregar:
- Post-processing de transcripciones
- Detección de idioma mejorada
- Filtros de audio
- etc.

## Requisitos del Sistema

### Para Build
- Docker con soporte GPU
- ~20GB espacio en disco
- Conexión a internet (descarga modelos)

### Para Runtime en RunPod
- GPU NVIDIA con CUDA 12.1+
- ~6GB VRAM
- ~20GB espacio en disco

## Performance

### Cold Start
- ~10-20 segundos (modelos pre-cargados en imagen)

### Inference Time
- Varía según:
  - Longitud del audio
  - Batch size
  - GPU utilizada
  - Si se usan timestamps

Ejemplo: Audio de 1 minuto en RTX 4090
- Sin timestamps: ~2-3 segundos
- Con timestamps: ~4-5 segundos
- Con word-level timestamps: ~6-8 segundos

## Monitoreo

### Logs
- Logs en GitHub Actions para build/test
- Logs en RunPod Console para runtime
- `rp_handler.py` incluye logging detallado

### Métricas
RunPod Console muestra:
- Request count
- Execution time
- GPU utilization
- Costos

## Troubleshooting

Ver [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) sección Troubleshooting para:
- Errores comunes
- Soluciones
- Tips de debugging
