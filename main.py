from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time
import io
import csv
from database import get_connection, get_cursor

app = FastAPI(title="Sistema de Transporte AQP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# MODELOS (estructura de los datos que recibe cada endpoint)
# ─────────────────────────────────────────────

class UbicacionInicial(BaseModel):
    latitud: float
    longitud: float

class AsignacionInicial(BaseModel):
    id_conductor: int
    turno: str  # "mañana", "tarde", "noche"

class RegistrarBusCompleto(BaseModel):
    # Datos del bus
    placa: str
    capacidad: int
    estado: str
    id_empresa: int
    id_terminal: int
    # Datos de la ubicación inicial
    ubicacion: UbicacionInicial
    # Datos de la asignación del conductor
    asignacion: AsignacionInicial


class ParaderoEnRuta(BaseModel):
    id_paradero: int
    orden: int
    tiempo_llegada_estimado: Optional[str] = None  # ej: "00:15:00"

class HorarioRuta(BaseModel):
    hora_salida: str   # ej: "06:00:00"
    hora_llegada: str  # ej: "07:30:00"
    frecuencia: Optional[str] = None  # ej: "00:30:00"

class CrearRutaCompleta(BaseModel):
    # Datos de la ruta
    nombre_ruta: str
    codigo_ruta: str
    tiempo_estimado: Optional[int] = None  # en minutos
    id_empresa: int
    # Lista de paraderos en orden
    paraderos: List[ParaderoEnRuta]
    # Horario
    horario: HorarioRuta


class RegistrarIncidencia(BaseModel):
    id_bus: int
    id_centro: int
    id_pasajero: int
    descripcion: str
    tipo: str
    # Mensaje de notificación que se enviará al pasajero
    mensaje_notificacion: str


# ─────────────────────────────────────────────
# ENDPOINT 1: Registrar bus completo
# Tablas: bus + asignacion_conductor + ubicacion_bus
# ─────────────────────────────────────────────

@app.post("/buses/registrar-completo", tags=["Buses"])
def registrar_bus_completo(datos: RegistrarBusCompleto):
    """
    Registra un bus nuevo junto con su ubicación inicial
    y la asignación de su conductor, todo en una sola transacción.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        # 1. Insertar el bus
        cur.execute("""
            INSERT INTO bus (placa, capacidad, estado, id_empresa, id_terminal)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_bus
        """, (datos.placa, datos.capacidad, datos.estado, datos.id_empresa, datos.id_terminal))
        id_bus = cur.fetchone()["id_bus"]

        # 2. Insertar la ubicación inicial del bus
        cur.execute("""
            INSERT INTO ubicacion_bus (latitud, longitud, fecha_hora, id_bus)
            VALUES (%s, %s, NOW(), %s)
        """, (datos.ubicacion.latitud, datos.ubicacion.longitud, id_bus))

        # 3. Crear la asignación del conductor
        cur.execute("""
            INSERT INTO asignacion_conductor (fecha_asignacion, turno, estado, id_conductor, id_bus)
            VALUES (CURRENT_DATE, %s, 'activo', %s, %s)
        """, (datos.asignacion.turno, datos.asignacion.id_conductor, id_bus))

        conn.commit()
        return {
            "mensaje": "Bus registrado exitosamente",
            "id_bus": id_bus
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# ENDPOINT 2: Crear ruta completa
# Tablas: ruta + recorrido_ruta + horario
# ─────────────────────────────────────────────

@app.post("/rutas/crear-completa", tags=["Rutas"])
def crear_ruta_completa(datos: CrearRutaCompleta):
    """
    Crea una ruta con todos sus paraderos en orden
    y su horario, todo en una sola transacción.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        # 1. Insertar la ruta
        cur.execute("""
            INSERT INTO ruta (nombre_ruta, codigo_ruta, tiempo_estimado, id_empresa)
            VALUES (%s, %s, %s, %s)
            RETURNING id_ruta
        """, (datos.nombre_ruta, datos.codigo_ruta, datos.tiempo_estimado, datos.id_empresa))
        id_ruta = cur.fetchone()["id_ruta"]

        # 2. Insertar cada paradero del recorrido
        for paradero in datos.paraderos:
            cur.execute("""
                INSERT INTO recorrido_ruta (orden_paradero, tiempo_llegada_estimado, id_ruta, id_paradero)
                VALUES (%s, %s, %s, %s)
            """, (paradero.orden, paradero.tiempo_llegada_estimado, id_ruta, paradero.id_paradero))

        # 3. Insertar el horario
        cur.execute("""
            INSERT INTO horario (hora_salida, hora_llegada, frecuencia, id_ruta)
            VALUES (%s, %s, %s, %s)
        """, (datos.horario.hora_salida, datos.horario.hora_llegada, datos.horario.frecuencia, id_ruta))

        conn.commit()
        return {
            "mensaje": "Ruta creada exitosamente",
            "id_ruta": id_ruta,
            "paraderos_agregados": len(datos.paraderos)
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# ENDPOINT 3: Registrar incidencia completa
# Tablas: incidencia + notificacion + registro_control
# ─────────────────────────────────────────────

@app.post("/incidencias/registrar-completa", tags=["Incidencias"])
def registrar_incidencia_completa(datos: RegistrarIncidencia):
    """
    Registra una incidencia, envía automáticamente una notificación
    al pasajero afectado y crea un registro en el centro de control.
    Todo en una sola transacción.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        # 1. Registrar la incidencia
        cur.execute("""
            INSERT INTO incidencia (id_bus, id_centro, id_pasajero, descripcion, tipo, fecha_reporte)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id_incidencia
        """, (datos.id_bus, datos.id_centro, datos.id_pasajero, datos.descripcion, datos.tipo))
        id_incidencia = cur.fetchone()["id_incidencia"]

        # 2. Enviar notificación al pasajero
        cur.execute("""
            INSERT INTO notificacion (id_centro, id_pasajero, mensaje, fecha_envio, tipo)
            VALUES (%s, %s, %s, NOW(), %s)
        """, (datos.id_centro, datos.id_pasajero, datos.mensaje_notificacion, "incidencia"))

        # 3. Crear registro en el centro de control
        cur.execute("""
            INSERT INTO registro_control (id_bus, id_centro, fecha_hora, retraso_minutos, observacion)
            VALUES (%s, %s, NOW(), 0, %s)
        """, (datos.id_bus, datos.id_centro, f"Incidencia #{id_incidencia}: {datos.tipo}"))

        conn.commit()
        return {
            "mensaje": "Incidencia registrada, notificación enviada y registro de control creado",
            "id_incidencia": id_incidencia
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# ENDPOINT 4: Consultar estado completo de un bus
# Tablas: bus + ubicacion_bus + asignacion_conductor + conductor
# ─────────────────────────────────────────────

@app.get("/buses/{id_bus}/estado-completo", tags=["Buses"])
def estado_completo_bus(id_bus: int):
    """
    Retorna toda la información de un bus: sus datos, ubicación más reciente,
    conductor asignado y turno actual. Usa JOIN entre 4 tablas.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("""
            SELECT
                b.id_bus,
                b.placa,
                b.capacidad,
                b.estado AS estado_bus,
                ub.latitud,
                ub.longitud,
                ub.fecha_hora AS ultima_ubicacion,
                c.nombres AS conductor,
                c.licencia,
                ac.turno,
                ac.estado AS estado_asignacion,
                ac.fecha_asignacion
            FROM bus b
            LEFT JOIN LATERAL (
                SELECT latitud, longitud, fecha_hora
                FROM ubicacion_bus
                WHERE id_bus = b.id_bus
                ORDER BY fecha_hora DESC
                LIMIT 1
            ) ub ON true
            LEFT JOIN asignacion_conductor ac
                ON ac.id_bus = b.id_bus AND ac.estado = 'activo'
            LEFT JOIN conductor c
                ON c.id_conductor = ac.id_conductor
            WHERE b.id_bus = %s
        """, (id_bus,))

        resultado = cur.fetchone()
        if not resultado:
            raise HTTPException(status_code=404, detail="Bus no encontrado")
        return resultado
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# ENDPOINT 5: Reporte de incidencias por empresa
# Agregaciones: GROUP BY + HAVING — exportable a CSV
# ─────────────────────────────────────────────

@app.get("/reportes/incidencias-por-empresa", tags=["Reportes"])
def reporte_incidencias_por_empresa(
    minimo_incidencias: int = 1,
    exportar_csv: bool = False
):
    """
    Agrupa las incidencias por empresa de transporte usando GROUP BY y HAVING.
    Si exportar_csv=true, descarga el resultado como archivo CSV.

    Ejemplo: /reportes/incidencias-por-empresa?minimo_incidencias=3&exportar_csv=true
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("""
            SELECT
                et.id_empresa,
                et.nombre AS empresa,
                et.ruc,
                COUNT(i.id_incidencia) AS total_incidencias,
                COUNT(CASE WHEN i.tipo = 'accidente' THEN 1 END) AS accidentes,
                COUNT(CASE WHEN i.tipo = 'retraso' THEN 1 END) AS retrasos,
                COUNT(CASE WHEN i.tipo = 'falla_mecanica' THEN 1 END) AS fallas_mecanicas,
                COUNT(DISTINCT i.id_bus) AS buses_con_incidencias
            FROM empresa_transporte et
            JOIN bus b ON b.id_empresa = et.id_empresa
            JOIN incidencia i ON i.id_bus = b.id_bus
            GROUP BY et.id_empresa, et.nombre, et.ruc
            HAVING COUNT(i.id_incidencia) >= %s
            ORDER BY total_incidencias DESC
        """, (minimo_incidencias,))

        filas = cur.fetchall()

        # Si piden exportar, devolver CSV para descargar
        if exportar_csv:
            output = io.StringIO()
            if filas:
                writer = csv.DictWriter(output, fieldnames=filas[0].keys())
                writer.writeheader()
                writer.writerows(filas)
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=incidencias_por_empresa.csv"}
            )

        return {"total_empresas": len(filas), "datos": filas}
    finally:
        cur.close()
        conn.close()
