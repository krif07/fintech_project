from fastapi import APIRouter, HTTPException, status
from typing import List
from . import services, schemas

router = APIRouter()

@router.post("/clientes", response_model=schemas.ClienteResponse, status_code=status.HTTP_201_CREATED, tags=["Clientes"])
def crear_cliente(cliente_data: schemas.ClienteCreate):
    try:
        cliente = services.crear_cliente(cliente_data)
        # Convertir fecha a string para la respuesta
        cliente['fecha_creacion'] = cliente['fecha_creacion'].isoformat()
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.post("/cuentas", response_model=schemas.CuentaResponse, status_code=status.HTTP_201_CREATED, tags=["Cuentas"])
def crear_cuenta(cuenta_data: schemas.CuentaCreate):
    try:
        cuenta = services.crear_cuenta(cuenta_data)
        cuenta['fecha_creacion'] = cuenta['fecha_creacion'].isoformat()
        return cuenta
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.get("/cuentas/{id_cuenta}/saldo", response_model=schemas.SaldoResponse, tags=["Cuentas"])
def get_saldo(id_cuenta: int):
    try:
        saldo_data = services.obtener_saldo(id_cuenta)
        return {"id_cuenta": id_cuenta, "saldo": saldo_data['saldo']}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.post("/cuentas/{id_cuenta}/deposito", response_model=schemas.MovimientoResponse, tags=["Movimientos"])
def depositar_dinero(id_cuenta: int, movimiento: schemas.Movimiento):
    try:
        resultado = services.realizar_deposito(id_cuenta, movimiento.monto)
        return {
            "mensaje": "Depósito realizado con éxito.",
            "id_cuenta": id_cuenta,
            "saldo_actual": resultado['saldo']
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.post("/cuentas/{id_cuenta}/retiro", response_model=schemas.MovimientoResponse, tags=["Movimientos"])
def retirar_dinero(id_cuenta: int, movimiento: schemas.Movimiento):
    try:
        resultado = services.realizar_retiro(id_cuenta, movimiento.monto)
        return {
            "mensaje": "Retiro realizado con éxito.",
            "id_cuenta": id_cuenta,
            "saldo_actual": resultado['saldo']
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


# --- FILENAME: main.py ---
# (Sin cambios, se mantiene igual)
from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Fintech API con MySQL",
    description="API para la gestión de clientes y cuentas bancarias de una Fintech, conectada a una base de datos MySQL.",
    version="1.1.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "Bienvenido a la API de la Fintech. Visita /docs para la documentación."}

