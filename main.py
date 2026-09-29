# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class Empleado(BaseModel):
#     empleado_id: int
#     nombre: str
#     departamento: str
#     salario: int

# @app.get("/")
# def inicio():
#     return {"mensaje": "Bienvenido a Ferzan Business Hub"}

# @app.get("/empleados")
# def obtener_empleados():
#     empleados = [
#         {"empleado_id": 1, "nombre": "Juan", "departamento": "Ventas", "salario": 50000},
#         {"empleado_id": 2, "nombre": "Maria", "departamento": "Marketing", "salario": 60000},
#         {"empleado_id": 3, "nombre": "Pedro", "departamento": "Tecnologia", "salario": 70000},
#         {"empleado_id": 4, "nombre": "Ana", "departamento": "Recursos Humanos", "salario": 55000},
#         {"empleado_id": 5, "nombre": "Luis", "departamento": "Finanzas", "salario": 65000},
#     ]
#     return empleados

# @app.get("/empleados/{empleado_id}")
# def obtener_empleado(empleado_id: int):

#     empleados = [
#         {"empleado_id": 1, "nombre": "Juan", "departamento": "Ventas", "salario": 50000},
#         {"empleado_id": 2, "nombre": "Maria", "departamento": "Marketing", "salario": 60000},
#         {"empleado_id": 3, "nombre": "Pedro", "departamento": "Tecnologia", "salario": 70000},
#         {"empleado_id": 4, "nombre": "Ana", "departamento": "Recursos Humanos", "salario": 55000},
#         {"empleado_id": 5, "nombre": "Luis", "departamento": "Finanzas", "salario": 65000},
#     ]

#     for empleado in empleados:
#         if empleado["empleado_id"] == empleado_id:
#             return empleado

#     return {"mensaje": "Empleado no encontrado"}


# @app.post("/empleados")
# def crear_empleado(empleado: Empleado):

#     return {
#         "mensaje": "Empleado creado correctamente",
#         "empleado": empleado
#     }

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg


app = FastAPI()

class Empleado(BaseModel):
    nombre: str
    departamento: str
    salario: int

class EmpleadoRespuesta(BaseModel):
    empleado_id: int
    nombre: str
    departamento: str
    salario: float

class EmpleadoCrear(BaseModel):
    nombre: str
    departamento: str
    salario: float

def obtener_conexion():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ferzan_db",
        user="ferzan_user",
        password="ferzan_password"
    )


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Ferzan Business Hub"
    }


@app.get("/empleados", response_model=list[EmpleadoRespuesta])
def obtener_empleados():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT empleado_id, nombre, departamento, salario
        FROM empleados
    """)

    empleados = cursor.fetchall()

    cursor.close()
    conexion.close()

    resultado = []

    for empleado in empleados:
        resultado.append({
            "empleado_id": empleado[0],
            "nombre": empleado[1],
            "departamento": empleado[2],
            "salario": empleado[3]
        })

    return resultado

@app.get("/empleados/{empleado_id}", response_model=EmpleadoRespuesta)
def obtener_empleado(empleado_id: int):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT empleado_id, nombre, departamento, salario
        FROM empleados
        WHERE empleado_id = %s
        """,
        (empleado_id,)
    )

    empleado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if empleado is None:
        raise HTTPException(
            status_code=404,
            detail="Empleado no encontrado"
        )

    return {
        "empleado_id": empleado[0],
        "nombre": empleado[1],
        "departamento": empleado[2],
        "salario": empleado[3]
    }

@app.post("/empleados")
def crear_empleado(empleado: EmpleadoCrear):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO empleados (nombre, departamento, salario)
        VALUES (%s, %s, %s)
        RETURNING empleado_id, nombre, departamento, salario
        """,
        (
            empleado.nombre,
            empleado.departamento,
            empleado.salario
        )
    )

    nuevo_empleado = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "empleado_id": nuevo_empleado[0],
        "nombre": nuevo_empleado[1],
        "departamento": nuevo_empleado[2],
        "salario": nuevo_empleado[3]
    }
    
@app.put("/empleados/{empleado_id}", response_model=EmpleadoRespuesta)
def actualizar_empleado(empleado_id: int, empleado: EmpleadoCrear):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE empleados
        SET nombre = %s,
            departamento = %s,
            salario = %s
        WHERE empleado_id = %s
        RETURNING empleado_id, nombre, departamento, salario
        """,
        (
            empleado.nombre,
            empleado.departamento,
            empleado.salario,
            empleado_id
        )
    )

    empleado_actualizado = cursor.fetchone()

    if empleado_actualizado is None:
        cursor.close()
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Empleado no encontrado"
        )

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "empleado_id": empleado_actualizado[0],
        "nombre": empleado_actualizado[1],
        "departamento": empleado_actualizado[2],
        "salario": empleado_actualizado[3]
    }
    

@app.delete("/empleados/{empleado_id}")
def eliminar_empleado(empleado_id: int):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM empleados
        WHERE empleado_id = %s
        RETURNING empleado_id
        """,
        (empleado_id,)
    )

    empleado_eliminado = cursor.fetchone()

    if empleado_eliminado is None:
        cursor.close()
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Empleado no encontrado"
        )

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "mensaje": "Empleado eliminado correctamente",
        "empleado_id": empleado_eliminado[0]
    }
    
@app.get("/health")
def health_check():
        return {
        "status": "ok",
        "service": "Ferzan Business Hub API"
    }