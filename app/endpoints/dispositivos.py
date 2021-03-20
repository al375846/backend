from fastapi.routing import APIRouter
from app.models.dispositivo import DispositivoCreate, DispositivoDB
from app.db.db import db


router = APIRouter()


@router.post("/dispositivo")
async def post_dispositivo(dispositivo: DispositivoCreate):
    disp = DispositivoDB(**dispositivo.dict())
    await db.motor.save(disp)
    return disp
