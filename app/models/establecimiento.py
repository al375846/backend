from app.models.db_base import DbBase

class Establecimiento(DbBase):
    identificador: str
    direccion: str
    aforo: int