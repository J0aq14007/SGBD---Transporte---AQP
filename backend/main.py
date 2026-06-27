from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "postgresql://postgres:AQPTransporte2026@localhost:5432/sistema_transporte_aqp"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==== Activar entorno virtual ====
# cd D:\Programacion\SistemaTransportesAQP\backend
# .\venv\Scripts\Activate.ps1

# ==== Levantar FastAPI ====
# uvicorn main:app --reload

# ==== GETS ====
@app.get("/")
def inicio():
    return {"mensaje": "Sistema de Transporte AQP funcionando"}

@app.get("/buses")
def listar_buses():
    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM bus")
    )

    buses = []

    for fila in resultado:
        buses.append({
            "id_bus": fila.id_bus,
            "placa": fila.placa,
            "capacidad": fila.capacidad,
            "estado": fila.estado
        })

    db.close()

    return buses

@app.get("/conductores")
def listar_conductores():
    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM conductor")
    )

    conductores = []

    for fila in resultado:
        conductores.append({
            "id_conductor": fila.id_conductor,
            "nombre": fila.nombres,
            "licencia": fila.licencia
        })

    db.close()

    return conductores

@app.get("/pasajeros")
def listar_pasajeros():
    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM pasajero")
    )

    pasajeros = []

    for fila in resultado:
        pasajeros.append({
            "id": fila.id_pasajero,
            "nombre": fila.nombres,
            "correo": fila.correo,
            "telefono": fila.telefono
        })

    db.close()

    return pasajeros

@app.get("/empresas")
def listar_empresas():
    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM empresa_transporte")
    )

    empresas = []

    for fila in resultado:
        empresas.append({
            "id": fila.id_empresa,
            "nombre": fila.nombre,
            "ruc": fila.ruc
        })

    db.close()

    return empresas

@app.get("/incidencias")
def listar_incidencias():
    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM incidencia")
    )

    incidencias = []

    for fila in resultado:
        incidencias.append({
            "id": fila.id_incidencia,
            "tipo": fila.tipo,
            "descripcion": fila.descripcion
        })

    db.close()

    return incidencias

@app.get("/rutas")
def listar_rutas():

    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM ruta")
    )

    rutas = []

    for fila in resultado:
        rutas.append({
            "id_ruta": fila.id_ruta,
            "nombre_ruta": fila.nombre_ruta,
            "codigo_ruta": fila.codigo_ruta,
            "tiempo_estimado": fila.tiempo_estimado
        })

    db.close()

    return rutas

@app.get("/terminales")
def listar_terminales():

    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM terminal")
    )

    terminales = []

    for fila in resultado:
        terminales.append({
            "id_terminal": fila.id_terminal,
            "nombre": fila.nombre,
            "distrito": fila.distrito,
            "capacidad": fila.capacidad_buses
        })

    db.close()

    return terminales

@app.get("/horarios")
def listar_horarios():

    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM horario")
    )

    horarios = []

    for fila in resultado:
        horarios.append({
            "id_horario": fila.id_horario,
            "hora_salida": str(fila.hora_salida),
            "hora_llegada": str(fila.hora_llegada),
            "id_ruta": fila.id_ruta
        })

    db.close()

    return horarios

@app.get("/paraderos")
def listar_paraderos():

    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM paradero")
    )

    paraderos = []

    for fila in resultado:
        paraderos.append({
            "id_paradero": fila.id_paradero,
            "nombre": fila.nombre,
            "direccion": fila.direccion
        })

    db.close()

    return paraderos

@app.get("/notificaciones")
def listar_notificaciones():

    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM notificacion")
    )

    notificaciones = []

    for fila in resultado:
        notificaciones.append({
            "id": fila.id_notificacion,
            "tipo": fila.tipo,
            "mensaje": fila.mensaje
        })

    db.close()

    return notificaciones

@app.get("/registro-control")
def listar_registro_control():

    db = SessionLocal()

    resultado = db.execute(
        text("SELECT * FROM registro_control")
    )

    registros = []

    for fila in resultado:
        registros.append({
            "id": fila.id_registro,
            "id_bus": fila.id_bus,
            "retraso": fila.retraso_minutos,
            "observacion": fila.observacion
        })

    db.close()

    return registros

# ==== POST ====
class Pasajero(BaseModel):
    nombres: str
    correo: str
    telefono: str

@app.post("/pasajeros")
def crear_pasajero(pasajero: Pasajero):

    db = SessionLocal()

    db.execute(
        text("""
            INSERT INTO pasajero
            (nombres, correo, telefono)
            VALUES
            (:nombres, :correo, :telefono)
        """),
        {
            "nombres": pasajero.nombres,
            "correo": pasajero.correo,
            "telefono": pasajero.telefono
        }
    )

    db.commit()
    db.close()

    return {"mensaje": "Pasajero registrado"}

class Incidencia(BaseModel):
    id_bus: int
    id_centro: int
    id_pasajero: int
    descripcion: str
    tipo: str

@app.post("/incidencias")
def crear_incidencia(incidencia: Incidencia):

    db = SessionLocal()

    db.execute(
        text("""
        INSERT INTO incidencia
        (
            id_bus,
            id_centro,
            id_pasajero,
            descripcion,
            tipo,
            fecha_reporte
        )
        VALUES
        (
            :id_bus,
            :id_centro,
            :id_pasajero,
            :descripcion,
            :tipo,
            NOW()
        )
        """),
        incidencia.model_dump()
    )

    db.commit()
    db.close()

    return {"mensaje": "Incidencia registrada"}

class Bus(BaseModel):
    placa: str
    capacidad: int
    estado: str
    id_empresa: int
    id_terminal: int

@app.post("/buses")
def crear_bus(bus: Bus):

    db = SessionLocal()

    db.execute(
        text("""
        INSERT INTO bus
        (placa, capacidad, estado, id_empresa, id_terminal)
        VALUES
        (:placa, :capacidad, :estado, :id_empresa, :id_terminal)
        """),
        {
            "placa": bus.placa,
            "capacidad": bus.capacidad,
            "estado": bus.estado,
            "id_empresa": bus.id_empresa,
            "id_terminal": bus.id_terminal
        }
    )

    db.commit()
    db.close()

    return {"mensaje": "Bus registrado"}

class Conductor(BaseModel):
    nombres: str
    licencia: str
    telefono: str
    fecha_ingreso: str

@app.post("/conductores")
def crear_conductor(conductor: Conductor):

    db = SessionLocal()

    db.execute(
        text("""
        INSERT INTO conductor
        (nombres, licencia, telefono, fecha_ingreso)
        VALUES
        (:nombres, :licencia, :telefono, :fecha_ingreso)
        """),
        {
            "nombres": conductor.nombres,
            "licencia": conductor.licencia,
            "telefono": conductor.telefono,
            "fecha_ingreso": conductor.fecha_ingreso
        }
    )

    db.commit()
    db.close()

    return {"mensaje": "Conductor registrado"}

# ==== Reportes ====
@app.get("/reportes/conductores")
def reporte_conductores():

    db = SessionLocal()

    resultado = db.execute(text("""
        SELECT
            c.nombres AS nombre_conductor,
            COUNT(ac.id_asignacion) AS total_asignaciones
        FROM conductor c
        JOIN asignacion_conductor ac
            ON c.id_conductor = ac.id_conductor
        GROUP BY c.nombres
        HAVING COUNT(ac.id_asignacion) >= 1
        ORDER BY total_asignaciones DESC
    """))

    datos = [dict(fila._mapping) for fila in resultado]

    db.close()

    return datos

@app.get("/reportes/incidencias")
def reporte_incidencias():

    db = SessionLocal()

    resultado = db.execute(text("""
        SELECT
            i.tipo AS tipo_incidencia,
            COUNT(i.id_incidencia) AS total_reportes
        FROM incidencia i
        GROUP BY i.tipo
        HAVING COUNT(i.id_incidencia) >= 1
        ORDER BY total_reportes DESC
    """))

    datos = [dict(fila._mapping) for fila in resultado]

    db.close()

    return datos

@app.get("/reportes/retrasos")
def reporte_retrasos():

    db = SessionLocal()

    resultado = db.execute(text("""
        SELECT
            b.placa AS placa_bus,
            r.retraso_minutos AS retraso_original,
            r.retraso_minutos + 10 AS retraso_ajustado
        FROM bus b
        JOIN registro_control r
            ON b.id_bus = r.id_bus
        WHERE r.retraso_minutos > 0
    """))

    datos = [dict(fila._mapping) for fila in resultado]

    db.close()

    return datos

@app.get("/reportes/empresas")
def reporte_empresas():

    db = SessionLocal()

    resultado = db.execute(text("""
        SELECT
            e.nombre AS empresa,
            COUNT(i.id_incidencia) AS total_incidencias,
            AVG(rc.retraso_minutos) AS promedio_retraso
        FROM empresa_transporte e
        JOIN bus b
            ON e.id_empresa = b.id_empresa
        JOIN incidencia i
            ON b.id_bus = i.id_bus
        JOIN registro_control rc
            ON b.id_bus = rc.id_bus
        GROUP BY e.nombre
        HAVING COUNT(i.id_incidencia) >= 1
        ORDER BY total_incidencias DESC
    """))

    datos = [dict(fila._mapping) for fila in resultado]

    db.close()

    return datos