from typing import Optional
from odmantic import EmbeddedModel, Field
from pydantic import BaseModel


class ConfiguracionEstablecimiento(EmbeddedModel):
    max_aforo: int = 10
    margen_aforo: int = Field(8,lt=max_aforo)
    max_ppm: int = 1000
    margen_ppm: int = Field(900,lt=max_ppm)



