import hashlib

class Cliente:
    """Representa a un cliente. Ya no maneja su propio guardado."""
    def __init__(self, nombre: str, apellido: str, dni: str, email: str, password: str):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

class Cuenta:
    """Representa una cuenta bancaria. Ya no maneja su propio guardado."""
    def __init__(self, id_cliente: int, saldo_inicial: float = 0.0):
        self.id_cliente = id_cliente
        self.saldo = saldo_inicial