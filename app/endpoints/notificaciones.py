from app.models.notificacion import Notificacion
from odmantic import ObjectId
from app.db.db import db

from fastapi import APIRouter

router = APIRouter(prefix="/notificaciones",
                   tags=["notificaciones"])


@router.get("/notify")
async def push(id:ObjectId):
    notification = await db.motor.find_one(Notificacion,Notificacion.id == id)
    print(f"Enviando push notification FAKE\n{notification}")