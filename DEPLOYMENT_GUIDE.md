# Deployment Guide - Whisper Large V3 Worker

Esta guía te ayudará a desplegar el worker de Whisper Large V3 en RunPod.

## Prerequisitos

1. **Cuenta de GitHub**: Para hospedar el código
2. **Cuenta de Docker Hub**: Para almacenar la imagen Docker
3. **Cuenta de RunPod**: Para ejecutar el worker serverless
4. **API Keys necesarios**:
   - Docker Hub Personal Access Token
   - RunPod API Key

## Paso 1: Configurar el Repositorio de GitHub

1. Crea un nuevo repositorio en GitHub (puede ser público o privado)
2. Clona este proyecto localmente
3. Conecta el proyecto con tu repositorio:

```bash
cd whisper-large-v3-worker
git remote add origin https://github.com/TU_USUARIO/whisper-large-v3-worker.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

## Paso 2: Configurar Docker Hub

1. Ve a [Docker Hub](https://hub.docker.com/)
2. Crea una cuenta si no tienes una
3. Genera un Personal Access Token:
   - Settings → Security → New Access Token
   - Nombre: "RunPod Worker"
   - Permisos: Read, Write, Delete
   - Guarda el token generado

## Paso 3: Configurar GitHub Secrets y Variables

Ve a tu repositorio en GitHub → Settings → Secrets and variables → Actions

### Secrets (secrets sensibles):
1. **DOCKERHUB_TOKEN**: Tu Docker Hub Personal Access Token
2. **RUNPOD_API_KEY**: Tu RunPod API Key (obtener en runpod.io/console/user/settings)

### Variables (públicas):
1. **DOCKERHUB_USERNAME**: Tu nombre de usuario de Docker Hub

## Paso 4: Actualizar el Workflow

Edita `.github/workflows/deploy.yml` y actualiza la línea del tag de Docker:

```yaml
tags: 'TU_USUARIO_DOCKERHUB/whisper-large-v3-worker:${{ github.sha }}'
```

Reemplaza `TU_USUARIO_DOCKERHUB` con tu usuario real de Docker Hub.

## Paso 5: Hacer Push y Deployar

```bash
git add .
git commit -m "Configure deployment"
git push origin main
```

GitHub Actions automáticamente:
1. Construirá la imagen Docker
2. La subirá a Docker Hub
3. Ejecutará tests en RunPod
4. Desplegará el worker

## Paso 6: Publicar en RunPod Hub (Opcional)

1. Ve a [RunPod Console](https://runpod.io/console)
2. Navega a "Serverless" → "Hub"
3. Click en "Add Endpoint"
4. Conecta tu repositorio de GitHub
5. RunPod leerá automáticamente `.runpod/hub.json` y configurará el worker

## Verificar el Deployment

### Ver los logs de GitHub Actions:
1. Ve a tu repositorio → Actions
2. Click en el último workflow run
3. Revisa los logs de cada step

### Probar el worker en RunPod:

```python
import requests

RUNPOD_API_KEY = "tu-api-key"
ENDPOINT_ID = "tu-endpoint-id"

url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"

payload = {
    "input": {
        "audio_url": "https://github.com/runpod-workers/sample-inputs/raw/main/audio/gettysburg.wav",
        "language": "en",
        "return_timestamps": True
    }
}

headers = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Estructura del Proyecto

```
whisper-large-v3-worker/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── .runpod/
│   ├── hub.json               # Configuración de RunPod Hub
│   └── tests.json             # Tests automáticos
├── builder/
│   ├── requirements.txt       # Dependencias Python
│   └── download_models.py     # Script para pre-descargar modelos
├── src/
│   ├── rp_handler.py          # Handler principal de RunPod
│   └── predict.py             # Lógica de predicción
├── Dockerfile                 # Configuración Docker
├── .gitignore
└── README.md
```

## Configuración Avanzada

### Cambiar el modelo de Whisper

En `src/predict.py` y `builder/download_models.py`, cambia:

```python
model_id = "openai/whisper-large-v3"
```

Por otro modelo como:
- `openai/whisper-large-v2`
- `openai/whisper-medium`
- `openai/whisper-small`

### Ajustar GPU requerida

En `.runpod/hub.json`, modifica:

```json
"config": {
    "gpuIds": "ADA_24",  // RTX 4090
    "containerDiskInGb": 25
}
```

Opciones de GPU:
- `"ADA_24"`: RTX 4090 (24GB)
- `"ADA_48"`: RTX 6000 Ada (48GB)
- `"AMPERE_80"`: A100 (80GB)

## Troubleshooting

### Error: "Model not found"
- Verifica que el modelo se descargó correctamente durante el build
- Revisa los logs de Docker build

### Error: "Out of memory"
- Reduce el `batch_size` en los requests
- Usa una GPU con más VRAM
- Cambia a un modelo más pequeño (medium o small)

### Tests fallan en GitHub Actions
- Verifica que el `RUNPOD_API_KEY` sea válido
- Asegúrate de que el audio de prueba sea accesible
- Revisa los logs del test runner

### Deployment no aparece en RunPod Hub
- Verifica que `.runpod/hub.json` esté correctamente formateado
- Asegúrate de que el repositorio esté conectado en RunPod Console
- Intenta hacer un nuevo push para triggerar el workflow

## Soporte

Para problemas o preguntas:
- GitHub Issues: Crea un issue en tu repositorio
- RunPod Discord: [discord.gg/runpod](https://discord.gg/runpod)
- RunPod Docs: [docs.runpod.io](https://docs.runpod.io)

## Próximos Pasos

1. **Optimizar rendimiento**: Experimenta con batch sizes y chunk lengths
2. **Agregar features**: Word-level timestamps, speaker diarization, etc.
3. **Monitorear costos**: Revisa el uso de GPU en RunPod Console
4. **Escalar**: Configura auto-scaling en RunPod para manejar picos de tráfico.
