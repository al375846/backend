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
async def obtener_medicion_aforo():
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    mediciones = establecimiento.mediciones
    if (mediciones):
        mediciones.sort(key=mediciones.fecha, reverse=True)
        ultima=mediciones[0]
        return ultima
    else:
        medicion = Medicion(identificador="", fecha=datetime.now(), contenido="No hay medicion de aforo")
        return medicion

