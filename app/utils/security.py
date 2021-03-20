import jwt
from bson import ObjectId
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from odmantic import Model

from app.config import JWT_SECRET
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt

from app.db.db import db
from app.models.administrador import Administrador
from app.models.gerente import Gerente

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/security/token')
#oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl='/security/token_admin')


def verify_pwd(password, hashed_password):
    return bcrypt.verify(password, hashed_password)


async def get_current_gerente(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

        gerente = await db.motor.find_one(Gerente, Gerente.id == ObjectId(payload.get("id")))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario o contraseña incorrectos'
        )
    if gerente is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario o contraseña incorrectos'
        )

    return gerente


def generate_token(obj: Model):
    token = jwt.encode({"id": str(obj.id)}, JWT_SECRET)

    return token


def encripta_pwd(pwd: str):
    return bcrypt.hash(pwd)


async def authenticate_admin(email: str, password: str):
    admin = await db.motor.find_one(Administrador, Administrador.email == email)
    if not admin:
        return False
    if not verify_pwd(password, admin.password):
        return False
    return admin


async def authenticate_gerente(email: str, password: str):
    gerente = await db.motor.find_one(Gerente, Gerente.email == email)
    if not gerente:
        return False
    if not verify_pwd(password, gerente.password):
        return False
    return gerente


async def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        admin = await db.motor.find_one(Administrador, Administrador.id == ObjectId(payload.get("id")))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario o contraseña incorrectos'
        )
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario o contraseña incorrectos'
        )

    return admin
