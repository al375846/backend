from odmantic import ObjectId
from fastapi import APIRouter, Depends

from app.db.db import db
from app.models.dispositivo import DispositivoCreate, DispositivoDB, DispositivoRet
from app.utils.security import get_current_gerente

router = APIRouter(prefix="/dispositivo", tags=["Dispositivos"])


@router.post("",response_model=DispositivoRet)
async def add_dispositivo(dispositivo: DispositivoCreate):
    disp = DispositivoDB(id = ObjectId(),**dispositivo.dict())
    await db.motor.save(disp)
    return {"id":str(disp.id)}


@router.get("/{dispositivo_id}")
async def retrieve_dispositivo(dispositivo_id: str, _=Depends(get_current_gerente)):
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    return disp


@router.put("/{dispositivo_id}/activar")
async def activate_dispositivo(dispositivo_id: str, activado: bool, _=Depends(get_current_gerente)):
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    disp.activado = activado
    await db.motor.save(disp)
    return disp


@router.put("/{dispositivo_id}/conectar")
async def connect_dispositivo(dispositivo_id: str, conectado: bool, _=Depends(get_current_gerente)):
    disp = await db.motor.find_one(DispositivoDB, DispositivoDB.id == ObjectId(dispositivo_id))
    disp.conectado = conectado
    await db.motor.save(disp)
    return disp
