from app.enums.medicion import TipoMedicion
from collections import defaultdict
from odmantic import ObjectId, query
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from starlette import status
import math

from app.db.db import db
from app.models.medicion import MediaAforo, Medicion, InformeMedicionRet, MedicionEstablecimiento, MedicionRet
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


@router.get("/informe/diario",response_model=List[MedicionEstablecimiento])
async def obtener_mediciones(*, gerente: Gerente = Depends(get_current_gerente)):
    establecimientos = await db.motor.find(EstablecimientoDB,EstablecimientoDB.gerente == gerente.id)
    
    res = []
    for establecimiento in establecimientos:
        if len(establecimiento.mediciones)> 0:
            mediciones_aforo = filtra_dia(establecimiento.mediciones,TipoMedicion.aforo)
            mediciones_aforo = media_mediciones_aforo(mediciones_aforo)
            est = MedicionEstablecimiento(descriptor = establecimiento.descriptor,
                                        aforo_value = mediciones_aforo[-1].media,
                                        medias_aforo = mediciones_aforo)
            res.append(est)
    return res

def media_mediciones_aforo(mediciones:list[Medicion]):
    medias = []
    for h in range(24):
        l = list(filter(lambda x: x.fecha.hour == h , mediciones))
        if len(l) > 0:
            valores = list(map(lambda x: float(x.contenido),l))
            avg = sum(valores)/len(valores)
            medias.append(MediaAforo(hora = h,media= math.ceil(avg)))
    return medias


def filtra_dia(mediciones: list[Medicion], tipo: TipoMedicion,  fecha: datetime = datetime.now())->list[Medicion]:
    return list(filter(lambda medicion:medicion.tipo_medicion == tipo and medicion.fecha.date() == fecha.date(),mediciones))

def filtra_fecha(mediciones: Medicion, tipo: TipoMedicion, fecha_ini: datetime = None, fecha_fin: datetime = None)->list[Medicion]:
    
    return list(filter(lambda medicion:medicion.tipo_medicion == tipo and (fecha_fin is None or medicion.fecha <= fecha_fin)
                and (fecha_ini is None or medicion.fecha >= fecha_ini),mediciones))



""" while i < len(mediciones):
        nmed = defaultdict(int)
        vals  = defaultdict(float)
        f = mediciones[i].fecha
        h = f.hour

        while i < len(mediciones) and h == mediciones[i].fecha.hour:
            medinion = mediciones[i]
            vals[medinion.tipo_medicion.value] += float(medinion.contenido)
            nmed[medinion.tipo_medicion.value] += 1
            i+=1
        for k,n in nmed.items():
            val = vals[k]
            if tipo == TipoMedicion.aforo:
                res.append(MediaAforo())
            elif tipo == TipoMedicion.aire:
                ... """