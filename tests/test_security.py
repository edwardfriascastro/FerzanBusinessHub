
from app.security import (
    crear_hash,
    verificar_password,
    crear_token_acceso,
    verificar_token,
)


def test_crear_hash_y_verificar_password():
    # Arrange: preparamos una contraseña
    password = "MiPasswordSegura123"
    password_hash = crear_hash(password)

    # Assert: el hash no debe ser la contraseña original
    assert password_hash != password

    # Assert: la contraseña correcta debe verificarse
    assert verificar_password(password, password_hash) is True

    # Assert: una contraseña incorrecta debe rechazarse
    assert verificar_password("PasswordIncorrecta", password_hash) is False



def test_crear_token_acceso(monkeypatch):
    # Configuramos una clave exclusiva para esta prueba.
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "clave-exclusiva-para-pruebas-automatizadas"
    )

    token = crear_token_acceso(1)

    assert isinstance(token, str)
    assert len(token) > 0


def test_verificar_token_valido(monkeypatch):
    # Usamos una clave exclusiva para esta prueba.
    # No utilizamos ni modificamos la clave real del proyecto.
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "clave-exclusiva-para-pruebas-automatizadas"
    )

    token = crear_token_acceso(1)
    payload = verificar_token(token)

    assert payload is not None
    assert payload["sub"] == "1"
    assert "exp" in payload


def test_verificar_token_alterado(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "clave-exclusiva-para-pruebas-automatizadas"
    )

    token = crear_token_acceso(1)
    token_alterado = token[:-1] + (
        "A" if token[-1] != "A" else "B"
    )

    payload = verificar_token(token_alterado)

    assert payload is None
