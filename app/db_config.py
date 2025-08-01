import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Crea y devuelve una conexión a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',       # O la IP de tu servidor de BD
            database='fintech_db',  # El nombre de tu base de datos
            user='root',            # Tu usuario de MySQL
            password='toor'  # Tu contraseña de MySQL
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
