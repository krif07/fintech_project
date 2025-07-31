from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# --- Esquemas para Clientes ---
class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, example="Juan")
    apellido: str = Field(..., min_length=2, example="Pérez")
    dni: str = Field(..., min_length=7, example="12345678")
    email: EmailStr = Field(..., example="juan.perez@email.com")

class ClienteCreate(ClienteBase):
    password: str = Field(..., min_length=8, example="micontraseña123")

class ClienteResponse(ClienteBase):
    id_cliente: str = Field(..., example="cli_1")
    fecha_creacion: str = Field(..., example="2024-07-30T10:00:00Z")

# --- Esquemas para Cuentas ---
class CuentaCreate(BaseModel):
    id_cliente: str = Field(..., example="cli_1")
    saldo_inicial: float = Field(0.0, ge=0, example=100.0)

class CuentaResponse(BaseModel):
    id_cuenta: str = Field(..., example="cta_1")
    id_cliente: str = Field(..., example="cli_1")
    saldo: float = Field(..., example=500.50)
    fecha_creacion: str

# --- Esquemas para Movimientos ---
class Movimiento(BaseModel):
    monto: float = Field(..., gt=0, example=50.0)

class MovimientoResponse(BaseModel):
    mensaje: str
    id_cuenta: str
    saldo_actual: float

class SaldoResponse(BaseModel):
    id_cuenta: str
    saldo: float

# --- Esquemas para Blockchain (Opcional) ---
class BlockResponse(BaseModel):
    index: int
    timestamp: float
    transaction: dict
    previous_hash: str
    hash: str