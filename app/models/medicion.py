from datetime import datetime
from typing import List, Optional, Union

from odmantic import EmbeddedModel
from pydantic.main import BaseModel
from app.enums.medicion import TipoMedicion

class Medicion(EmbeddedModel):
    tipo_medicion: TipoMedicion
    identificador_disp: str
    fecha: datetime = datetime.now()
    contenido: str



class InformeMedicionRet(BaseModel):
    contenido: Optional[List[Medicion]] = None

class MedicionRet(BaseModel):
    contenido: Optional[str] = None