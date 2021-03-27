from enum import Enum

class TipoMedicion(str, Enum):
    aforo = "AFORO"
    distancia = "DISTANCIA"
    mascarillas = "MASCARILLAS"
    aire = "AIRE"
