from app.models.configuracion_establecimiento import ConfiguracionEstablecimiento
from typing import List
from odmantic import ObjectId
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from starlette import status
from app.models.generic_respones import BasicReturn

from app.db.db import db
from app.models.dispositivo import DispositivoDB
from app.models.establecimiento import Establecimiento, EstablecimientoDB, EstablecimientoRet
from app.models.gerente import Gerente
from app.utils.security import get_current_gerente

router = APIRouter(prefix="/establecimiento",
                   tags=["Gestion establecimiento"])


@router.post("/alta", response_model=EstablecimientoRet)
async def crear_establecimiento(establecimiento_modelo: Establecimiento,
                                gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = EstablecimientoDB(
        **establecimiento_modelo.dict(), gerente=gerente)
    establecimientos = await db.motor.find(EstablecimientoDB, EstablecimientoDB.gerente == gerente.id)
    for otroEstablecimiento in establecimientos:
        if otroEstablecimiento.descriptor == establecimiento.descriptor:
            raise HTTPException(detail="descriptor repetido",
                                status_code=status.HTTP_409_CONFLICT)
    await db.motor.save(establecimiento)
    return establecimiento


@router.get("/get/{establecimiento_id}", response_model=EstablecimientoDB)
async def obtener_establecimiento(establecimiento_id: ObjectId,
                                  gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == establecimiento_id)
    valida(establecimiento=establecimiento, gerente_id=gerente.id)
    return establecimiento


@router.get("/get/{establecimiento_id}/dispositivos", response_model=List[DispositivoDB])
async def obtener_dispositivos_establecimiento(establecimiento_id: str,
                                               _=Depends(get_current_gerente)):
    dispositivos = await db.motor.find(DispositivoDB, DispositivoDB.establecimiento == establecimiento_id)
    return dispositivos


@router.get("/todos", response_model=List[EstablecimientoRet])
async def obtener_establecimientos(gerente: Gerente = Depends(get_current_gerente)):
    establecimientos = await db.motor.find(EstablecimientoDB, EstablecimientoDB.gerente == gerente.id)
    return establecimientos


@router.delete("/{establecimiento_id}/baja", response_model=EstablecimientoDB)
async def borrar_establecimiento(establecimiento_id: ObjectId, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == establecimiento_id)
    valida(establecimiento=establecimiento, gerente_id=gerente.id)
    await db.motor.delete(establecimiento)
    return establecimiento


@router.put("/{establecimiento_id}/cambio", response_model=EstablecimientoDB)
async def cambiar_establecimiento(establecimiento_id: ObjectId, config: ConfiguracionEstablecimiento, gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == establecimiento_id)
    valida(establecimiento=establecimiento, gerente_id=gerente.id)
    establecimiento.configuracion = config
    await db.motor.save(establecimiento)
    return establecimiento


@router.put("/{establecimiento_id}/dispositivo/{dispositivo_id}", response_model=DispositivoDB)
async def asignar_dispositivo(establecimiento_id: ObjectId, dispositivo_id: ObjectId,
                              gerente: Gerente = Depends(get_current_gerente)):

    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == dispositivo_id)
    if disp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no existe")
    if disp.establecimiento is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Dispositivo en uso")

    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == establecimiento_id)
    valida(establecimiento, gerente_id=gerente.id)
    disp.establecimiento = str(establecimiento_id)
    await db.motor.save(disp)
    return disp


@router.put("/desasigna_dispositivo/{dispositivo_id}", response_model=BasicReturn)
async def desasigna_dispositivo(dispositivo_id: ObjectId, gerente: Gerente = Depends(get_current_gerente)):

    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == dispositivo_id)
    if disp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no existe")
    if disp is None or disp.establecimiento is None:
        return BasicReturn(done=False)

    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == ObjectId(disp.establecimiento))
    valida(establecimiento, gerente_id=gerente.id)
    disp.establecimiento = None
    await db.motor.save(disp)
    return BasicReturn()


def valida(establecimiento, gerente_id):
    if establecimiento is None:
        raise HTTPException(detail="Ese establecimiento no existe",
                            status_code=status.HTTP_404_NOT_FOUND)
    if establecimiento.gerente.id != gerente_id:
        raise HTTPException(detail="Ese establecimiento no pertenece al gerente actual",
                            status_code=status.HTTP_409_CONFLICT)
