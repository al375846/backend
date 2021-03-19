from fastapi.routing import APIRouter
from app.models.dispositivo import DispositivoCreate, DispositivoDB
from app.db.db import db
from datetime import datetime

router = APIRouter()

@router.post("/dispositivo")
async def post_dispositivo(dispositivo: DispositivoCreate):
    disp = DispositivoDB(
        modelo=dispositivo.modelo,
        fechaRegistro=datetime.now(),
        activado=dispositivo.activado,
        conectado=dispositivo.conectado,
        tipo=dispositivo.tipo
    )
    await db.save(disp)
    return disp