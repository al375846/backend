from fastapi import Depends
from fastapi.routing import APIRouter
from app.db.db import db
from app.models.establecimiento import Establecimiento, EstablecimientoDB
from app.models.gerente import Gerente
from app.utils.security import get_current_gerente

router = APIRouter()


@router.post("/alta_establecimiento")
async def crear_establecimiento(establecimiento: Establecimiento,gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = EstablecimientoDB(**establecimiento.dict())

    await db.motor.save(establecimiento)
    return establecimiento

"""
@router.delete("/establecimiento/{identificador}")
async def borrar_establecimiento(
    

):
    await db.delete(establecimiento.identificador)
    """