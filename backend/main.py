from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Esto es para que Html corra sin errores CORS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Sistema de Transporte AQP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Activar entorno virtual ====
# cd D:\Programacion\SistemaTransportesAQP\backend
# .\venv\Scripts\Activate.ps1

# ==== Levantar FastAPI ====
# uvicorn main:app --reload

DATABASE_URL = "postgresql://postgres:AQPTransporte2026@localhost:5432/sistema_transporte_aqp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def rows_to_list(resultado):
    return [dict(fila._mapping) for fila in resultado]

# ─────────────────────────────────────────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/")
def inicio():
    return {"mensaje": "Sistema de Transporte AQP funcionando"}

# ═════════════════════════════════════════════════════════════════════════════
# BUSES
# ═════════════════════════════════════════════════════════════════════════════
class Bus(BaseModel):
    placa: str
    capacidad: int
    estado: str
    id_empresa: Optional[int] = None
    id_terminal: Optional[int] = None

@app.get("/buses")
def listar_buses():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM bus ORDER BY id_bus"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/buses/{id_bus}")
def obtener_bus(id_bus: int):
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM bus WHERE id_bus=:id"), {"id": id_bus})
    fila = resultado.fetchone()
    db.close()
    if not fila:
        raise HTTPException(status_code=404, detail="Bus no encontrado")
    return dict(fila._mapping)

@app.post("/buses")
def crear_bus(bus: Bus):
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO bus (placa, capacidad, estado, id_empresa, id_terminal)
            VALUES (:placa, :capacidad, :estado, :id_empresa, :id_terminal)
        """), bus.model_dump())
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Bus registrado"}

@app.put("/buses/{id_bus}")
def editar_bus(id_bus: int, bus: Bus):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            UPDATE bus SET placa=:placa, capacidad=:capacidad, estado=:estado,
            id_empresa=:id_empresa, id_terminal=:id_terminal
            WHERE id_bus=:id
        """), {**bus.model_dump(), "id": id_bus})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bus no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Bus actualizado"}

@app.delete("/buses/{id_bus}")
def eliminar_bus(id_bus: int):
    db = SessionLocal()
    try:
        result = db.execute(text("DELETE FROM bus WHERE id_bus=:id"), {"id": id_bus})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bus no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Bus eliminado"}

# ═════════════════════════════════════════════════════════════════════════════
# CONDUCTORES
# ═════════════════════════════════════════════════════════════════════════════
class Conductor(BaseModel):
    nombres: str
    licencia: str
    telefono: Optional[str] = None
    fecha_ingreso: str

@app.get("/conductores")
def listar_conductores():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM conductor ORDER BY id_conductor"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/conductores/{id_conductor}")
def obtener_conductor(id_conductor: int):
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM conductor WHERE id_conductor=:id"), {"id": id_conductor})
    fila = resultado.fetchone()
    db.close()
    if not fila:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return dict(fila._mapping)

@app.post("/conductores")
def crear_conductor(conductor: Conductor):
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO conductor (nombres, licencia, telefono, fecha_ingreso)
            VALUES (:nombres, :licencia, :telefono, :fecha_ingreso)
        """), conductor.model_dump())
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Conductor registrado"}


# ═════════════════════════════════════════════════════════════════════════════
# PASAJEROS
# ═════════════════════════════════════════════════════════════════════════════
class Pasajero(BaseModel):
    nombres: str
    correo: str
    telefono: str

@app.get("/pasajeros")
def listar_pasajeros():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM pasajero ORDER BY id_pasajero"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/pasajeros/{id_pasajero}")
def obtener_pasajero(id_pasajero: int):
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM pasajero WHERE id_pasajero=:id"), {"id": id_pasajero})
    fila = resultado.fetchone()
    db.close()
    if not fila:
        raise HTTPException(status_code=404, detail="Pasajero no encontrado")
    return dict(fila._mapping)

@app.post("/pasajeros")
def crear_pasajero(pasajero: Pasajero):
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO pasajero (nombres, correo, telefono)
            VALUES (:nombres, :correo, :telefono)
        """), pasajero.model_dump())
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Pasajero registrado"}

@app.put("/pasajeros/{id_pasajero}")
def editar_pasajero(id_pasajero: int, pasajero: Pasajero):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            UPDATE pasajero SET nombres=:nombres, correo=:correo, telefono=:telefono
            WHERE id_pasajero=:id
        """), {**pasajero.model_dump(), "id": id_pasajero})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pasajero no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Pasajero actualizado"}

@app.delete("/pasajeros/{id_pasajero}")
def eliminar_pasajero(id_pasajero: int):
    db = SessionLocal()
    try:
        result = db.execute(text("DELETE FROM pasajero WHERE id_pasajero=:id"), {"id": id_pasajero})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pasajero no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Pasajero eliminado"}

# ═════════════════════════════════════════════════════════════════════════════
# INCIDENCIAS
# ═════════════════════════════════════════════════════════════════════════════
class Incidencia(BaseModel):
    id_bus: int
    id_centro: int
    id_pasajero: int
    descripcion: str
    tipo: str

@app.get("/incidencias")
def listar_incidencias():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM incidencia ORDER BY id_incidencia"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/incidencias/{id_incidencia}")
def obtener_incidencia(id_incidencia: int):
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM incidencia WHERE id_incidencia=:id"), {"id": id_incidencia})
    fila = resultado.fetchone()
    db.close()
    if not fila:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return dict(fila._mapping)

@app.post("/incidencias")
def crear_incidencia(incidencia: Incidencia):
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO incidencia (id_bus, id_centro, id_pasajero, descripcion, tipo, fecha_reporte)
            VALUES (:id_bus, :id_centro, :id_pasajero, :descripcion, :tipo, NOW())
        """), incidencia.model_dump())
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Incidencia registrada"}

@app.put("/incidencias/{id_incidencia}")
def editar_incidencia(id_incidencia: int, incidencia: Incidencia):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            UPDATE incidencia SET id_bus=:id_bus, id_centro=:id_centro,
            id_pasajero=:id_pasajero, descripcion=:descripcion, tipo=:tipo
            WHERE id_incidencia=:id
        """), {**incidencia.model_dump(), "id": id_incidencia})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Incidencia actualizada"}

@app.delete("/incidencias/{id_incidencia}")
def eliminar_incidencia(id_incidencia: int):
    db = SessionLocal()
    try:
        result = db.execute(text("DELETE FROM incidencia WHERE id_incidencia=:id"), {"id": id_incidencia})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Incidencia eliminada"}

# ═════════════════════════════════════════════════════════════════════════════
# EMPRESAS
# ═════════════════════════════════════════════════════════════════════════════
class Empresa(BaseModel):
    nombre: str
    ruc: str
    telefono: Optional[str] = None
    correo: Optional[str] = None

@app.get("/empresas")
def listar_empresas():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM empresa_transporte ORDER BY id_empresa"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/empresas/{id_empresa}")
def obtener_empresa(id_empresa: int):
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM empresa_transporte WHERE id_empresa=:id"), {"id": id_empresa})
    fila = resultado.fetchone()
    db.close()
    if not fila:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return dict(fila._mapping)

@app.post("/empresas")
def crear_empresa(empresa: Empresa):
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO empresa_transporte (nombre, ruc, telefono, correo)
            VALUES (:nombre, :ruc, :telefono, :correo)
        """), empresa.model_dump())
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Empresa registrada"}

@app.put("/empresas/{id_empresa}")
def editar_empresa(id_empresa: int, empresa: Empresa):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            UPDATE empresa_transporte SET nombre=:nombre, ruc=:ruc,
            telefono=:telefono, correo=:correo WHERE id_empresa=:id
        """), {**empresa.model_dump(), "id": id_empresa})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Empresa actualizada"}

@app.delete("/empresas/{id_empresa}")
def eliminar_empresa(id_empresa: int):
    db = SessionLocal()
    try:
        result = db.execute(text("DELETE FROM empresa_transporte WHERE id_empresa=:id"), {"id": id_empresa})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return {"mensaje": "Empresa eliminada"}

# ═════════════════════════════════════════════════════════════════════════════
# SOLO LECTURA
# ═════════════════════════════════════════════════════════════════════════════
@app.get("/rutas")
def listar_rutas():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM ruta ORDER BY id_ruta"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/terminales")
def listar_terminales():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM terminal ORDER BY id_terminal"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/horarios")
def listar_horarios():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM horario ORDER BY id_horario"))
    datos = rows_to_list(resultado)
    db.close()
    return [{"id_horario": r["id_horario"], "hora_salida": str(r["hora_salida"]),
             "hora_llegada": str(r["hora_llegada"]), "id_ruta": r["id_ruta"]} for r in datos]

@app.get("/paraderos")
def listar_paraderos():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM paradero ORDER BY id_paradero"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/notificaciones")
def listar_notificaciones():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM notificacion ORDER BY id_notificacion"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

@app.get("/registro-control")
def listar_registro_control():
    db = SessionLocal()
    resultado = db.execute(text("SELECT * FROM registro_control ORDER BY id_registro"))
    datos = rows_to_list(resultado)
    db.close()
    return datos

# ═════════════════════════════════════════════════════════════════════════════
# REPORTES — GROUP BY / HAVING / JOIN 3+ tablas
# ═════════════════════════════════════════════════════════════════════════════

# Reporte 1: conductor + asignacion_conductor + bus
@app.get("/reportes/conductores")
def reporte_conductores():
    db = SessionLocal()
    resultado = db.execute(text("""
        SELECT
            c.nombres AS nombre_conductor,
            c.licencia,
            b.placa AS bus_asignado,
            COUNT(ac.id_asignacion) AS total_asignaciones
        FROM conductor c
        JOIN asignacion_conductor ac ON c.id_conductor = ac.id_conductor
        JOIN bus b ON ac.id_bus = b.id_bus
        GROUP BY c.nombres, c.licencia, b.placa
        HAVING COUNT(ac.id_asignacion) >= 1
        ORDER BY total_asignaciones DESC
    """))
    datos = rows_to_list(resultado)
    db.close()
    return datos

# Reporte 2: incidencia + bus + empresa_transporte
@app.get("/reportes/incidencias")
def reporte_incidencias():
    db = SessionLocal()
    resultado = db.execute(text("""
        SELECT
            i.tipo AS tipo_incidencia,
            e.nombre AS empresa,
            COUNT(i.id_incidencia) AS total_reportes
        FROM incidencia i
        JOIN bus b ON i.id_bus = b.id_bus
        JOIN empresa_transporte e ON b.id_empresa = e.id_empresa
        GROUP BY i.tipo, e.nombre
        HAVING COUNT(i.id_incidencia) >= 1
        ORDER BY total_reportes DESC
    """))
    datos = rows_to_list(resultado)
    db.close()
    return datos

# Reporte 3: bus + registro_control + empresa_transporte
@app.get("/reportes/retrasos")
def reporte_retrasos():
    db = SessionLocal()
    resultado = db.execute(text("""
        SELECT
            b.placa AS placa_bus,
            e.nombre AS empresa,
            r.retraso_minutos AS retraso_original,
            r.retraso_minutos + 10 AS retraso_ajustado,
            r.observacion
        FROM bus b
        JOIN registro_control r ON b.id_bus = r.id_bus
        JOIN empresa_transporte e ON b.id_empresa = e.id_empresa
        WHERE r.retraso_minutos > 0
        ORDER BY r.retraso_minutos DESC
    """))
    datos = rows_to_list(resultado)
    db.close()
    return datos

# Reporte 4: empresa_transporte + bus + incidencia + registro_control
@app.get("/reportes/empresas")
def reporte_empresas():
    db = SessionLocal()
    resultado = db.execute(text("""
        SELECT
            e.nombre AS empresa,
            COUNT(DISTINCT i.id_incidencia) AS total_incidencias,
            ROUND(AVG(rc.retraso_minutos)::numeric, 2) AS promedio_retraso_min
        FROM empresa_transporte e
        JOIN bus b ON e.id_empresa = b.id_empresa
        JOIN incidencia i ON b.id_bus = i.id_bus
        JOIN registro_control rc ON b.id_bus = rc.id_bus
        GROUP BY e.nombre
        HAVING COUNT(DISTINCT i.id_incidencia) >= 1
        ORDER BY total_incidencias DESC
    """))
    datos = rows_to_list(resultado)
    db.close()
    return datos
