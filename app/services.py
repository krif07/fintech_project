from .models import db, Cliente, Cuenta, Block
from .schemas import ClienteCreate, CuentaCreate
import time

def crear_genesis_block():
    """Crea el primer bloque de la cadena si no existe."""
    if not db["blockchain"]:
        genesis_block = Block(0, time.time(), {"proof-of-work": 9, "transaction": "genesis_block"}, "0")
        db["blockchain"].append(genesis_block)

# Inicializa el blockchain
crear_genesis_block()

def registrar_transaccion_en_blockchain(tipo: str, id_cuenta: str, monto: float):
    """Añade un nuevo bloque a la cadena con la información de la transacción."""
    previous_block = db["blockchain"][-1]
    transaction_data = {
        "tipo": tipo,
        "id_cuenta": id_cuenta,
        "monto": monto,
        "timestamp": time.time()
    }
    nuevo_bloque = Block(
        index=previous_block.index + 1,
        timestamp=time.time(),
        transaction=transaction_data,
        previous_hash=previous_block.hash
    )
    db["blockchain"].append(nuevo_bloque)
    return nuevo_bloque

def crear_cliente(cliente_data: ClienteCreate) -> Cliente:
    """Crea un nuevo cliente y lo guarda en la 'base de datos'."""
    # Validación simple para evitar emails duplicados
    for cliente_existente in db["clientes"].values():
        if cliente_existente.email == cliente_data.email:
            raise ValueError(f"El email '{cliente_data.email}' ya está registrado.")

    nuevo_cliente = Cliente(
        nombre=cliente_data.nombre,
        apellido=cliente_data.apellido,
        dni=cliente_data.dni,
        email=cliente_data.email,
        password=cliente_data.password
    )
    db["clientes"][nuevo_cliente.id_cliente] = nuevo_cliente
    return nuevo_cliente

def crear_cuenta(cuenta_data: CuentaCreate) -> Cuenta:
    """Crea una nueva cuenta para un cliente existente."""
    if cuenta_data.id_cliente not in db["clientes"]:
        raise ValueError("El cliente no existe.")

    nueva_cuenta = Cuenta(
        id_cliente=cuenta_data.id_cliente,
        saldo_inicial=cuenta_data.saldo_inicial
    )
    db["cuentas"][nueva_cuenta.id_cuenta] = nueva_cuenta
    # Asocia la cuenta al cliente
    db["clientes"][cuenta_data.id_cliente].cuentas.append(nueva_cuenta.id_cuenta)
    return nueva_cuenta

def realizar_deposito(id_cuenta: str, monto: float) -> Cuenta:
    """Deposita un monto en una cuenta y registra la transacción."""
    if id_cuenta not in db["cuentas"]:
        raise ValueError("La cuenta no existe.")
    if monto <= 0:
        raise ValueError("El monto a depositar debe ser positivo.")

    cuenta = db["cuentas"][id_cuenta]
    cuenta.saldo += monto
    registrar_transaccion_en_blockchain("deposito", id_cuenta, monto)
    return cuenta

def realizar_retiro(id_cuenta: str, monto: float) -> Cuenta:
    """Retira un monto de una cuenta si hay fondos suficientes."""
    if id_cuenta not in db["cuentas"]:
        raise ValueError("La cuenta no existe.")
    if monto <= 0:
        raise ValueError("El monto a retirar debe ser positivo.")

    cuenta = db["cuentas"][id_cuenta]
    if cuenta.saldo < monto:
        raise ValueError("Fondos insuficientes.")

    cuenta.saldo -= monto
    registrar_transaccion_en_blockchain("retiro", id_cuenta, monto)
    return cuenta

def obtener_saldo(id_cuenta: str) -> Cuenta:
    """Obtiene el saldo de una cuenta específica."""
    if id_cuenta not in db["cuentas"]:
        raise ValueError("La cuenta no existe.")
    return db["cuentas"][id_cuenta]

def obtener_cadena_completa():
    """Devuelve toda la cadena de bloques."""
    return db["blockchain"]