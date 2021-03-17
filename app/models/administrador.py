from datetime import datetime
from app.models.user import User


class Administrador(User):
    fecha_contratacion: datetime
