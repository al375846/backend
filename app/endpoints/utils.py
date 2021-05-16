from fastapi.exceptions import HTTPException
from app.models.medicion import Medicion
from fastapi import APIRouter, status
from app.db.db import db
from app.enums.medicion import TipoMedicion
from odmantic import ObjectId
from app.models.establecimiento import EstablecimientoDB
import datetime
from random import randrange
from fastapi import Query
from datetime import date

router = APIRouter(prefix="/utils", tags=["Utils"])


def random_date(dia: int, mes: int, ano: int, h_i: int = 9, h_f: int = 20):
    today = datetime.datetime(ano, mes, dia)
    start = datetime.datetime(today.year, today.month, today.day, h_i)
    end = datetime.datetime(today.year, today.month, today.day, h_f)

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


@router.post("")
async def genera_mediciones_falsas(
    id_establecimiento: ObjectId,
    n_mediciones: int,
    h_i: int = 9,
    h_f: int = 20,
    dia: int = Query(date.today().day, gt=1, le=31),
    mes: int = Query(date.today().month, gt=1, le=12),
    ano: int = Query(date.today().year, gt=1),
    tipo: TipoMedicion = TipoMedicion.aforo,
    rango_valores_tope: int = 10,
    rango_valores_min: int = 0,
):

    est = await db.motor.find_one(
        EstablecimientoDB, EstablecimientoDB.id == id_establecimiento
    )
    if est is not None:
        horas = sorted(
            random_date(dia, mes, ano, h_i, h_f) for _ in range(n_mediciones)
        )
        mediciones = []
        for h in horas:
            mediciones.append(
                Medicion(
                    tipo_medicion=tipo,
                    identificador_disp="FAKE",
                    fecha=h,
                    contenido=randrange(rango_valores_min, rango_valores_tope),
                )
            )
        est.mediciones += mediciones
        await db.motor.save(est)
        return True

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No existe establecimiento"
        )
