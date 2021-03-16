from app.models.db_base import DbBase

class Sugerencia(DbBase):
    identificador: str
    contenido: str
    resolucion: bool