from app.enums.medicion import TipoMedicion
from odmantic import ObjectId, query
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from starlette import status

from app.db.db import db
from app.models.medicion import Medicion, InformeMedicionRet, MedicionRet
from app.models.establecimiento import EstablecimientoDB
from app.models.gerente import Gerente
from app.utils.security import get_current_gerente
from typing import List
from datetime import datetime

router = APIRouter(prefix="/medicion",
                   tags=["Mediciones"])


@router.get("/aforo/{establecimiento_id}",response_model=MedicionRet)
async def obtener_medicion_aforo(establecimiento_id: ObjectId, gerente: Gerente = Depends(get_current_gerente)):

    establecimiento = await db.motor.find_one(EstablecimientoDB, EstablecimientoDB.id == establecimiento_id)
    if establecimiento is None:
        raise HTTPException(detail="Ese establecimiento no existe",
                            status_code=status.HTTP_404_NOT_FOUND)
    if establecimiento.mediciones is None:
        return MedicionRet()
    else:
        ultima = filtra_fecha(establecimiento.mediciones,TipoMedicion.aforo)[-1].contenido
        return MedicionRet(contenido = ultima)


@router.get("/informe/aforo/{establecimiento_id}",response_model=InformeMedicionRet)
async def obtener_mediciones_aforo(*, establecimiento_id: ObjectId, fecha_ini: datetime = None, fecha_fin: datetime = None,
                                   gerente: Gerente = Depends(get_current_gerente)):
    establecimiento = await db.motor.find_one(EstablecimientoDB,query.and_(EstablecimientoDB.gerente == gerente.id,EstablecimientoDB.id == establecimiento_id))
    
    if establecimiento is None:
        raise HTTPException(detail="Ese establecimiento no existe",
                            status_code=status.HTTP_404_NOT_FOUND)
    if establecimiento.mediciones is None:
        return InformeMedicionRet()
    else:
        mediciones = establecimiento.mediciones
        mediciones = filtra_fecha(mediciones,TipoMedicion.aforo,fecha_ini,fecha_fin)
        return InformeMedicionRet(contenido= mediciones)


def filtra_fecha(mediciones: Medicion, tipo: TipoMedicion, fecha_ini: datetime = None, fecha_fin: datetime = None):
    
    return list(filter(lambda medicion:medicion.tipo_medicion == tipo and (fecha_fin is None or medicion.fecha <= fecha_fin)
                and (fecha_ini is None or medicion.fecha >= fecha_ini),mediciones))
