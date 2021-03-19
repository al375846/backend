from enum import Enum


class UserType(str, Enum):
    administrador = "administrador"
    gerente = "gerente"
