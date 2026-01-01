"""
Modulo encargado de crear la conexion a la base de datos
MySQL . Retorna un objeto de conexion que puede ser 
utilizado por el backend.
"""

import mysql.connector

def get_connection():
    """
    Crea y retorna una conexion a la base de datos MySQL.
    Lanza una excepcion si la conexion falla. 
    """
    try:
        return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root1234",
        database = "mini_backend"
    )
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        raise
