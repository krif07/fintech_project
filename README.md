# =============================================================================
# INSTRUCCIONES DE CONFIGURACIÓN Y EJECUCIÓN
# =============================================================================
#
# 1. ESTRUCTURA DE CARPETAS:
#    Crea la siguiente estructura de carpetas y archivos en tu computadora.
#
#    /fintech_project
#    |-- app/
#    |   |-- __init__.py         (Archivo vacío)
#    |   |-- api.py              (Contendrá los endpoints de la API)
#    |   |-- models.py           (Contendrá las clases y la "base de datos" en memoria)
#    |   |-- schemas.py          (Contendrá los modelos de datos para validación con Pydantic)
#    |   `-- services.py         (Contendrá la lógica de negocio)
#    |
#    |-- main.py                 (El punto de entrada para iniciar el servidor)
#    `-- requirements.txt        (Las dependencias del proyecto)
#
# 2. COPIA EL CÓDIGO:
#    Copia el contenido de cada sección de este bloque en el archivo correspondiente.
#
# 3. INSTALACIÓN:
#    Abre tu terminal en la carpeta 'fintech_project' y ejecuta:
#    pip install -r requirements.txt
#
# 4. EJECUCIÓN:
#    En la misma terminal, ejecuta el siguiente comando para iniciar el servidor:
#    uvicorn main:app --reload
#
# 5. PRUEBA LA API:
#    Abre tu navegador y ve a http://127.0.0.1:8000/docs
#    Verás la documentación interactiva para probar todos los endpoints.
#
# =============================================================================

# --- FILENAME: requirements.txt ---
# fastapi: El framework web para construir la API.
# uvicorn: El servidor ASGI para ejecutar la aplicación FastAPI.
# python-multipart: Necesario para manejar formularios.
#
# Contenido para requirements.txt:
# fastapi==0.110.0
# uvicorn[standard]==0.29.0
# python-multipart==0.0.9