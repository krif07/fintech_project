from .db_config import get_db_connection
from .schemas import ClienteCreate, CuentaCreate
import hashlib

def crear_cliente(cliente_data: ClienteCreate) -> dict:
    """Crea un nuevo cliente en la base de datos."""
    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    
    cursor = conn.cursor(dictionary=True)
    
    # Verificar si el email o DNI ya existen
    cursor.execute("SELECT email FROM clientes WHERE email = %s OR dni = %s", (cliente_data.email, cliente_data.dni))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("El email o DNI ya está registrado.")

    password_hash = hashlib.sha256(cliente_data.password.encode()).hexdigest()
    
    query = """
        INSERT INTO clientes (nombre, apellido, dni, email, password_hash)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (cliente_data.nombre, cliente_data.apellido, cliente_data.dni, cliente_data.email, password_hash))
    id_cliente = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT id_cliente, nombre, apellido, dni, email, fecha_creacion FROM clientes WHERE id_cliente = %s", (id_cliente,))
    nuevo_cliente = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return nuevo_cliente

def crear_cuenta(cuenta_data: CuentaCreate) -> dict:
    """Crea una nueva cuenta para un cliente en la base de datos."""
    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
        
    cursor = conn.cursor(dictionary=True)
    
    # Verificar que el cliente exista
    cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = %s", (cuenta_data.id_cliente,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("El cliente no existe.")
        
    query = "INSERT INTO cuentas (id_cliente, saldo) VALUES (%s, %s)"
    cursor.execute(query, (cuenta_data.id_cliente, cuenta_data.saldo_inicial))
    id_cuenta = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT id_cuenta, id_cliente, saldo, fecha_creacion FROM cuentas WHERE id_cuenta = %s", (id_cuenta,))
    nueva_cuenta = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return nueva_cuenta

def realizar_deposito(id_cuenta: int, monto: float) -> dict:
    """Deposita un monto en una cuenta y registra el movimiento."""
    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Iniciar transacción
        conn.start_transaction()
        
        # Actualizar saldo
        cursor.execute("UPDATE cuentas SET saldo = saldo + %s WHERE id_cuenta = %s", (monto, id_cuenta))
        
        # Registrar movimiento
        cursor.execute("INSERT INTO movimientos (id_cuenta, tipo_movimiento, monto) VALUES (%s, 'deposito', %s)", (id_cuenta, monto))
        
        conn.commit()
        
        # Obtener saldo actualizado
        cursor.execute("SELECT saldo FROM cuentas WHERE id_cuenta = %s", (id_cuenta,))
        resultado = cursor.fetchone()
        
        return resultado
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def realizar_retiro(id_cuenta: int, monto: float) -> dict:
    """Retira un monto de una cuenta si hay fondos suficientes."""
    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        conn.start_transaction()
        
        # Verificar fondos suficientes (con bloqueo para evitar concurrencia)
        cursor.execute("SELECT saldo FROM cuentas WHERE id_cuenta = %s FOR UPDATE", (id_cuenta,))
        cuenta = cursor.fetchone()
        
        if not cuenta or cuenta['saldo'] < monto:
            conn.rollback()
            raise ValueError("Fondos insuficientes o cuenta no existe.")
            
        # Actualizar saldo
        cursor.execute("UPDATE cuentas SET saldo = saldo - %s WHERE id_cuenta = %s", (monto, id_cuenta))
        
        # Registrar movimiento
        cursor.execute("INSERT INTO movimientos (id_cuenta, tipo_movimiento, monto) VALUES (%s, 'retiro', %s)", (id_cuenta, monto))
        
        conn.commit()
        
        return {"saldo": cuenta['saldo'] - monto}
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def obtener_saldo(id_cuenta: int) -> dict:
    """Obtiene el saldo de una cuenta específica."""
    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT saldo FROM cuentas WHERE id_cuenta = %s", (id_cuenta,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not resultado:
        raise ValueError("La cuenta no existe.")
        
    return resultado
