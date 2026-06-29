import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="SISTEMA_DE_GESTION_DE_TRANSPORTE_AQP",
        user="postgres",       # cambia por tu usuario
        password="guetatsvqp", # cambia por tu contraseña
        port="5432"
    )

def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)