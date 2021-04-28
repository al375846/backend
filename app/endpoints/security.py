from app.models.generic_respones import BasicReturn
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.enums.user_type import UserType
from app.models.administrador import Administrador
from app.models.gerente import Gerente
from app.models.registro import LoginReturn
from app.models.user_data import LoginData
from app.utils.security import authenticate_admin, generate_token, authenticate_gerente, get_current_gerente, \
    get_current_admin
from app.db.db import db

router = APIRouter(prefix="/security",
                   tags=["Security"])


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
        if login_data.phone_token not in gerente.phone_tokens:
            gerente.phone_tokens.append(login_data.phone_token)
        await db.motor.save(gerente)

    return lrt


@router.post("/logout", response_model=BasicReturn)
async def logout(phone_token:str, gerente:Gerente = Depends(get_current_gerente)):
    if phone_token in gerente.phone_tokens:
        gerente.phone_tokens.remove(phone_token)
        await db.motor.save(gerente)
    return BasicReturn()
        



