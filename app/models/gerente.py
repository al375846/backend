from app.enums.suscripcion import TipoSuscripcion
from typing import Optional
from app.models.user import User


class Gerente(User):
    suscripciones: Optional[list[TipoSuscripcion]]

