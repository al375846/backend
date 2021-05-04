from app.models.generic_respones import BasicReturn
from app.models.incidencia import Incidencia, NewIncidencia
from app.models.gerente import Gerente

from fastapi import Depends, BackgroundTasks
from fastapi.routing import APIRouter
from app.utils.security import get_current_gerente
from app.db.db import db
from app.utils.send_email import send_mail

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])


@router.post("", response_model=BasicReturn)
async def nuevaIncidencia(
    incidencia: NewIncidencia,
    bt: BackgroundTasks,
    gerente: Gerente = Depends(get_current_gerente),
):
    incidencia_interna = Incidencia(gerente=gerente, **incidencia.dict())
    await db.motor.save(incidencia_interna)
    bt.add_task(send_mail, incidencia_interna)
    return BasicReturn()
