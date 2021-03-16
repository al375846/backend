from datetime import date
from app.models.user import User


class Administrador(User):
    fecha_contratacion: date
