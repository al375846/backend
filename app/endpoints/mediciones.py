from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from starlette import status

from app.db.db import db
from app.models.medicion import Medicion
from app.models.establecimiento import EstablecimientoDB
from app.models.gerente import Gerente
from app.utils.security import get_current_gerente
from typing import List
from datetime import datetime

router = APIRouter(prefix="/medicion",
                   tags=["Mediciones"])

router.get("/aforo/{establecimiento_id}")
async def obtener_medicion_aforo(gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    if establecimiento is None:
        raise HTTPException(detail="Ese establecimiento no existe", status_code=status.HTTP_404_NOT_FOUND)
    mediciones = establecimiento.mediciones
    if mediciones is None:
        ultima=mediciones[-1]
        return ultima
    else:
        medicion = Medicion(identificador="AFORO", fecha=datetime.now(), contenido="0")
        return medicion

