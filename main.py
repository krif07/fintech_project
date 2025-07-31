from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Fintech API",
    description="API para la gestión de clientes y cuentas bancarias de una Fintech.",
    version="1.0.0"
)

# Incluir las rutas definidas en api.py
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "Bienvenido a la API de la Fintech. Visita /docs para la documentación."}

