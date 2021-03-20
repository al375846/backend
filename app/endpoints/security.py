from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

from app.db.db import db
from app.enums import user_type
from app.enums.user_type import UserType
from app.models.administrador import Administrador
from app.models.gerente import Gerente
from app.models.registro import Registro, LoginReturn
from app.models.user_data import UserData, LoginData
from app.utils.security import authenticate_admin, generate_token, authenticate_gerente, encripta_pwd, \
    get_current_gerente, get_current_admin

router = APIRouter(prefix="/security",
                   tags=["Security"])


@router.post("/registra_gerente", response_model=Gerente)
async def index(gerente: Registro):
    await check_unique_email(gerente)
    gerente.password = encripta_pwd(gerente.password)
    gdb = Gerente(**gerente.dict())
    await db.motor.save(gdb)
    return gdb


@router.post("/registra_administrador", response_model=Administrador)
async def index(admin: Registro, _=Depends(get_current_admin)):
    await check_unique_email(admin)
    admin.password = encripta_pwd(admin.password)
    gdb = Administrador(**admin.dict())
    await db.motor.save(gdb)
    return gdb


@router.delete("/baja_gerente", response_model=UserData)
async def baja_gerente(email_baja: EmailStr, _=Depends(get_current_admin)):
    gerente = await db.motor.find_one(Gerente, Gerente.email == email_baja)
    if gerente is None:
        raise HTTPException(detail="Usuario no existe", status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(gerente)
    return gerente


@router.delete("/baja_admin", response_model=UserData)
async def baja_admin(email_baja: EmailStr, _=Depends(get_current_admin)):
    admin = await db.motor.find_one(Administrador, Administrador.email == email_baja)
    if admin is None:
        raise HTTPException(detail="Usuario no existe", status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(admin)
    return admin


async def check_unique_email(user: Registro):
    n1 = len(await db.motor.find(Administrador, Administrador.email == user.email))
    n2 = len(await db.motor.find(Gerente, Gerente.email == user.email))
    if n1 + n2 > 0:
        raise HTTPException(detail="email repetido", status_code=status.HTTP_409_CONFLICT)


@router.get("/gerente/yo", response_model=Gerente)
async def index(gerente: Gerente = Depends(get_current_gerente)):
    return gerente


@router.get("/admin/yo", response_model=Administrador)
async def index(admin: Administrador = Depends(get_current_admin)):
    return admin


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = await authenticate_admin(form_data.username, form_data.password)
    gerente = await authenticate_gerente(form_data.username, form_data.password)
    if not admin and not gerente:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = None
    if admin:
        token = generate_token(admin)
    elif gerente:
        token = generate_token(gerente)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=LoginReturn)
async def login(login_data: LoginData):
    gerente = await authenticate_gerente(login_data.email, login_data.password)
    admin = await authenticate_admin(login_data.email, login_data.password)
    if not admin and not gerente:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    lrt = LoginReturn(access_token="", token_type="bearer", user_type=UserType.gerente)
    if admin:
        lrt.access_token = generate_token(admin)
        lrt.user_type = UserType.administrador
    elif gerente:
        lrt.access_token = generate_token(gerente)

    return lrt
