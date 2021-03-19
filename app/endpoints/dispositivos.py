from fastapi.routing import APIRouter
from app.models.dispositivo import DispositivoCreate, DispositivoDB
from app.db.db import db
from datetime import datetime

router = APIRouter()

@router.post("/dispositivo")
async def post_dispositivo(dispositivo: DispositivoCreate):
    disp = DispositivoDB(
        fechaRegistro=datetime.now(),
        **dispositivo.dict()
    )
    await db.save(disp)
    return disp