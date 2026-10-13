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

from fastapi import FastAPI, HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import psycopg
from dotenv import load_dotenv
import os

from app.schema import UsuarioCrear, UsuarioLogin
from app.security import crear_hash, verificar_password, crear_token_acceso,verificar_token

load_dotenv()

security = HTTPBearer()

app = FastAPI()


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security)
):
    token = credenciales.credentials

    payload = verificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    try:
        usuario_id = int(payload.get("sub", ""))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT usuario_id, nombre, email, activo, rol
            FROM usuarios
            WHERE usuario_id = %s
            """,
            (usuario_id,)
        )

        usuario_db = cursor.fetchone()

    finally:
        cursor.close()
        conexion.close()

    if usuario_db is None or not usuario_db[3]:
        raise HTTPException(
            status_code=401,
            detail="Usuario inexistente o cuenta inactiva"
        )

    return {
        "usuario_id": usuario_db[0],
        "nombre": usuario_db[1],
        "email": usuario_db[2],
        "activo": usuario_db[3],
        "rol": usuario_db[4]
    }
    

def exigir_rol(*roles_permitidos: str):
    def verificar_rol(
        usuario_actual=Depends(obtener_usuario_actual)
    ):
        if usuario_actual["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para realizar esta operación"
            )

        return usuario_actual

    return verificar_rol
    
@app.get("/me")
def obtener_mi_usuario(
    usuario_actual=Depends(obtener_usuario_actual)
):
    return {
        "mensaje": "Autenticación correcta",
        "usuario": usuario_actual
    }
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
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Ferzan Business Hub"
    }


@app.get("/empleados", response_model=list[EmpleadoRespuesta])
def obtener_empleados(
    departamento: str | None = None,
    usuario_actual=Depends(obtener_usuario_actual),
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if departamento is not None:
        # Buscar por departamento
        cursor.execute(
            """
            SELECT empleado_id, nombre, departamento, salario
            FROM empleados
            WHERE departamento = %s
            """,
            (departamento,)
        )
    else:
        # Traer todos los empleados
        cursor.execute(
            """
            SELECT empleado_id, nombre, departamento, salario
            FROM empleados
            """
        )

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
def obtener_empleado(
    empleado_id: int,
    usuario_actual=Depends(obtener_usuario_actual)
):
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
def crear_empleado(
    empleado: EmpleadoCrear,
    usuario_actual=Depends(exigir_rol("admin"))
):
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
def actualizar_empleado(empleado_id: int, empleado: EmpleadoCrear,
    usuario_actual=Depends(exigir_rol("admin"))
):


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
def eliminar_empleado(empleado_id: int, usuario_actual=Depends(exigir_rol("admin"))):

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
        
@app.post("/register")
def registrar_usuario(usuario: UsuarioCrear):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    password_hash = crear_hash(usuario.password)

    cursor.execute(
        """
        INSERT INTO usuarios (nombre, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING usuario_id, nombre, email
        """,
        (
            usuario.nombre,
            usuario.email,
            password_hash
        )
    )

    nuevo_usuario = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "usuario_id": nuevo_usuario[0],
        "nombre": nuevo_usuario[1],
        "email": nuevo_usuario[2]
    }
    
@app.post("/login")
def iniciar_sesion(usuario: UsuarioLogin):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT usuario_id, nombre, email, password_hash
        FROM usuarios
        WHERE email = %s
        """,
        (usuario.email,)
    )

    usuario_db = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario_db is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    password_correcta = verificar_password(
        usuario.password,
        usuario_db[3]
    )

    if not password_correcta:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = crear_token_acceso(usuario_db[0])

    return {
        "access_token": token,
        "token_type": "bearer"
    }