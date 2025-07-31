from fastapi import APIRouter, HTTPException, status
from typing import List
from . import services, schemas

router = APIRouter()

@router.post("/clientes", response_model=schemas.ClienteResponse, status_code=status.HTTP_201_CREATED, tags=["Clientes"])
def crear_cliente(cliente_data: schemas.ClienteCreate):
    """
    Crea un nuevo cliente en el sistema.
    - **nombre**: Nombre del cliente.
    - **apellido**: Apellido del cliente.
    - **dni**: Documento Nacional de Identidad.
    - **email**: Correo electrónico (será usado para login).
    - **password**: Contraseña (mínimo 8 caracteres).
    """
    try:
        cliente = services.crear_cliente(cliente_data)
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/cuentas", response_model=schemas.CuentaResponse, status_code=status.HTTP_201_CREATED, tags=["Cuentas"])
def crear_cuenta(cuenta_data: schemas.CuentaCreate):
    """
    Crea una nueva cuenta bancaria para un cliente existente.
    - **id_cliente**: El ID del cliente al que pertenece la cuenta.
    - **saldo_inicial**: El monto con el que se abre la cuenta (opcional).
    """
    try:
        cuenta = services.crear_cuenta(cuenta_data)
        return cuenta
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/cuentas/{id_cuenta}/saldo", response_model=schemas.SaldoResponse, tags=["Cuentas"])
def get_saldo(id_cuenta: str):
    """Consulta el saldo de una cuenta específica."""
    try:
        cuenta = services.obtener_saldo(id_cuenta)
        return {"id_cuenta": id_cuenta, "saldo": cuenta.saldo}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/cuentas/{id_cuenta}/deposito", response_model=schemas.MovimientoResponse, tags=["Movimientos"])
def depositar_dinero(id_cuenta: str, movimiento: schemas.Movimiento):
    """Realiza un depósito en una cuenta."""
    try:
        cuenta_actualizada = services.realizar_deposito(id_cuenta, movimiento.monto)
        return {
            "mensaje": "Depósito realizado con éxito.",
            "id_cuenta": id_cuenta,
            "saldo_actual": cuenta_actualizada.saldo
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/cuentas/{id_cuenta}/retiro", response_model=schemas.MovimientoResponse, tags=["Movimientos"])
def retirar_dinero(id_cuenta: str, movimiento: schemas.Movimiento):
    """Realiza un retiro de una cuenta."""
    try:
        cuenta_actualizada = services.realizar_retiro(id_cuenta, movimiento.monto)
        return {
            "mensaje": "Retiro realizado con éxito.",
            "id_cuenta": id_cuenta,
            "saldo_actual": cuenta_actualizada.saldo
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# --- Endpoint Opcional de Blockchain ---
@router.get("/blockchain", response_model=List[schemas.BlockResponse], tags=["Blockchain (Opcional)"])
def get_blockchain():
    """Obtiene la cadena de bloques completa con todas las transacciones."""
    cadena = services.obtener_cadena_completa()
    return [block.__dict__ for block in cadena]