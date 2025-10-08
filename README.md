# RoboCopProject

Proyecto Python Flask para gestión de dispositivos Apple con Apple Business Manager API, tickets de activación por email Gmail y control local de iPhone vía WebDriverAgent.

## Requisitos

- Python 3.9+
- Archivo `credentials.json` OAuth2 para Gmail (Google Cloud Console)
- Archivo `AuthKey_<KEY_ID>.p8` para Apple Business Manager JWT
- iPhone conectado en modo desarrollador con WebDriverAgent corriendo (puerto 8100)

## Instalación

1. Clona o descarga el proyecto.
2. Crea y activa entorno virtual:
python -m venv venv
source venv/bin/activate

3. Instala dependencias:
pip install -r requirements.txt

4. Coloca los archivos `credentials.json` y `AuthKey_<KEY_ID>.p8` en la raíz del proyecto.
5. Configura variables en `config.py`.
6. Ejecuta la app:
python run.py

7. Abre navegador en http://localhost:5000

## Uso

- Accede a la web para administrar dispositivos Apple y aprobar tickets.
- Controla iPhone conectado con WebDriverAgent.
- Tokens Gmail se gestionan automáticamente.

## Notas

- WebDriverAgent debe estar corriendo en iPhone para control.
- Mantén tokens seguros y no los subas a repositorios públicos.

