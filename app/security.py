
import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


password_hash = PasswordHash.recommended()
security = HTTPBearer()


def crear_hash(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(
    password: str,
    password_hash_guardado: str
) -> bool:
    return password_hash.verify(password, password_hash_guardado)


def obtener_clave_jwt() -> str:
    clave = os.getenv("JWT_SECRET_KEY")

    if not clave:
        raise RuntimeError(
            "La variable de entorno JWT_SECRET_KEY no está configurada"
        )

    return clave


def crear_token_acceso(usuario_id: int) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": str(usuario_id),
        "exp": expiracion
    }

    token = jwt.encode(
        payload,
        obtener_clave_jwt(),
        algorithm="HS256"
    )

    return token


def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            obtener_clave_jwt(),
            algorithms=["HS256"]
        )

        return payload

    except jwt.InvalidTokenError:
        return None


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

    return payload


if __name__ == "__main__":
    resultado = crear_hash("123456")

    print("Hash:", resultado)
    print(
        "Contraseña correcta:",
        verificar_password("123456", resultado)
    )
    print(
        "Contraseña incorrecta:",
        verificar_password("999999", resultado)
    )

    token = crear_token_acceso(1)
    print("Token:", token)

    payload = verificar_token(token)
    print("Payload:", payload)
