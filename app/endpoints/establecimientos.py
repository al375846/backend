from fastapi.routing import APIRouter
from app.db.db import db
from app.models.establecimiento import Establecimiento, EstablecimientoDB


router = APIRouter()


@router.post("/alta_establecimiento")
async def crear_establecimiento(establecimiento: Establecimiento):
    establecimiento = EstablecimientoDB(**establecimiento.dict())

    await db.save(establecimiento)
    return establecimiento

"""
@router.delete("/establecimiento/{identificador}")
async def borrar_establecimiento(
    

):
    await db.delete(establecimiento.identificador)
    """