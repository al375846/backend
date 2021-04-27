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
    
    def __add__(self,other):
        if type(other) == Medicion:
            return float(self.contenido) + float(other.contenido)
        else:
            return float(self.contenido) + other
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)



class Media(BaseModel):
    hora: int
    media:float

class MedicionEstablecimiento(BaseModel):
    descriptor: str
    id_establecimiento: str
    aforo_value: int = 0
    medias_aforo: List[Media] = []
    aire_value: int = 0
    medias_aire: List[Media] = []

class InformeMedicionRet(BaseModel):
    contenido: Optional[List[Medicion]] = None

class MedicionRet(BaseModel):
    contenido: Optional[str] = None