from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from app.db.db import db
from app.models.establecimiento import Establecimiento, EstablecimientoDB
from app.models.gerente import Gerente
from app.utils.security import get_current_gerente
from app.models.dispositivo import DispositivoDB
from bson import ObjectId
from starlette import status

router = APIRouter()


@router.post("/establecimiento/alta")
async def crear_establecimiento(establecimiento: Establecimiento, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento_db = EstablecimientoDB(**establecimiento.dict(), gerente=gerente)
    await db.motor.save(establecimiento_db)
    return establecimiento_db


@router.delete("/establecimiento/baja/{id}")
async def borrar_establecimiento(id: str, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento_db = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(id))
    if establecimiento_db is None:
        raise HTTPException(detail="No existe", status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(establecimiento_db)
    return establecimiento_db


@router.put("/{establecimiento_id}/dispositivo/{dispositivo_id}")
async def asignar_dispositivo(establecimiento_id:str, dispositivo_id:str, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    if establecimiento.id != gerente.id:
        raise HTTPException(detail="Ese establecimiento no pertenece al gerente actual", status_code=status.HTTP_409_CONFLICT)
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    disp.establecimiento = establecimiento_id
    await db.motor.save(disp)
    return disp
