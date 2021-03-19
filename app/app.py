
from typing import List, Optional
from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from fastapi.security import OAuth2PasswordBearer

from app.db.db import db
from app.models.gerente import Gerente, RegistroGerente
from app.endpoints.dispositivos import router as router_dispositivos
from app.endpoints.establecimientos import router as router_establecimientos
app = FastAPI()

app.include_router(router_dispositivos)

app.include_router(router_establecimientos)

