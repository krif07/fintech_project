import datetime
import hashlib
import time

# --- Base de datos en memoria (para simulación) ---
# En un proyecto real, esto se reemplazaría por una base de datos como PostgreSQL o MySQL.
db = {
    "clientes": {},
    "cuentas": {},
    "blockchain": []
}

# --- Modelo para el Blockchain (Opcional) ---
class Block:
    """Representa un bloque en la cadena de transacciones (Blockchain)."""
    def __init__(self, index, timestamp, transaction, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calcula el hash del bloque."""
        block_string = str(self.index) + str(self.timestamp) + str(self.transaction) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

# --- Clases del Dominio (POO) ---
class Cliente:
    """Representa a un cliente de la fintech."""
    def __init__(self, nombre: str, apellido: str, dni: str, email: str, password: str):
        self.id_cliente = f"cli_{len(db['clientes']) + 1}"
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.password_hash = hashlib.sha256(password.encode()).hexdigest() # Guardar hash, no la contraseña
        self.cuentas = []
        self.fecha_creacion = datetime.datetime.now(datetime.timezone.utc).isoformat()

class Cuenta:
    """Representa una cuenta bancaria asociada a un cliente."""
    def __init__(self, id_cliente: str, saldo_inicial: float = 0.0):
        if id_cliente not in db["clientes"]:
            raise ValueError("El cliente especificado no existe.")
        self.id_cuenta = f"cta_{len(db['cuentas']) + 1}"
        self.id_cliente = id_cliente
        self.saldo = saldo_inicial
        self.fecha_creacion = datetime.datetime.now(datetime.timezone.utc).isoformat()
