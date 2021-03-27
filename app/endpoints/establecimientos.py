from typing import List
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from starlette import status

from app.db.db import db
from app.models.dispositivo import DispositivoDB
from app.models.establecimiento import Establecimiento, EstablecimientoDB
from app.models.gerente import Gerente
from app.utils.security import get_current_gerente

router = APIRouter(prefix="/establecimiento",
                   tags=["Gestion establecimiento"])


@router.post("/alta")
async def crear_establecimiento(establecimiento_modelo: Establecimiento,
                                gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = EstablecimientoDB(**establecimiento_modelo.dict(), gerente=gerente)
    await db.motor.save(establecimiento)
    return establecimiento


@router.get("/get/{establecimiento_id}")
async def obtener_establecimiento(establecimiento_id: str,
                                gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    valida(establecimiento=establecimiento, gerente_id=gerente.id)
    return establecimiento


@router.get("/todos",response_model=List[Establecimiento])
async def obtener_establecimientos(gerente: Gerente = Depends(get_current_gerente)):
    establecimientos = await db.motor.find(EstablecimientoDB, EstablecimientoDB.gerente == gerente.id)
    return establecimientos


@router.post("/{id}")
async def obtener_establecimiento(establecimiento_modelo: Establecimiento,
                                  gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = EstablecimientoDB(**establecimiento_modelo.dict(), gerente=gerente)
    await db.motor.save(establecimiento)
    return establecimiento


@router.delete("/{establecimiento_id}/baja")
async def borrar_establecimiento(establecimiento_id: str, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    valida(establecimiento=establecimiento, gerente_id=gerente.id)
    await db.motor.delete(establecimiento)
    return establecimiento


@router.put("/{establecimiento_id}/cambio/{aforo}")
async def cambiar_establecimiento(establecimiento_id: str, aforo: int, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    valida(establecimiento=establecimiento, gerente_id=gerente.id)
    establecimiento.aforo = aforo
    await db.motor.save(establecimiento)
    return establecimiento


@router.put("/{establecimiento_id}/dispositivo/{dispositivo_id}")
async def asignar_dispositivo(establecimiento_id: str, dispositivo_id: str,
                              gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(establecimiento_id))
    valida(establecimiento, gerente_id=gerente.id)
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    disp.establecimiento = establecimiento_id
    await db.motor.save(disp)
    return disp


def valida(establecimiento, gerente_id):
    if establecimiento is None:
        raise HTTPException(detail="Ese establecimiento no existe", status_code=status.HTTP_404_NOT_FOUND)
    if establecimiento.gerente.id != gerente_id:
        raise HTTPException(detail="Ese establecimiento no pertenece al gerente actual",
                            status_code=status.HTTP_409_CONFLICT)
