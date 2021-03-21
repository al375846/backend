from fastapi.routing import APIRouter
from app.models.dispositivo import DispositivoCreate, DispositivoDB
from app.db.db import db
from bson import ObjectId

router = APIRouter(prefix="/dispositivo", tags=["Dispositivos"])


@router.post("")
async def add_dispositivo(dispositivo: DispositivoCreate):
    disp = DispositivoDB(**dispositivo.dict())
    await db.motor.save(disp)
    return disp

@router.get("/{dispositivo_id}")
async def retrieve_dispositivo(dispositivo_id):
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    return disp

@router.put("/{dispositivo_id}/activar")
async def activate_dispositivo(dispositivo_id, activado:bool):
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    disp.activado = activado
    await db.motor.save(disp)
    return disp

@router.put("/{dispositivo_id}/conectar")
async def connect_dispositivo(dispositivo_id, conectado:bool):
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    disp.conectado = conectado
    await db.motor.save(disp)
    return disp
