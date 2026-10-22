
from fastapi.testclient import TestClient
import pytest
from fastapi import HTTPException

from main import (
    app,
    obtener_usuario_actual,
    verificar_rol_permitido,
)
client = TestClient(app)


def test_empleados_sin_token_retorna_401():
    response = client.get("/empleados")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_empleado_normal_no_puede_crear_empleados():
    usuario_empleado = {
        "usuario_id": 10,
        "nombre": "Empleado de prueba",
        "email": "empleado@prueba.local",
        "activo": True,
        "rol": "empleado",
    }

    app.dependency_overrides[obtener_usuario_actual] = (
        lambda: usuario_empleado
    )

    try:
        response = client.post(
            "/empleados",
            json={
                "nombre": "Empleado ficticio",
                "departamento": "Pruebas",
                "salario": 50000,
            },
        )

        assert response.status_code == 403
        assert response.json()["detail"] == (
            "No tienes permisos para realizar esta operación"
        )

    finally:
        app.dependency_overrides.clear()


def test_empleado_normal_no_puede_actualizar_empleados():
    usuario_empleado = {
        "usuario_id": 10,
        "nombre": "Empleado de prueba",
        "email": "empleado@prueba.local",
        "activo": True,
        "rol": "empleado",
    }

    app.dependency_overrides[obtener_usuario_actual] = (
        lambda: usuario_empleado
    )

    try:
        response = client.put(
            "/empleados/1",
            json={
                "nombre": "Nombre modificado",
                "departamento": "Pruebas",
                "salario": 50000,
            },
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides.clear()


def test_empleado_normal_no_puede_eliminar_empleados():
    usuario_empleado = {
        "usuario_id": 10,
        "nombre": "Empleado de prueba",
        "email": "empleado@prueba.local",
        "activo": True,
        "rol": "empleado",
    }

    app.dependency_overrides[obtener_usuario_actual] = (
        lambda: usuario_empleado
    )

    try:
        response = client.delete("/empleados/1")

        assert response.status_code == 403

    finally:
        app.dependency_overrides.clear()


from main import exigir_rol

def test_administrador_tiene_permiso():
    usuario_admin = {
        "usuario_id": 1,
        "nombre": "Administrador de prueba",
        "email": "admin@prueba.local",
        "activo": True,
        "rol": "admin",
    }

    resultado = verificar_rol_permitido(
        usuario_admin,
        ("admin",),
    )

    assert resultado == usuario_admin
    assert resultado["rol"] == "admin"


def test_empleado_normal_no_tiene_permiso_admin():
    usuario_empleado = {
        "usuario_id": 10,
        "nombre": "Empleado de prueba",
        "email": "empleado@prueba.local",
        "activo": True,
        "rol": "empleado",
    }

    with pytest.raises(HTTPException) as error:
        verificar_rol_permitido(
            usuario_empleado,
            ("admin",),
        )

    assert error.value.status_code == 403
    assert error.value.detail == (
        "No tienes permisos para realizar esta operación"
    )
