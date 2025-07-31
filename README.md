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

✅ 1. Abre Visual Studio Code en tu carpeta del proyecto
Por ejemplo:

bash
Copiar
Editar
cd C:\Users\AsusTUF\Documents\EducacionIT\Programación OO con IA\proyecto integrador\fintech_project
code .

✅ 2. Crea un entorno virtual
Ejecutá este comando en la terminal integrada de VS Code:

bash
Copiar
Editar
python -m venv venv
Esto creará una carpeta llamada venv/ con el entorno virtual.

✅ 3. Activa el entorno virtual
En Windows (cmd o PowerShell):
bash
Copiar
Editar
venv\Scripts\activate
Una vez activado, deberías ver algo como esto en la terminal:

bash
Copiar
Editar
(venv) C:\Users\AsusTUF\Documents\...\
✅ 4. Instala las dependencias necesarias
Por ejemplo, para FastAPI y Uvicorn (servidor ASGI):

bash
Copiar
Editar
pip install fastapi uvicorn
Podés ir agregando más librerías que necesites (como SQLAlchemy, Pydantic, etc.).

✅ 5. Guarda las dependencias en requirements.txt (opcional, pero recomendado)
bash
Copiar
Editar
pip freeze > requirements.txt
Esto te permite que cualquier otra persona (o vos en otra máquina) pueda instalar todo de golpe con:

bash
Copiar
Editar
pip install -r requirements.txt
✅ 6. [VS Code] Seleccioná el intérprete de Python correcto
Presioná Ctrl+Shift+P → "Python: Select Interpreter" → seleccioná el que diga algo como:

Copiar
Editar
.\venv\Scripts\python.exe
